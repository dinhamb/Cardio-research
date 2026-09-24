#!/usr/bin/env python3
"""Targeted FDA MAUDE pull for CIED battery and power-path mechanisms.

High-recall candidate generator. It does not infer that premature depletion
equals battery-cell failure. Raw FDA bulk files are temporary and not committed.
"""

from __future__ import annotations

import argparse, csv, hashlib, io, json, re, shutil, tempfile, time, urllib.request, zipfile
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(100_000_000)
BASE = "https://www.accessdata.fda.gov/MAUDE/ftparea"

MFG_RE = re.compile(
    r"(abbott|st[ ._-]*jude|medtronic|boston scientific|cardiac pacemakers|"
    r"biotronik|microport|sorin|livanova)", re.I
)
GENERATOR_RE = re.compile(
    r"(pacemaker|pulse[- ]?generator|implantable cardioverter|cardioverter[- ]?defibrillat|"
    r"cardiac resynchronization|\bicd\b|\bcrt[- ]?[dp]\b)", re.I
)
EXCLUDE_RE = re.compile(
    r"(lead|electrode|delivery system|catheter|neuromodulation|vascular|"
    r"structural heart|diabetes|neurovascular)", re.I
)

PATTERNS = {
    "lithium_cluster": re.compile(r"lithium\s+(?:cluster|bridge|bridging|dendrit)", re.I),
    "lithium_plating": re.compile(r"lithium\s+(?:plating|re[- ]?plating|plate)", re.I),
    "cell_internal_short": re.compile(
        r"(?:internal\s+(?:battery|cell)\s+short|(?:battery|cell)\s+internal\s+short)", re.I
    ),
    "anode_cathode_leakage": re.compile(
        r"(?:anode.{0,100}cathode|cathode.{0,100}anode).{0,120}(?:leak|short)|"
        r"(?:leak|short).{0,120}(?:anode.{0,100}cathode|cathode.{0,100}anode)", re.I
    ),
    "internal_self_depletion": re.compile(r"internal\s+self[- ]?depletion", re.I),
    "separator_barrier": re.compile(
        r"(?:battery|cell).{0,120}(?:separator|electrode\s+barrier)|"
        r"(?:separator|electrode\s+barrier).{0,120}(?:battery|cell)", re.I
    ),
    "battery_header_feedthrough": re.compile(r"battery\s+(?:header|feedthrough|hermetic)", re.I),
    "battery_terminal": re.compile(
        r"battery\s+(?:terminal\s+pin|terminal|post|spring\s+(?:contact|connector))", re.I
    ),
    "battery_interconnect": re.compile(
        r"(?:battery\s+(?:terminal(?:\s+pin)?|post|spring\s+(?:contact|connector)|interconnect))"
        r".{0,120}(?:corrod|open\s+connection|failed|failure|broken|fractur|discontinu|high\s+resistan)|"
        r"(?:corrod|open\s+connection|failed|failure|broken|fractur|discontinu|high\s+resistan)"
        r".{0,120}(?:battery\s+(?:terminal(?:\s+pin)?|post|spring\s+(?:contact|connector)|interconnect))|"
        r"(?:open\s+connection|discontinuity).{0,120}between\s+(?:the\s+)?battery\s+and\s+"
        r"(?:the\s+)?(?:hybrid|electronic(?:s)?\s+(?:module|assembly))",
        re.I,
    ),
    "abnormal_current_drain": re.compile(
        r"(?:abnormal|excess(?:ive)?|elevated|unexpected).{0,60}(?:current\s+(?:drain|draw|consumption))|"
        r"(?:current\s+(?:drain|draw|consumption)).{0,60}(?:abnormal|excess(?:ive)?|elevated|unexpected)", re.I
    ),
    "capacitor_load": re.compile(
        r"(?:capacitor|reform(?:ing)?).{0,100}(?:battery|deplet|drain|current)|"
        r"(?:battery|deplet|drain|current).{0,100}(?:capacitor|reform(?:ing)?)", re.I
    ),
    "telemetry_firmware_drain": re.compile(
        r"(?:telemetry|communication|firmware|software).{0,120}(?:battery|deplet|drain|current)", re.I
    ),
    "premature_depletion": re.compile(
        r"premature\s+(?:battery\s+)?deplet|rapid\s+(?:battery\s+)?deplet|"
        r"accelerated\s+(?:battery\s+)?deplet|unexpected\s+(?:battery\s+)?deplet|"
        r"battery\s+deplet(?:ed|ion).{0,80}(?:earl|premature|rapid|unexpected)", re.I
    ),
    "abrupt_power_loss": re.compile(
        r"(?:abrupt|sudden).{0,50}(?:power|battery).{0,50}(?:loss|deplet)|"
        r"(?:unable|could not|cannot).{0,50}interrogat.{0,100}(?:battery|power)", re.I
    ),
}

