#!/usr/bin/env python3
"""
Generate reproducible cell listing from captured BatteryArchive metadata.
Source: evidence/l0/source_pages/batteryarchive_metadata.csv
Output: evidence/l0/raw_listing.txt
"""

import csv
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    l0_dir = script_dir.parent
    meta_csv = l0_dir / "source_pages/batteryarchive_metadata.csv"
    out_txt = l0_dir / "raw_listing.txt"

    with open(meta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    snl_cells = [r for r in rows if r.get("study", "").lower() == "snl" or r.get("cell_id", "").startswith("SNL_")]

    with open(out_txt, "w", encoding="utf-8") as out:
        out.write("# BatteryArchive.org SNL (Sandia National Laboratories) Cell Inventory\n")
        out.write("# Generated from: evidence/l0/source_pages/batteryarchive_metadata.csv\n")
        out.write(f"# Total SNL Cells: {len(snl_cells)}\n")
        out.write("#\n")
        out.write("# Note on File Naming Standard:\n")
        out.write("# Database Cell ID contains '/' in charge/discharge rate (e.g. SNL_18650_LFP_25C_0-100_0.5/1C_a).\n")
        out.write("# Filesystem Filename Base converts '/' to '-' (e.g. SNL_18650_LFP_25C_0-100_0.5-1C_a)\n")
        out.write("# per BatteryArchive data_transfer.py:L135 (file_name = cell_id.replace('/', '-'))\n")
        out.write("#\n")
        out.write("cell_id | filename_base | study | cathode | anode | temp_C | soc_range | crate_c | crate_d | cap_ah | form_factor\n")
        out.write("--------|---------------|-------|---------|-------|--------|-----------|---------|---------|--------|------------\n")
        for r in sorted(snl_cells, key=lambda x: x["cell_id"]):
            cid = r["cell_id"]
            fname_base = cid.replace("/", "-")
            out.write(f"{cid} | {fname_base} | {r['study']} | {r['cathode']} | {r['anode']} | {r['temperature']}C | {r['min_soc']}-{r['max_soc']}% | {r['charge_crate']}C | {r['discharge_crate']}C | {r['capacity_ah']}Ah | {r['form_factor']}\n")

    print(f"Successfully generated {out_txt} with {len(snl_cells)} entries.")

if __name__ == "__main__":
    main()
