#!/usr/bin/env python3
"""Boston Scientific ACCOLADE-family PaceSafe/automatic-threshold MAUDE sweep."""

from __future__ import annotations
import argparse,csv,hashlib,io,json,re,shutil,tempfile,time,urllib.request,zipfile
from collections import Counter,defaultdict
from pathlib import Path
csv.field_size_limit(100_000_000)
BASE="https://www.accessdata.fda.gov/MAUDE/ftparea"

BSC_RE=re.compile(r"boston scientific",re.I)
FAMILY_RE=re.compile(r"(accolade|proponent|essentio|altrua\s*2|visionist|valitude)",re.I)
TERM_RE=re.compile(
    r"\bpacesafe\b|\brvat\b|\braat\b|right\s+ventricular\s+automatic\s+threshold|"
    r"right\s+atrial\s+automatic\s+threshold|automatic\s+threshold|auto\s+threshold|"
    r"automatic\s+capture",
    re.I,
)
CLINICAL_RE=re.compile(r"(syncope|presyncope|asystol|bradycard|loss\s+of\s+capture|failure\s+to\s+capture|pacing\s+inhibition|dizz|lighthead|hypotension)",re.I)
TEST_INTERACTION_RE=re.compile(r"(during|while|following|after).{0,120}(?:rvat|raat|automatic\s+threshold|threshold\s+test)|(?:rvat|raat|automatic\s+threshold|threshold\s+test).{0,120}(?:loss\s+of\s+capture|failure\s+to\s+capture|asystol|bradycard|pacing\s+inhibition|tachycard|vt\b|vf\b)",re.I)
SUSPEND_RE=re.compile(r"(rvat|raat|automatic\s+threshold).{0,120}(suspend|retry|low\s+er|low\s+evoked|noise|greater\s+than\s+programmed)",re.I)
DATA_RE=re.compile(r"(atrial\s+fibrillation|atr\b|burden|logbook|trend|data).{0,180}(rvat|raat|automatic\s+threshold)|(rvat|raat|automatic\s+threshold).{0,180}(burden|logbook|trend|data)",re.I)
LEAD_RE=re.compile(r"(lead\s+(?:dislodg|fractur|damage|insulation|high\s+threshold|impedance)|non[- ]?boston\s+scientific\s+lead|lead\s+revision)",re.I)
BATTERY_RE=re.compile(r"(battery\s+longevity|power\s+consumption|battery\s+deplet|eri|eol|high\s+output)",re.I)

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--periods",nargs="+",required=True)
    p.add_argument("--output-dir",required=True)
    return p.parse_args()

def urls(period):
    if period=="current": return f"{BASE}/foitext.zip",f"{BASE}/device.zip"
    return f"{BASE}/foitext{period}.zip",f"{BASE}/device{period}.zip"

def dl(url,dest):
    if dest.exists(): return
    req=urllib.request.Request(url,headers={"User-Agent":"Cardio-research-Boston-PaceSafe/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r,dest.open("wb") as f:
        shutil.copyfileobj(r,f,1024*1024)

def stream_zip(path):
    z=zipfile.ZipFile(path); names=[n for n in z.namelist() if not n.endswith("/")]
    raw=z.open(names[0]); txt=io.TextIOWrapper(raw,encoding="latin-1",errors="replace",newline="")
    return z,txt

def device_fields(row):
    if len(row)==34:
        get=lambda i: row[i].strip() if i<len(row) else ""
        return {"key":get(0),"brand":get(9),"generic":get(10),"mfr":get(11),"model":get(22),"product_code":get(28)}
    if len(row)>=31:
        get=lambda i: row[i].strip() if i<len(row) else ""
        return {"key":get(0),"brand":get(6),"generic":get(7),"mfr":get(8),"model":get(19),"product_code":get(25)}
    return None

def is_target(d):
    h=" ".join([d["brand"],d["generic"],d["mfr"],d["model"]])
    return bool(BSC_RE.search(h) and FAMILY_RE.search(h))

def family(brand):
    m=FAMILY_RE.search(brand or "")
    return m.group(1).upper().replace(" ","") if m else "OTHER"

def event_hash(texts):
    norm=sorted(set(re.sub(r"\s+"," ",t).strip().lower() for t in texts if t.strip()))
    return hashlib.sha256(" || ".join(norm).encode()).hexdigest()[:20]

def classify(text):
    if TEST_INTERACTION_RE.search(text) and CLINICAL_RE.search(text):
        return "A_TEST_OR_ALGORITHM_CLINICAL_INTERACTION"
    if DATA_RE.search(text):
        return "B_DATA_DIAGNOSTIC_INTERACTION"
    if SUSPEND_RE.search(text) and CLINICAL_RE.search(text):
        return "C_SUSPENDED_TEST_WITH_CAPTURE_OR_SYMPTOM"
    if SUSPEND_RE.search(text):
        return "D_SUSPENDED_OR_FAILED_TEST"
    if BATTERY_RE.search(text):
        return "E_OUTPUT_OR_LONGEVITY"
    if LEAD_RE.search(text):
        return "F_LEAD_HARDWARE_CONTEXT"
    if CLINICAL_RE.search(text):
        return "G_CLINICAL_EVENT_AUTOTHRESHOLD_MENTION"
    return "H_OTHER_PACESAFE_MENTION"

def main():
    a=parse_args(); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    rows=[]; stats={"periods":a.periods,"generated_unix":int(time.time()),"period_stats":{}}
    with tempfile.TemporaryDirectory(prefix="pacesafe-") as td:
        td=Path(td)
        for period in a.periods:
            text_url,dev_url=urls(period); dz=td/f"device-{period}.zip"; tz=td/f"text-{period}.zip"
            dl(dev_url,dz); dl(text_url,tz)
            devices=defaultdict(list)
            z,s=stream_zip(dz)
            try:
                for row in csv.reader(s,delimiter="|"):
                    d=device_fields(row)
                    if d and d["key"].isdigit() and is_target(d): devices[d["key"]].append(d)
            finally: s.close(); z.close()
            narratives=defaultdict(list)
            z,s=stream_zip(tz)
            try:
                for row in csv.reader(s,delimiter="|"):
                    if len(row)<6: continue
                    key=row[0].strip()
                    if key not in devices: continue
                    txt=row[5].strip()
                    if TERM_RE.search(txt): narratives[key].append(txt[:120000])
            finally: s.close(); z.close()
            for key,texts in narratives.items():
                joined=" || ".join(texts); h=event_hash(texts); cls=classify(joined)
                for d in devices[key]:
                    rows.append({**d,"family":family(d["brand"]),"period":period,"event_text_hash":h,"classification":cls,"narrative":joined})
            stats["period_stats"][period]={"family_mdr_keys":len(devices),"pacesafe_mdr_keys":len(narratives)}
    groups=defaultdict(list)
    for r in rows: groups[r["event_text_hash"]].append(r)
    stats["n_rows"]=len(rows)
    stats["n_mdr_keys"]=len(set(r["key"] for r in rows))
    stats["n_event_groups"]=len(groups)
    stats["classification_groups"]=dict(Counter(next(iter(v))["classification"] for v in groups.values()))
    stats["family_groups"]=dict(Counter(next(iter(v))["family"] for v in groups.values()))
    for r in rows: r["event_group_size"]=len(groups[r["event_text_hash"]])
    with (out/"pacesafe_candidates.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["key","period","event_text_hash","event_group_size","family","mfr","brand","generic","model","product_code","classification","narrative"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    with (out/"summary.json").open("w") as f: json.dump(stats,f,indent=2)
    print(json.dumps(stats,indent=2))
if __name__=="__main__": main()
