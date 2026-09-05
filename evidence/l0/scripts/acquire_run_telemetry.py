#!/usr/bin/env python3
"""
Telemetry Acquisition Protocol for Sandia Battery Degradation Audit
Route: Documented BatteryArchive Public Transfer Protocol (battery-archive-sandbox)
Source: https://www.batteryarchive.org/data/snl/{filename_base}_cycle_data.csv

Generates:
  - runs/{run_id}/raw_acquisition_manifest.json
  - runs/{run_id}/expected_vs_observed_cells.json
  - runs/{run_id}/inputs.sha256
  - runs/{run_id}/byte_count.txt
  - runs/{run_id}/acquisition_stdout.log
  - runs/{run_id}/acquisition_stderr.log
"""

import sys
import json
import hashlib
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

def compute_sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Acquire SNL Telemetry Files")
    parser.add_argument("--run-id", type=str, default="run-002-a1h", help="Run identifier")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    run_dir = repo_root / "runs" / args.run_id
    raw_data_dir = run_dir / "raw_data"
    raw_data_dir.mkdir(exist_ok=True, parents=True)

    log_out_path = run_dir / "acquisition_stdout.log"
    log_err_path = run_dir / "acquisition_stderr.log"

    out_lines = []
    err_lines = []

    def log_print(msg: str):
        print(msg)
        out_lines.append(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")

    def err_print(msg: str):
        print(f"ERROR: {msg}", file=sys.stderr)
        err_lines.append(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")

    log_print("===================================================================")
    log_print(f" Starting Telemetry Acquisition: {args.run_id}")
    log_print(" Protocol: BatteryArchive Public Download Protocol")
    log_print("===================================================================\n")

    # Load expected cells inventory from raw_listing.txt
    listing_path = repo_root / "evidence" / "l0" / "raw_listing.txt"
    if not listing_path.exists():
        err_print(f"raw_listing.txt not found at {listing_path}")
        sys.exit(1)

    expected_cells = []
    for line in listing_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("cell_id") or line.startswith("---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 2:
            expected_cells.append({
                "cell_id": parts[0],
                "filename_base": parts[1],
                "study": parts[2] if len(parts) > 2 else "snl",
                "cathode": parts[3] if len(parts) > 3 else "",
                "temp_C": parts[5] if len(parts) > 5 else "",
                "soc_range": parts[6] if len(parts) > 6 else ""
            })

    log_print(f"Total expected SNL cohort cells: {len(expected_cells)}")

    acquired_manifest = []
    sha256_records = []
    total_bytes = 0
    missing_cells = []
    successful_cells = []

    base_url = "https://www.batteryarchive.org/data/snl/"

    for idx, cinfo in enumerate(expected_cells):
        cell_id = cinfo["cell_id"]
        filename_base = cinfo["filename_base"]
        filename = f"{filename_base}_cycle_data.csv"
        file_url = f"{base_url}{filename}"
        local_dest = raw_data_dir / filename

        log_print(f"[{idx+1}/{len(expected_cells)}] Fetching {filename}...")
        
        req = urllib.request.Request(
            file_url,
            headers={"User-Agent": "VolMax-Audit-Engine/1.0 (Research Reconstruction; info@batteryarchive.org)"}
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                byte_len = len(content)
                sha256_hash = compute_sha256_bytes(content)

                local_dest.write_bytes(content)
                total_bytes += byte_len

                acquired_manifest.append({
                    "cell_id": cell_id,
                    "filename_base": filename_base,
                    "filename": filename,
                    "url": file_url,
                    "http_status": response.status,
                    "byte_count": byte_len,
                    "sha256": sha256_hash,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

                sha256_records.append(f"{sha256_hash}  {filename}")
                successful_cells.append(cell_id)
                log_print(f"  -> SUCCESS: {byte_len:,} bytes, SHA256: {sha256_hash[:12]}...")

        except urllib.error.HTTPError as e:
            err_print(f"HTTP {e.code} for {cell_id} ({filename}): {e.reason}")
            missing_cells.append({"cell_id": cell_id, "filename": filename, "error": f"HTTP {e.code}", "reason": str(e.reason)})
        except Exception as e:
            err_print(f"Fetch failed for {cell_id} ({filename}): {type(e).__name__} - {e}")
            missing_cells.append({"cell_id": cell_id, "filename": filename, "error": type(e).__name__, "reason": str(e)})

        # Courteous pacing (200ms)
        time.sleep(0.2)

    # Summary analysis
    expected_vs_observed = {
        "run_id": args.run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_expected_cells": len(expected_cells),
        "total_observed_cells": len(successful_cells),
        "total_missing_cells": len(missing_cells),
        "missing_cell_details": missing_cells,
        "unexpected_cells": [],
        "acquisition_complete": (len(missing_cells) == 0)
    }

    # Write manifest files
    (run_dir / "raw_acquisition_manifest.json").write_text(json.dumps(acquired_manifest, indent=2), encoding="utf-8")
    (run_dir / "expected_vs_observed_cells.json").write_text(json.dumps(expected_vs_observed, indent=2), encoding="utf-8")
    (run_dir / "inputs.sha256").write_text("\n".join(sha256_records) + "\n", encoding="utf-8")
    (run_dir / "byte_count.txt").write_text(f"Total Bytes Acquired: {total_bytes:,} bytes across {len(successful_cells)} files\n", encoding="utf-8")
    log_out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    log_err_path.write_text("\n".join(err_lines) + "\n", encoding="utf-8")

    log_print("\n===================================================================")
    log_print(f" Acquisition Complete: {len(successful_cells)}/{len(expected_cells)} files acquired.")
    log_print(f" Total bytes: {total_bytes:,} bytes.")
    log_print(f" Artifacts written to {run_dir}")
    log_print("===================================================================")

if __name__ == "__main__":
    main()
