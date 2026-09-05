#!/usr/bin/env python3
"""
Deterministic Optical Coordinate Transformer: Pixel Clicks -> Physical EFC Ground Truth
Reads:
  - artifacts/figure2a_raw_pixel_clicks.json (captured from interactive human digitization session)
Generates:
  - artifacts/figure2a_reference.csv
  - artifacts/reference_partition_analysis.json

Mathematical Model:
- Main plot (LFP):
    scale_lfp = efc_max / |y_px_0 - y_px_top|
    efc = scale_lfp * (y_px_0 - y_px)
- Inset plot (NMC & NCA):
    scale_inset = efc_max / |y_px_0 - y_px_top|
    efc = scale_inset * (y_px_0 - y_px)
- Uncertainty:
    tau_c = (2 * scale) + delta_axis
- Decoupled Target Resolution:
    * A2 Target Resolution: MEASURED_PRESENT vs EXTRAPOLATED_ONLY vs UNRESOLVED
    * A1 Target Resolution: EXACT_CARDINALITY_MATCH (evaluable) vs A1_REFERENCE_CARDINALITY_UNRESOLVED (overplotted/anomalous)
"""

import json
import csv
import sys
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parents[3]
    artifacts_dir = repo_root / "artifacts"
    input_path = artifacts_dir / "figure2a_raw_pixel_clicks.json"
    
    if not input_path.exists():
        print(f"ERROR: Raw pixel clicks artifact not found at {input_path}")
        print("Please execute human-assisted digitization session to generate raw pixel clicks.")
        sys.exit(1)

    raw_data = json.loads(input_path.read_text(encoding="utf-8"))
    calib = raw_data["axis_calibration"]
    
    # Calibration parameters
    lfp_cal = calib["main_plot_lfp"]
    lfp_y0 = lfp_cal["y_px_0"]
    lfp_ytop = lfp_cal["y_px_max"]
    lfp_efc_max = lfp_cal["efc_max"]
    lfp_delta_axis = lfp_cal.get("delta_axis", 25.0)
    lfp_scale = lfp_efc_max / abs(lfp_y0 - lfp_ytop)

    inset_cal = calib["inset_plot_nmc_nca"]
    inset_y0 = inset_cal["y_px_0"]
    inset_ytop = inset_cal["y_px_max"]
    inset_efc_max = inset_cal["efc_max"]
    inset_delta_axis = inset_cal.get("delta_axis", 10.0)
    inset_scale = inset_efc_max / abs(inset_y0 - inset_ytop)

    conditions_input = raw_data["conditions"]
    ref_rows = []

    for cid, cond in conditions_input.items():
        chem = cond["chemistry"]
        plot_type = "main" if chem == "LFP" else "inset"
        y0 = lfp_y0 if plot_type == "main" else inset_y0
        ytop = lfp_ytop if plot_type == "main" else inset_ytop
        efc_max = lfp_efc_max if plot_type == "main" else inset_efc_max
        scale = lfp_scale if plot_type == "main" else inset_scale
        delta_axis = lfp_delta_axis if plot_type == "main" else inset_delta_axis
        tau_c = (2.0 * scale) + delta_axis

        rep_count = cond["replicate_count_metadata"]
        raw_markers = cond.get("raw_markers_px", [])
        visual_plus_count = len(raw_markers)
        bar_top_px = cond.get("bar_top_px", {}).get("y_px", y0)
        
        # Transform pixels to physical EFC
        marker_efcs = []
        for m in raw_markers:
            y_px = m["y_px"]
            efc_val = efc_max * (y0 - y_px) / (y0 - ytop)
            marker_efcs.append(round(efc_val, 1))
        marker_efcs.sort()

        bar_efc = round(efc_max * (y0 - bar_top_px) / (y0 - ytop), 1)

        # Target A2 Ground Truth Classification
        visual_ass = cond.get("visual_assessment", "")
        if visual_ass in ("MEASURED_PRESENT", "EXTRAPOLATED_ONLY", "UNRESOLVED"):
            a2_class = visual_ass
        else:
            a2_class = "MEASURED_PRESENT" if visual_plus_count > 0 else "EXTRAPOLATED_ONLY"

        a2_status = "RESOLVED" if a2_class in ("MEASURED_PRESENT", "EXTRAPOLATED_ONLY") else "UNRESOLVED"

        # Target A1 Ground Truth Multiset Resolution
        if a2_class == "EXTRAPOLATED_ONLY":
            a1_status = "N/A_EXTRAPOLATED"
            card_status = "EXTRAPOLATED_MATCH"
        elif visual_plus_count == rep_count:
            a1_status = "EXACT_CARDINALITY_MATCH"
            card_status = "EXACT_CARDINALITY_MATCH"
        elif visual_plus_count < rep_count and visual_plus_count > 0:
            a1_status = "A1_REFERENCE_CARDINALITY_UNRESOLVED"
            card_status = "OVERPLOTTED_OR_MIXED"
        elif visual_plus_count > rep_count:
            a1_status = "A1_REFERENCE_CARDINALITY_UNRESOLVED"
            card_status = "ANOMALOUS_COUNT_EXCEEDS_METADATA"
        else:
            a1_status = "A1_REFERENCE_CARDINALITY_UNRESOLVED"
            card_status = "CARDINALITY_UNRESOLVED"

        # Spread & Power classification
        if len(marker_efcs) > 1:
            spread = round(max(marker_efcs) - min(marker_efcs), 1)
            if spread > (2.0 * tau_c):
                a1_power = "HIGH_POWER"
            elif spread > tau_c:
                a1_power = "MODERATE_POWER"
            else:
                a1_power = "LOW_POWER"
        elif len(marker_efcs) == 1:
            spread = 0.0
            a1_power = "LOW_POWER"
        else:
            spread = 0.0
            a1_power = "N/A_EXTRAPOLATED"

        ref_rows.append({
            "condition_id": cid,
            "chemistry": chem,
            "temperature_C": cond["temperature_C"],
            "soc_min": cond["soc_min"],
            "soc_max": cond["soc_max"],
            "charge_C": cond["charge_C"],
            "discharge_C": cond["discharge_C"],
            "replicate_count_metadata": rep_count,
            "visual_plus_count": visual_plus_count,
            "digitized_marker_efc": ";".join(map(str, marker_efcs)),
            "bar_efc_value": bar_efc,
            "cardinality_status": card_status,
            "a2_published_class": a2_class,
            "a2_reference_status": a2_status,
            "a1_reference_status": a1_status,
            "axis_efc_per_pixel": round(scale, 2),
            "tau_c": round(tau_c, 1),
            "within_marker_spread": spread,
            "a1_power_classification": a1_power
        })

    # Write CSV
    csv_path = artifacts_dir / "figure2a_reference.csv"
    fieldnames = list(ref_rows[0].keys())
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ref_rows)
    print(f"Generated deterministic reference CSV: {csv_path}")

if __name__ == "__main__":
    main()