def args():
    p=argparse.ArgumentParser()
    p.add_argument("--periods", nargs="+", default=["current"])
    p.add_argument("--output-dir", default="cied-surveillance/warehouse/maude-battery-pilot")
    return p.parse_args()

def urls(period):
    if period=="current":
        return f"{BASE}/foitext.zip", f"{BASE}/device.zip", f"{BASE}/foidevproblem.zip"
    return f"{BASE}/foitext{period}.zip", f"{BASE}/device{period}.zip", f"{BASE}/foidevproblem_thru2025.zip"

def download(url,dest):
    if dest.exists() and dest.stat().st_size: return
    print("Downloading",url,flush=True)
    req=urllib.request.Request(url,headers={"User-Agent":"Cardio-research-CIED-battery/0.3"})
    with urllib.request.urlopen(req,timeout=180) as r, dest.open("wb") as f:
        shutil.copyfileobj(r,f,1024*1024)

def stream_zip(path):
    z=zipfile.ZipFile(path)
    n=next(x for x in z.namelist() if not x.endswith("/"))
    raw=z.open(n)
    return z,io.TextIOWrapper(raw,encoding="latin-1",errors="replace",newline="")

def is_generator(rec):
    h=" ".join(rec[k] for k in ("manufacturer","brand","generic_name","model"))
    return bool(MFG_RE.search(h) and GENERATOR_RE.search(h) and not EXCLUDE_RE.search(h))

def device_rows(path):
    out=defaultdict(list)
    z,s=stream_zip(path)
    try:
        for row in csv.reader(s,delimiter="|"):
            if len(row)<31 or not row[0].strip().isdigit(): continue
            if len(row)==34:
                get=lambda i: row[i].strip() if i<len(row) else ""
                rec={
                    "mdr_report_key":get(0),"device_sequence_no":get(4),
                    "device_date_received":get(8),"brand":get(9),"generic_name":get(10),
                    "manufacturer":get(11),"model":get(22),"catalog":get(23),
                    "device_availability":get(26),"date_returned_to_manufacturer":get(27),
                    "product_code":get(28),"device_age_text":get(29),"device_evaluated":get(30),
                    "device_layout":"CURRENT_34",
                }
            else:
                get=lambda i: row[i].strip() if i<len(row) else ""
                rec={
                    "mdr_report_key":get(0),"device_sequence_no":get(4),
                    "device_date_received":get(5),"brand":get(6),"generic_name":get(7),
                    "manufacturer":get(8),"model":get(19),"catalog":get(20),
                    "device_availability":get(23),"date_returned_to_manufacturer":get(24),
                    "product_code":get(25),"device_age_text":get(26),"device_evaluated":get(27),
                    "device_layout":"LEGACY_DOCUMENTED",
                }
            if is_generator(rec): out[rec["mdr_report_key"]].append(rec)
    finally:
        s.close(); z.close()
    return out

def matched(text):
    return {k for k,p in PATTERNS.items() if p.search(text)}

def narrative_rows(path, keys):
    out={}
    z,s=stream_zip(path)
    try:
        for row in csv.reader(s,delimiter="|"):
            if len(row)<6: continue
            key=row[0].strip()
            if key not in keys: continue
            m=matched(row[5])
            if not m: continue
            x=out.setdefault(key,{"terms":set(),"texts":[],"types":[],"dates":[]})
            x["terms"].update(m); x["texts"].append(row[5][:100000]); x["types"].append(row[2].strip())
            if row[4].strip(): x["dates"].append(row[4].strip())
    finally:
        s.close(); z.close()
    return out

