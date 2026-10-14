#!/usr/bin/env python3
"""Abbott/St Jude pacemaker AutoCapture MAUDE narrative surveillance.

Searches FDA MAUDE yearly bulk device + narrative files and emits only CRM
generator MDRs whose narratives mention AutoCapture/capture-management terms.
This is a signal corpus, not an incidence denominator.
"""

from __future__ import annotations
import argparse,csv,hashlib,io,json,re,shutil,tempfile,time,urllib.request,zipfile
from collections import Counter,defaultdict
from pathlib import Path
csv.field_size_limit(100_000_000)
BASE="https://www.accessdata.fda.gov/MAUDE/ftparea"

ABBOTT_RE=re.compile(r"(abbott|st[ ._-]*jude|pacesetter)",re.I)
PACER_RE=re.compile(r"(pacemaker|pulse[- ]?generator|implantable pulse generator|\bpm\d{3,4}\b|assurity|enduri(?:ty|ty)|accent|victory|zephyr|identity)",re.I)
TERM_RE=re.compile(r"\bauto\s*-?\s*capture\b|\bautocapture\b|automatic\s+capture|capture\s+algorithm",re.I)
TRUE_CAPTURE_RE=re.compile(r"(ineffective\s+pacing|failure\s+to\s+capture|failed\s+to\s+capture|loss\s+of\s+capture|inadequate\s+capture|captur(?:e|ing)\s+problem|no\s+capture)",re.I)
ALGORITHM_CAUSE_RE=re.compile(r"(due\s+to\s+(?:the\s+)?auto\s*-?\s*capture|autocapture\s+algorithm|capture\s+algorithm.{0,120}(?:caus|result|lead)|(?:caus|result|lead).{0,120}autocapture)",re.I)
REPROGRAM_RE=re.compile(r"reprogram|programmed\s+(?:off|to)|turn(?:ed)?\s+off|disabled",re.I)
LONGEVITY_RE=re.compile(r"(premature\s+(?:battery|discharge)|battery\s+deplet|longevity|eri|eol|high\s+output|current\s+drain)",re.I)
NOT_CONFIRMED_RE=re.compile(r"(not\s+confirmed|could\s+not\s+be\s+confirmed|no\s+anomal)",re.I)

def args():
    p=argparse.ArgumentParser()
    p.add_argument("--periods",nargs="+",required=True)
    p.add_argument("--output-dir",required=True)
    return p.parse_args()

def urls(period):
    if period=="current": return f"{BASE}/foitext.zip",f"{BASE}/device.zip"
    return f"{BASE}/foitext{period}.zip",f"{BASE}/device{period}.zip"

def dl(url,dest):
    if dest.exists(): return
    req=urllib.request.Request(url,headers={"User-Agent":"Cardio-research-Abbott-AutoCapture/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r,dest.open("wb") as f: shutil.copyfileobj(r,f,1024*1024)

def stream_zip(path):
    z=zipfile.ZipFile(path); names=[n for n in z.namelist() if not n.endswith("/")]
    raw=z.open(names[0]); txt=io.TextIOWrapper(raw,encoding="latin-1",errors="replace",newline="")
    return z,txt

def device_fields(row):
    # Match validated MAUDE layouts from the CIED interface pipeline.
    if len(row)==34:
        get=lambda i: row[i].strip() if i<len(row) else ""
        return {"key":get(0),"brand":get(9),"generic":get(10),"mfr":get(11),"model":get(22),"product_code":get(28)}
    if len(row)>=31:
        get=lambda i: row[i].strip() if i<len(row) else ""
        return {"key":get(0),"brand":get(6),"generic":get(7),"mfr":get(8),"model":get(19),"product_code":get(25)}
    return None

def is_abbott_pacer(d):
    h=" ".join([d["brand"],d["generic"],d["mfr"],d["model"]])
    return bool(ABBOTT_RE.search(h) and PACER_RE.search(h))

def event_hash(texts):
    norm=sorted(set(re.sub(r"\s+"," ",t).strip().lower() for t in texts if t.strip()))
    return hashlib.sha256(" || ".join(norm).encode()).hexdigest()[:20]

def classify(text):
    if ALGORITHM_CAUSE_RE.search(text) and TRUE_CAPTURE_RE.search(text):
        return "A_EXPLICIT_ALGORITHM_CAPTURE_FAILURE"
    if TRUE_CAPTURE_RE.search(text) and REPROGRAM_RE.search(text):
        return "B_CAPTURE_EVENT_WITH_REPROGRAMMING"
    if TRUE_CAPTURE_RE.search(text):
        return "C_CAPTURE_EVENT_AUTOCAPTURE_MENTION"
    if LONGEVITY_RE.search(text):
        if NOT_CONFIRMED_RE.search(text):
            return "D_LONGEVITY_NORMAL_OR_NOT_CONFIRMED"
        return "E_LONGEVITY_OR_HIGH_OUTPUT"
    return "F_OTHER_AUTOCAPTURE_MENTION"

def main():
    a=args(); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    rows=[]; stats={"periods":a.periods,"generated_unix":int(time.time()),"period_stats":{}}
    with tempfile.TemporaryDirectory(prefix="autocap-") as td:
        td=Path(td)
        for period in a.periods:
            text_url,dev_url=urls(period); dz=td/f"device-{period}.zip"; tz=td/f"text-{period}.zip"
            dl(dev_url,dz); dl(text_url,tz)
            devices=defaultdict(list)
            z,s=stream_zip(dz)
            try:
                for row in csv.reader(s,delimiter="|"):
                    d=device_fields(row)
                    if d and d["key"].isdigit() and is_abbott_pacer(d): devices[d["key"]].append(d)
            finally: s.close(); z.close()
            narratives=defaultdict(list)
            z,s=stream_zip(tz)
            try:
                for row in csv.reader(s,delimiter="|"):
                    if len(row)<6: continue
                    key=row[0].strip()
                    if key not in devices: continue
                    txt=row[5].strip()
                    if TERM_RE.search(txt): narratives[key].append(txt[:100000])
            finally: s.close(); z.close()
            for key,texts in narratives.items():
                joined=" || ".join(texts); h=event_hash(texts); cls=classify(joined)
                for d in devices[key]:
                    rows.append({**d,"period":period,"event_text_hash":h,"classification":cls,"narrative":joined})
            stats["period_stats"][period]={"abbott_pacer_mdr_keys":len(devices),"autocapture_mdr_keys":len(narratives)}
    groups=defaultdict(list)
    for r in rows: groups[r["event_text_hash"]].append(r)
    for r in rows: r["event_group_size"]=len(groups[r["event_text_hash"]])
    stats["n_rows"]=len(rows); stats["n_mdr_keys"]=len(set(r["key"] for r in rows)); stats["n_event_groups"]=len(groups)
    stats["classification_groups"]=dict(Counter(next(iter(v))["classification"] for v in groups.values()))
    with (out/"autocapture_candidates.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["key","period","event_text_hash","event_group_size","mfr","brand","generic","model","product_code","classification","narrative"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    with (out/"summary.json").open("w") as f: json.dump(stats,f,indent=2)
    print(json.dumps(stats,indent=2))
if __name__=="__main__": main()
