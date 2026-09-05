#!/usr/bin/env python3
"""
Mechanical Generator for Target A1-H Required Inputs Manifest
Derives canonical required cell inputs exclusively from raw_listing.txt and a1_h_eligibility_manifest.json.

Hardened with:
- 86-cell cohort parse verification (fails on unparsed/dropped rows)
- Bidirectional condition set equality assertion (assert eligible_conditions_set == set(eligible_conditions_found))
- Replicate cardinality equality assertion against eligibility manifest
- Full condition-by-condition accounting (including 0-hit ineligible conditions)
- Deterministic canonical formatting and SHA-256 computation
"""

import sys
import json
import hashlib
from pathlib import Path

def compute_sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main():
    repo_root = Path(__file__).resolve().parents[3]
    listing_path = repo_root / "evidence" / "l0" / "raw_listing.txt"
    eligibility_path = repo_root / "artifacts" / "a1_h_eligibility_manifest.json"
    output_path = repo_root / "runs" / "run-002-a1h" / "a1_h_required_inputs.json"

    if not listing_path.exists():
        print(f"ERROR: {listing_path} not found", file=sys.stderr)
        sys.exit(1)
    if not eligibility_path.exists():
        print(f"ERROR: {eligibility_path} not found", file=sys.stderr)
        sys.exit(1)

    listing_bytes = listing_path.read_bytes()
    listing_sha256 = compute_sha256_bytes(listing_bytes)

    eligibility_bytes = eligibility_path.read_bytes()
    eligibility_sha256 = compute_sha256_bytes(eligibility_bytes)

    eligibility_data = json.loads(eligibility_bytes.decode("utf-8"))
    eligible_conditions_dict = {
        cid: cinfo for cid, cinfo in eligibility_data["conditions"].items()
        if cinfo.get("a1_h_eligible") is True
    }
    eligible_conditions_set = set(eligible_conditions_dict.keys())

    # 1. Parse raw_listing.txt with exhaustive accounting
    lines = listing_bytes.decode("utf-8").splitlines()
    total_lines = len(lines)
    comment_header_lines = 0
    parsed_cells = []

    for line_idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("cell_id") or line.startswith("---"):
            comment_header_lines += 1
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 9:
            raise ValueError(f"Malformed row at line {line_idx} (expected >= 9 pipe-delimited fields): {line}")

        cell_id = parts[0]
        filename_base = parts[1]
        study = parts[2]
        cathode = parts[3]
        temp_str = parts[5].replace("C", "")
        soc_str = parts[6].replace("%", "")
        crate_c_str = parts[7].replace("C", "")
        crate_d_str = parts[8].replace("C", "")

        cid = f"{cathode}_{soc_str}_{temp_str}C_{crate_c_str}-{crate_d_str}C"

        parsed_cells.append({
            "cell_id": cell_id,
            "filename_base": filename_base,
            "condition_id": cid,
            "cathode": cathode,
            "temperature_C": temp_str,
            "soc_range": soc_str,
            "crate_c": crate_c_str,
            "crate_d": crate_d_str
        })

    total_parsed_cells = len(parsed_cells)
    if total_parsed_cells != 86:
        raise AssertionError(f"Cohort population mismatch: expected 86 SNL cells from raw_listing.txt, but parsed {total_parsed_cells}")

    # 2. Filter required cells for A1-H
    required_cells = []
    cells_by_condition = {}

    for c in parsed_cells:
        cid = c["condition_id"]
        if cid not in cells_by_condition:
            cells_by_condition[cid] = []
        cells_by_condition[cid].append(c["cell_id"])

        if cid in eligible_conditions_set:
            required_cells.append({
                "cell_id": c["cell_id"],
                "filename_base": c["filename_base"],
                "condition_id": cid,
                "chemistry": c["cathode"]
            })

    eligible_conditions_found = sorted(list({c["condition_id"] for c in required_cells}))

    # 3. Strict Assertions (G2)
    # Check A: Exact bidirectional set equality
    missing_from_found = eligible_conditions_set - set(eligible_conditions_found)
    unexpected_in_found = set(eligible_conditions_found) - eligible_conditions_set
    if missing_from_found:
        raise AssertionError(f"Silent Drop Defect: Eligible condition(s) in manifest yielded 0 cell matches: {missing_from_found}")
    if unexpected_in_found:
        raise AssertionError(f"Unexpected condition(s) matched: {unexpected_in_found}")
    assert eligible_conditions_set == set(eligible_conditions_found), "Condition set mismatch"

    # Check B: Exact cardinality match against eligibility manifest
    for cid in eligible_conditions_found:
        manifest_reps = eligible_conditions_dict[cid]["replicate_count_metadata"]
        matched_cells = [c for c in required_cells if c["condition_id"] == cid]
        matched_count = len(matched_cells)
        if matched_count != manifest_reps:
            raise AssertionError(f"Replicate mismatch for {cid}: manifest states {manifest_reps} replicates, but matched {matched_count} cells in raw_listing.txt")

    # 4. Construct Output Manifest
    manifest = {
        "artifact": "a1_h_required_inputs",
        "description": "Mechanical enumeration of required cell telemetry inputs for Target A1-H verification.",
        "generation_timestamp": "2026-09-06T00:50:00Z",
        "source_lineage": {
            "raw_listing_file": "evidence/l0/raw_listing.txt",
            "raw_listing_sha256": listing_sha256,
            "raw_listing_total_lines": total_lines,
            "raw_listing_comment_header_lines": comment_header_lines,
            "raw_listing_parsed_cells": total_parsed_cells,
            "eligibility_manifest_file": "artifacts/a1_h_eligibility_manifest.json",
            "eligibility_manifest_sha256": eligibility_sha256,
            "inherited_uncertainty_note": "Required input population is mechanically derived from the frozen digitized Figure 2a reference partition and inherits stated reference uncertainty."
        },
        "required_condition_count": len(eligible_conditions_found),
        "required_cell_count": len(required_cells),
        "required_conditions": eligible_conditions_found,
        "required_cells": required_cells
    }

    manifest_text = json.dumps(manifest, indent=2) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(manifest_text, encoding="utf-8")

    manifest_sha256 = compute_sha256_bytes(manifest_text.encode("utf-8"))

    # 5. Comprehensive Audit Report
    print("===================================================================")
    print(" TARGET A1-H REQUIRED INPUTS GENERATOR AUDIT REPORT")
    print("===================================================================")
    print("Listing Line Accounting:")
    print("  Total lines read:            ", total_lines)
    print("  Comment / header lines:      ", comment_header_lines)
    print("  Parsed cell rows:            ", total_parsed_cells, "(EXPECTED: 86 | STATUS: PASS)")
    print("-------------------------------------------------------------------")
    print("Source File Provenance:")
    print("  raw_listing.txt SHA256:      ", listing_sha256)
    print("  a1_h_eligibility SHA256:     ", eligibility_sha256)
    print("-------------------------------------------------------------------")
    print("Condition Set Reconciliation:")
    print("  Eligible conditions in manifest:   ", len(eligible_conditions_set))
    print("  Eligible conditions matched:       ", len(eligible_conditions_found))
    print("  Set equality assertion:            ", "PASS (assert eligible_conditions_set == set(eligible_conditions_found))")
    print("-------------------------------------------------------------------")
    print("Exhaustive 33-Condition Accounting (Figure 2a Population):")
    all_manifest_conditions = eligibility_data["conditions"]
    for idx, (cid, cinfo) in enumerate(all_manifest_conditions.items(), 1):
        cat = cinfo.get("eligibility_category", "UNKNOWN")
        rep_meta = cinfo.get("replicate_count_metadata", 0)
        c_cells = [rc["cell_id"] for rc in required_cells if rc["condition_id"] == cid]
        req_count = len(c_cells)
        is_elig = cinfo.get("a1_h_eligible", False)
        print(f"  [{idx:2d}/33] {cid:<26} | Cat: {cat:<32} | Meta: {rep_meta} | A1-H Req: {req_count} | Status: {'ELIGIBLE (INCLUDED)' if is_elig else 'EXCLUDED (0 REQUIRED)'}")
    print("-------------------------------------------------------------------")
    print("Enumerated Required Conditions & Cells (A1-H Cohort):")
    for cond_idx, cond in enumerate(eligible_conditions_found, 1):
        c_cells = [rc["cell_id"] for rc in required_cells if rc["condition_id"] == cond]
        manifest_rep = eligible_conditions_dict[cond]["replicate_count_metadata"]
        print("  [{}] Condition: {} | Replicates: {}/{} matched".format(cond_idx, cond, len(c_cells), manifest_rep))
        for cell_id in c_cells:
            print("      - {}".format(cell_id))
    print("-------------------------------------------------------------------")
    print("Summary Metrics:")
    print("  Total Evaluated Conditions:   ", len(all_manifest_conditions))
    print("  Ineligible Conditions (0 req):", len(all_manifest_conditions) - len(eligible_conditions_found))
    print("  Derived Required Conditions:  ", len(eligible_conditions_found))
    print("  Derived Required Cells:       ", len(required_cells))
    print("  Generated Manifest Path:      ", str(output_path.relative_to(repo_root)))
    print("  Generated Manifest SHA256:    ", manifest_sha256)
    print("===================================================================")

if __name__ == "__main__":
    main()