def problem_rows(path,keys):
    out=defaultdict(set); z,s=stream_zip(path)
    try:
        for row in csv.reader(s,delimiter="|"):
            if len(row)>=2 and row[0].strip() in keys and row[1].strip():
                out[row[0].strip()].add(row[1].strip())
    finally:
        s.close(); z.close()
    return out

def event_hash(texts):
    vals=sorted(set(re.sub(r"\s+"," ",t).strip().lower() for t in texts if t.strip()))
    return hashlib.sha256(" || ".join(vals).encode()).hexdigest()[:20]

def priority(terms):
    if terms & {"lithium_cluster","lithium_plating","cell_internal_short","anode_cathode_leakage","internal_self_depletion"}:
        return "A_CELL_MECHANISM_CANDIDATE"
    if terms & {"battery_terminal","battery_interconnect"}:
        return "B_BATTERY_INTERCONNECT_CANDIDATE"
    if "battery_header_feedthrough" in terms:
        return "C_BATTERY_PACKAGE_CANDIDATE"
    if terms & {"abnormal_current_drain","capacitor_load","telemetry_firmware_drain"}:
        return "D_GENERATOR_LOAD_CANDIDATE"
    return "E_DEPLETION_PHENOTYPE_ONLY_CANDIDATE"

def main():
    a=args(); outdir=Path(a.output_dir); outdir.mkdir(parents=True,exist_ok=True)
    rows=[]; stats={"periods":a.periods,"generated_unix":int(time.time()),"period_stats":{}}
    with tempfile.TemporaryDirectory(prefix="maude-battery-") as td:
        td=Path(td)
        for period in a.periods:
            tu,du,pu=urls(period); dz=td/f"device-{period}.zip"; tz=td/f"text-{period}.zip"; pz=td/f"problem-{period}.zip"
            download(du,dz); devices=device_rows(dz)
            print(period, f"{len(devices):,} generator MDR keys",flush=True)
            download(tu,tz); narr=narrative_rows(tz,set(devices)); keep=set(narr)
            print(period, f"{len(keep):,} battery/power narrative candidates",flush=True)
            download(pu,pz); problems=problem_rows(pz,keep)
            termc=Counter()
            for key in sorted(keep,key=int):
                x=narr[key]; termc.update(x["terms"])
                for dev in devices[key]:
                    rows.append({**dev,"report_period":period,"event_text_hash":event_hash(x["texts"]),
                        "matched_terms":";".join(sorted(x["terms"])),"priority_bucket":priority(x["terms"]),
                        "problem_codes":";".join(sorted(problems.get(key,set()))),
                        "narrative_report_dates":";".join(sorted(set(x["dates"]))),
                        "matching_narratives":" || ".join(x["texts"])})
            stats["period_stats"][period]={"n_generator_mdr_keys":len(devices),"n_candidate_mdr_keys":len(keep),
                "top_terms":termc.most_common(),"text_source":tu,"device_source":du}
    counts=Counter(r["event_text_hash"] for r in rows)
    for r in rows:r["event_text_group_size"]=str(counts[r["event_text_hash"]])
    fields=["mdr_report_key","report_period","event_text_hash","event_text_group_size","device_sequence_no","device_layout","manufacturer","brand",
        "generic_name","model","catalog","product_code","device_date_received","device_age_text",
        "device_availability","date_returned_to_manufacturer","device_evaluated","matched_terms","priority_bucket",
        "problem_codes","narrative_report_dates","matching_narratives"]
    p=outdir/"battery_candidates.csv"
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    stats.update({"n_output_rows":len(rows),"n_unique_mdr_keys":len({r["mdr_report_key"] for r in rows}),
        "n_unique_exact_narrative_event_groups":len(counts),
        "priority_counts":dict(Counter(r["priority_bucket"] for r in rows))})
    (outdir/"summary.json").write_text(json.dumps(stats,indent=2),encoding="utf-8")
    print(json.dumps(stats,indent=2),flush=True)

if __name__=="__main__": main()
