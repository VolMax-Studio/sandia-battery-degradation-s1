#!/usr/bin/env python3
"""
Mechanical Generator for Target A1-H Required Inputs Manifest
Derives canonical required cell inputs exclusively from raw_listing.txt and a1_h_eligibility_manifest.json.
"""

import json
import hashlib
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parents[3]
    listing_path = repo_root / "evidence" / "l0" / "raw_listing.txt"
    eligibility_path = repo_root / "artifacts" / "a1_h_eligibility_manifest.json"
    output_path = repo_root / "runs" / "run-002-a1h" / "a1_h_required_inputs.json"

    listing_bytes = listing_path.read_bytes()
    listing_sha256 = hashlib.sha256(listing_bytes).hexdigest()

    eligibility_bytes = eligibility_path.read_bytes()
    eligibility_sha256 = hashlib.sha256(eligibility_bytes).hexdigest()

    eligibility_data = json.loads(eligibility_bytes.decode("utf-8"))
    eligible_conditions_set = {
        cid for cid, cinfo in eligibility_data["conditions"].items()
        if cinfo.get("a1_h_eligible") is True
    }

    cells = []
    for line in listing_bytes.decode("utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("cell_id") or line.startswith("---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 9:
            cell_id = parts[0]
            filename_base = parts[1]
            study = parts[2]
            cathode = parts[3]
            temp_str = parts[5].replace("C", "")
            soc_str = parts[6].replace("%", "")
            crate_c_str = parts[7].replace("C", "")
            crate_d_str = parts[8].replace("C", "")
            
            cid = f"{cathode}_{soc_str}_{temp_str}C_{crate_c_str}-{crate_d_str}C"
            
            cells.append({
                "cell_id": cell_id,
                "filename_base": filename_base,
                "condition_id": cid,
                "cathode": cathode,
                "temperature_C": temp_str,
                "soc_range": soc_str,
                "crate_c": crate_c_str,
                "crate_d": crate_d_str
            })

    required_cells = []
    for c in cells:
        if c["condition_id"] in eligible_conditions_set:
            required_cells.append({
                "cell_id": c["cell_id"],
                "filename_base": c["filename_base"],
                "condition_id": c["condition_id"],
                "chemistry": c["cathode"]
            })

    eligible_conditions_found = sorted(list({c["condition_id"] for c in required_cells}))

    manifest = {
        "artifact": "a1_h_required_inputs",
        "description": "Mechanical enumeration of required cell telemetry inputs for Target A1-H verification.",
        "source_lineage": {
            "raw_listing_file": "evidence/l0/raw_listing.txt",
            "raw_listing_sha256": listing_sha256,
            "eligibility_manifest_file": "artifacts/a1_h_eligibility_manifest.json",
            "eligibility_manifest_sha256": eligibility_sha256
        },
        "required_condition_count": len(eligible_conditions_found),
        "required_cell_count": len(required_cells),
        "required_conditions": eligible_conditions_found,
        "required_cells": required_cells
    }

    manifest_text = json.dumps(manifest, indent=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(manifest_text, encoding="utf-8")

    manifest_sha256 = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()

    print("===================================================================")
    print(" TARGET A1-H REQUIRED INPUTS GENERATOR OUTPUT")
    print("===================================================================")
    print("Source raw_listing.txt SHA256:        ", listing_sha256)
    print("Source a1_h_eligibility_manifest SHA: ", eligibility_sha256)
    print("Required Condition Count (derived):    ", len(eligible_conditions_found))
    print("Required Cell Count (derived):         ", len(required_cells))
    print("Generated Manifest SHA256:            ", manifest_sha256)
    print("-------------------------------------------------------------------")
    print("Enumerated Required Cells:")
    for idx, rc in enumerate(required_cells, 1):
        print("  [{:2d}] Cell ID: {} | Condition: {}".format(idx, rc["cell_id"], rc["condition_id"]))
    print("-------------------------------------------------------------------")
    print("Conditions Breakdown:")
    for cond in eligible_conditions_found:
        c_cells = [rc["cell_id"] for rc in required_cells if rc["condition_id"] == cond]
        print("  * {}: {} cells -> {}".format(cond, len(c_cells), c_cells))
    print("===================================================================")

if __name__ == "__main__":
    main()
