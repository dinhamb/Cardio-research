#!/usr/bin/env python3
import csv, io, zipfile, urllib.request, tempfile, shutil
from pathlib import Path

csv.field_size_limit(100_000_000)
url="https://www.accessdata.fda.gov/MAUDE/ftparea/device2025.zip"
with tempfile.TemporaryDirectory(prefix="maude-layout-") as td:
    p=Path(td)/"device2025.zip"
    req=urllib.request.Request(url, headers={"User-Agent":"Cardio-research-CIED-layout-probe/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r, p.open("wb") as f:
        shutil.copyfileobj(r,f,1024*1024)
    with zipfile.ZipFile(p) as z:
        member=next(n for n in z.namelist() if not n.endswith("/"))
        with z.open(member) as raw:
            stream=io.TextIOWrapper(raw,encoding="latin-1",errors="replace",newline="")
            for row in csv.reader(stream,delimiter="|"):
                if row and row[0].strip().isdigit():
                    print("DEVICE2025_LAYOUT", "field_count="+str(len(row)))
                    print({i: row[i].strip()[:80] for i in range(min(len(row),36))})
                    break
