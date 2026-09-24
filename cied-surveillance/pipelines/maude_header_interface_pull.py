#!/usr/bin/env python3
"""Targeted FDA MAUDE pull for CIED proximal lead-header interface candidates.

High-recall candidate generator, not an automatic root-cause classifier.

Pipeline:
1. download one FDA device bulk file and identify likely CIED MDR keys;
2. stream that period's narrative file and retain only interface-keyword text
   belonging to those CIED keys;
3. attach structured device-problem codes by MDR Report Key;
4. emit compact CSV + JSON summary;
5. delete raw downloads unless --keep-downloads is requested.

Raw FDA files never belong in git.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import tempfile
import time
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

# MAUDE manufacturer narratives can exceed Python's conservative default field
# limit. Keep a finite but generous ceiling so malformed data cannot allocate
# unbounded memory.
csv.field_size_limit(100_000_000)

BASE = "https://www.accessdata.fda.gov/MAUDE/ftparea"

KNOWN_PROBLEM_CODES = {
    "1036": "Signal Artifact/Noise",
    "1081": "Failure to Capture",
    "1260": "Fracture",
    "1291": "High impedance",
    "1316": "Difficult to Insert",
    "1371": "Loose or Intermittent Connection",
    "1399": "Misconnection",
    "1438": "Over-Sensing",
    "2183": "Fitting Problem",
    "2900": "Connection Problem",
    "2926": "Electrical Shorting",
}

# Known CIED product codes in the seed corpus. Manufacturer + device-name
# fallback is deliberately retained to avoid treating this list as exhaustive.
CIED_PRODUCT_CODES = {"DXY", "LWP", "LWS", "MRM", "NIK", "NVY", "NVZ"}

CIED_MANUFACTURER_RE = re.compile(
    r"(abbott|st[ ._-]*jude|medtronic|boston scientific|biotronik|"
    r"microport|sorin|livanova|cardiac pacemakers)",
    re.I,
)
CIED_DEVICE_RE = re.compile(
    r"(pacemaker|pulse[- ]?generator|implantable cardioverter|defibrillat|"
    r"cardiac resynchronization|\bicd\b|\bcrt[- ]?[dp]\b|"
    r"defibrillation lead|permanent defibrillator electrode|pacing lead)",
    re.I,
)

TERM_PATTERNS = {
    "header": re.compile(r"\bheader\b", re.I),
    "terminal_pin": re.compile(r"\bterminal\s+pin\b", re.I),
    "lead_pin": re.compile(r"\blead\s+pin\b", re.I),
    "connector_block": re.compile(r"\bconnector\s+block\b", re.I),
    "connector_bore": re.compile(r"\bconnector\s+(?:bore|port)\b|\bheader\s+bore\b", re.I),
    "setscrew": re.compile(r"\bset\s*-?\s*screw\b|\bsetscrew\b", re.I),
    "spring_contact": re.compile(r"\bspring\s+(?:contact|connector|element)\b", re.I),
    "under_insertion": re.compile(
        r"under[- ]?insert|incomplete(?:ly)?\s+insert|not\s+fully\s+insert|"
        r"difficult\s+to\s+insert|fully\s+seat|not\s+fully\s+seat",
        re.I,
    ),
    "reseat_reconnect": re.compile(
        r"re[- ]?seat|reinsert|re[- ]?insert|reconnect|re[- ]?connect|"
        r"detach(?:ed)?\s+and\s+re[- ]?attach",
        re.I,
    ),
    "intermittent_connection": re.compile(r"intermittent\s+(?:connection|contact)", re.I),
    "cross_contact": re.compile(r"cross[- ]?contact|between\s+(?:the\s+)?contacts", re.I),
    "conductive_bridge": re.compile(r"conductive\s+bridge", re.I),
    "current_leakage": re.compile(r"current\s+leak|leakage\s+(?:path|current)", re.I),
    "crosstalk": re.compile(r"cross[- ]?talk|crosstalk", re.I),
    "ingress_contamination": re.compile(
        r"(?:fluid|blood|moisture)\s+(?:ingress|entry|inside)|"
        r"contaminat(?:ion|ed)|seal(?:ing)?\s+ring",
        re.I,
    ),
    "arc_over": re.compile(r"arc[- ]?over|electrical\s+arc", re.I),
}

STRONG_INTERFACE_TERMS = {
    "header", "terminal_pin", "lead_pin", "connector_block", "connector_bore",
    "setscrew", "spring_contact", "under_insertion", "reseat_reconnect",
    "intermittent_connection", "cross_contact", "conductive_bridge",
    "current_leakage", "ingress_contamination",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--periods",
        nargs="+",
        default=["current"],
        help="Calendar years and/or 'current'. Example: 2025 current",
    )
    p.add_argument(
        "--output-dir",
        default="cied-surveillance/warehouse/maude-header-pilot",
    )
    p.add_argument("--keep-downloads", action="store_true")
    return p.parse_args()


def file_urls(period: str) -> tuple[str, str]:
    if period == "current":
        return f"{BASE}/foitext.zip", f"{BASE}/device.zip"
    if not re.fullmatch(r"20\d{2}|19\d{2}", period):
        raise ValueError(f"Unsupported period: {period}")
    return f"{BASE}/foitext{period}.zip", f"{BASE}/device{period}.zip"


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    print(f"Downloading {url}", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Cardio-research-CIED/0.3"})
    with urllib.request.urlopen(req, timeout=180) as response, dest.open("wb") as f:
        shutil.copyfileobj(response, f, length=1024 * 1024)
    print(f"Downloaded {dest.name}: {dest.stat().st_size:,} bytes", flush=True)


def open_first_zip_member(path: Path):
    zf = zipfile.ZipFile(path)
    members = [n for n in zf.namelist() if not n.endswith("/")]
    if not members:
        zf.close()
        raise RuntimeError(f"No file in {path}")
    raw = zf.open(members[0], "r")
    txt = io.TextIOWrapper(raw, encoding="latin-1", errors="replace", newline="")
    return zf, txt


def likely_cied(rec: dict[str, str]) -> bool:
    code = rec["product_code"].strip().upper()
    haystack = " ".join(
        rec[k] for k in ("brand", "generic_name", "manufacturer", "model")
    )
    if code in CIED_PRODUCT_CODES and CIED_MANUFACTURER_RE.search(haystack):
        return True
    return bool(CIED_MANUFACTURER_RE.search(haystack) and CIED_DEVICE_RE.search(haystack))


def collect_cied_devices(zip_path: Path) -> dict[str, list[dict[str, str]]]:
    """Scan device table first so non-CIED narratives never enter memory."""
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    zf, stream = open_first_zip_member(zip_path)
    try:
        reader = csv.reader(stream, delimiter="|")
        for row in reader:
            if len(row) < 31:
                continue
            key = row[0].strip()
            if not key.isdigit():
                continue

            # FDA's published layout places Brand Name at field 7 and
            # Device Report Product Code at field 26 (one-based). The live
            # 2026 device file has three additional pre-brand fields, shifting
            # the Section-D block by +3. Detect the live layout from the
            # product-code slot rather than hard-coding one generation.
            extended = len(row) >= 34 and bool(re.fullmatch(r"[A-Z]{3}", row[28].strip()))
            shift = 3 if extended else 0

            def field(base_zero_index: int) -> str:
                idx = base_zero_index + shift
                return row[idx].strip() if idx < len(row) else ""

            rec = {
                "mdr_report_key": key,
                "brand": field(6),
                "generic_name": field(7),
                "manufacturer": field(8),
                "model": field(19),
                "catalog": field(20),
                "product_code": field(25),
                "device_age": field(26),
                "device_evaluated": field(27),
            }
            if likely_cied(rec):
                out[key].append(rec)
    finally:
        stream.close()
        zf.close()
    return out


def text_matches(text: str) -> set[str]:
    return {name for name, pat in TERM_PATTERNS.items() if pat.search(text)}


def collect_text_candidates(zip_path: Path, cied_keys: set[str]) -> dict[str, dict]:
    """Retain only matching narratives for MDRs already known to be CIED."""
    out: dict[str, dict] = {}
    zf, stream = open_first_zip_member(zip_path)
    try:
        reader = csv.reader(stream, delimiter="|")
        for row in reader:
            if len(row) < 6:
                continue
            key = row[0].strip()
            if key not in cied_keys:
                continue
            text_type = row[2].strip()
            text = row[5].strip()
            matches = text_matches(text)
            if not matches:
                continue
            rec = out.setdefault(
                key,
                {"matched_terms": set(), "texts": [], "text_types": []},
            )
            rec["matched_terms"].update(matches)
            rec["texts"].append(text[:100_000])
            rec["text_types"].append(text_type)
    finally:
        stream.close()
        zf.close()
    return out


def collect_problem_codes(zip_path: Path, keep_keys: set[str]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    zf, stream = open_first_zip_member(zip_path)
    try:
        reader = csv.reader(stream, delimiter="|")
        for row in reader:
            if len(row) < 2:
                continue
            key, code = row[0].strip(), row[1].strip()
            if key in keep_keys and code:
                out[key].add(code)
    finally:
        stream.close()
        zf.close()
    return out


def simple_priority(matched: set[str], codes: set[str]) -> str:
    if matched & {"cross_contact", "conductive_bridge", "current_leakage"}:
        return "A_PHYSICAL_CROSS_CONTACT_CANDIDATE"
    if matched & STRONG_INTERFACE_TERMS:
        return "B_INTERFACE_CANDIDATE"
    if "crosstalk" in matched:
        return "C_CROSSTALK_SIGNAL_ONLY_CANDIDATE"
    if "arc_over" in matched:
        return "D_HEADER_NONLEAD_OR_UNRESOLVED"
    if codes & {"1371", "1399", "2900", "2926"}:
        return "B_INTERFACE_CANDIDATE"
    return "E_LOW_SPECIFICITY"


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_ctx = None
    if args.keep_downloads:
        download_dir = output_dir / "downloads"
        download_dir.mkdir(exist_ok=True)
    else:
        temp_ctx = tempfile.TemporaryDirectory(prefix="maude-cied-")
        download_dir = Path(temp_ctx.name)

    rows_out: list[dict[str, str]] = []
    stats = {
        "periods": args.periods,
        "generated_unix": int(time.time()),
        "period_stats": {},
        "method": "FDA bulk device-first CIED filter, then narrative interface-keyword filter",
        "warning": "Candidates are not confirmed interface failures; manual narrative adjudication is required.",
    }

    try:
        for period in args.periods:
            text_url, device_url = file_urls(period)
            text_zip = download_dir / f"text-{period}.zip"
            device_zip = download_dir / f"device-{period}.zip"

            # Device-first order is deliberate.
            download(device_url, device_zip)
            devices_all = collect_cied_devices(device_zip)
            print(f"{period}: {len(devices_all):,} CIED MDR keys before narrative filter", flush=True)

            download(text_url, text_zip)
            text_candidates = collect_text_candidates(text_zip, set(devices_all))
            keep_keys = set(text_candidates)
            print(f"{period}: {len(keep_keys):,} CIED MDR keys with interface terms", flush=True)

            if period == "current":
                problem_url = f"{BASE}/foidevproblem.zip"
                problem_zip = download_dir / "problems-current.zip"
            else:
                problem_url = f"{BASE}/foidevproblem_thru2025.zip"
                problem_zip = download_dir / "problems-thru2025.zip"
            download(problem_url, problem_zip)
            problem_codes = collect_problem_codes(problem_zip, keep_keys)

            term_counter = Counter()
            manufacturer_counter = Counter()
            for key in sorted(keep_keys, key=int):
                txt = text_candidates[key]
                terms = set(txt["matched_terms"])
                codes = problem_codes.get(key, set())
                term_counter.update(terms)
                for device in devices_all[key]:
                    manufacturer_counter[device["manufacturer"]] += 1
                    code_labels = [
                        f"{c}:{KNOWN_PROBLEM_CODES.get(c, 'UNMAPPED')}"
                        for c in sorted(codes)
                    ]
                    rows_out.append(
                        {
                            **device,
                            "report_period": period,
                            "matched_terms": ";".join(sorted(terms)),
                            "problem_codes": ";".join(code_labels),
                            "priority_bucket": simple_priority(terms, codes),
                            "narrative_types": ";".join(txt["text_types"]),
                            "matching_narratives": " || ".join(txt["texts"]),
                        }
                    )

            stats["period_stats"][period] = {
                "n_cied_mdr_keys_before_narrative_filter": len(devices_all),
                "n_cied_mdr_keys_matching_interface_terms": len(keep_keys),
                "n_device_rows_output": sum(len(devices_all[k]) for k in keep_keys),
                "top_terms": term_counter.most_common(),
                "top_manufacturers": manufacturer_counter.most_common(20),
                "text_source": text_url,
                "device_source": device_url,
            }

        fieldnames = [
            "mdr_report_key", "report_period", "manufacturer", "brand",
            "generic_name", "model", "catalog", "product_code", "device_age",
            "device_evaluated", "matched_terms", "problem_codes",
            "priority_bucket", "narrative_types", "matching_narratives",
        ]
        candidate_path = output_dir / "header_interface_candidates.csv"
        with candidate_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_out)

        stats["n_output_rows"] = len(rows_out)
        stats["n_unique_mdr_keys"] = len({r["mdr_report_key"] for r in rows_out})
        stats["priority_counts"] = dict(Counter(r["priority_bucket"] for r in rows_out))
        stats["candidate_csv"] = str(candidate_path)

        with (output_dir / "summary.json").open("w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

        print(json.dumps(stats, indent=2), flush=True)
    finally:
        if temp_ctx is not None:
            temp_ctx.cleanup()


if __name__ == "__main__":
    main()
