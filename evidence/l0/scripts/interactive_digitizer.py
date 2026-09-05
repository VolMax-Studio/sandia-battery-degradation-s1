#!/usr/bin/env python3
"""
Interactive Raw Pixel Digitizer for Figure 2a (Preger et al., 2020)
Designed for human operator execution (Ivan).

Workflow:
1. Loads Figure 2 / 2a image.
2. Interactively collects 4 calibration ticks:
   - Main Plot (LFP): 0 EFC tick, then 10,000 EFC tick
   - Inset Plot (NMC & NCA): 0 EFC tick, then 3,000 EFC tick
3. Iterates through the 33 experimental conditions:
   - Left-click visible '+' markers (if any).
   - Press Enter or middle-click when done with markers.
   - Click the top of the bar.
   - Enter 'm' for MEASURED_PRESENT or 'e' for EXTRAPOLATED_ONLY (or default inferred).
4. Saves raw coordinates to artifacts/figure2a_raw_pixel_clicks.json.
5. Executes evidence/l0/scripts/pixel_to_efc.py to generate deterministic reference table.
"""

import sys
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Interactive Human Digitization for Figure 2a")
    parser.add_argument("--image", type=str, required=True, help="Path to Figure 2 / 2a image file")
    parser.add_argument("--operator", type=str, default="Ivan", help="Operator name")
    args = parser.parse_args()

    img_path = Path(args.image).resolve()
    if not img_path.exists():
        print(f"ERROR: Image file not found: {img_path}")
        sys.exit(1)

    repo_root = Path(__file__).resolve().parents[3]
    artifacts_dir = repo_root / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    img_sha256 = hashlib.sha256(img_path.read_bytes()).hexdigest()
    print("===================================================================")
    print(" Figure 2a Human-Assisted Raw Pixel Digitizer")
    print(f" Operator: {args.operator}")
    print(f" Image:    {img_path.name}")
    print(f" SHA-256:  {img_sha256}")
    print("===================================================================\n")

    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
    except ImportError:
        print("ERROR: matplotlib is required. Please install via: pip install matplotlib")
        sys.exit(1)

    img = mpimg.imread(str(img_path))
    h, w = img.shape[:2]

    fig, ax = plt.subplots(figsize=(14, 9))
    ax.imshow(img)
    plt.tight_layout()

    # Step 1: Calibration Clicks
    print(">>> STEP 1: AXIS CALIBRATION (4 Clicks Required)")
    
    # 1. Main y=0
    ax.set_title("CALIBRATION 1/4: Click on MAIN plot y=0 EFC tick line", fontsize=12, color="blue")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    lfp_y0 = pts[0][1]
    ax.axhline(lfp_y0, color="cyan", linestyle="--", alpha=0.7)
    print(f"  [1/4] Main Plot y=0 tick: y = {lfp_y0:.1f} px")

    # 2. Main y=10000
    ax.set_title("CALIBRATION 2/4: Click on MAIN plot y=10,000 EFC tick line", fontsize=12, color="blue")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    lfp_ytop = pts[0][1]
    ax.axhline(lfp_ytop, color="cyan", linestyle="--", alpha=0.7)
    print(f"  [2/4] Main Plot y=10,000 tick: y = {lfp_ytop:.1f} px")

    # 3. Inset y=0
    ax.set_title("CALIBRATION 3/4: Click on INSET plot y=0 EFC tick line", fontsize=12, color="magenta")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    inset_y0 = pts[0][1]
    ax.axhline(inset_y0, color="magenta", linestyle="--", alpha=0.7)
    print(f"  [3/4] Inset Plot y=0 tick: y = {inset_y0:.1f} px")

    # 4. Inset y=3000
    ax.set_title("CALIBRATION 4/4: Click on INSET plot y=3,000 EFC tick line", fontsize=12, color="magenta")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    inset_ytop = pts[0][1]
    ax.axhline(inset_ytop, color="magenta", linestyle="--", alpha=0.7)
    print(f"  [4/4] Inset Plot y=3,000 tick: y = {inset_ytop:.1f} px")

    calibration_data = {
        "main_plot_lfp": {
            "y_px_0": round(lfp_y0, 2),
            "y_px_max": round(lfp_ytop, 2),
            "efc_max": 10000.0,
            "delta_axis": 25.0
        },
        "inset_plot_nmc_nca": {
            "y_px_0": round(inset_y0, 2),
            "y_px_max": round(inset_ytop, 2),
            "efc_max": 3000.0,
            "delta_axis": 10.0
        }
    }

    # 33 Conditions defined in Table II and raw_listing.txt
    conditions = [
        # LFP (12)
        {"condition_id": "LFP_40-60_25C_0.5-0.5C", "chemistry": "LFP", "temperature_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "LFP_40-60_25C_0.5-3C",   "chemistry": "LFP", "temperature_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_20-80_25C_0.5-0.5C", "chemistry": "LFP", "temperature_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "LFP_20-80_25C_0.5-3C",   "chemistry": "LFP", "temperature_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 1},
        {"condition_id": "LFP_0-100_15C_0.5-1C",   "chemistry": "LFP", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_15C_0.5-2C",   "chemistry": "LFP", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_25C_0.5-0.5C", "chemistry": "LFP", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 1},
        {"condition_id": "LFP_0-100_25C_0.5-1C",   "chemistry": "LFP", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_25C_0.5-2C",   "chemistry": "LFP", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_25C_0.5-3C",   "chemistry": "LFP", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_35C_0.5-1C",   "chemistry": "LFP", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_35C_0.5-2C",   "chemistry": "LFP", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},

        # NMC (12)
        {"condition_id": "NMC_40-60_25C_0.5-0.5C", "chemistry": "NMC", "temperature_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NMC_40-60_25C_0.5-3C",   "chemistry": "NMC", "temperature_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_20-80_25C_0.5-0.5C", "chemistry": "NMC", "temperature_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "NMC_20-80_25C_0.5-3C",   "chemistry": "NMC", "temperature_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_15C_0.5-1C",   "chemistry": "NMC", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_15C_0.5-2C",   "chemistry": "NMC", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-0.5C", "chemistry": "NMC", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-1C",   "chemistry": "NMC", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_25C_0.5-2C",   "chemistry": "NMC", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-3C",   "chemistry": "NMC", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_35C_0.5-1C",   "chemistry": "NMC", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_35C_0.5-2C",   "chemistry": "NMC", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},

        # NCA (9)
        {"condition_id": "NCA_40-60_25C_0.5-0.5C", "chemistry": "NCA", "temperature_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NCA_20-80_25C_0.5-0.5C", "chemistry": "NCA", "temperature_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_15C_0.5-1C",   "chemistry": "NCA", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_15C_0.5-2C",   "chemistry": "NCA", "temperature_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_25C_0.5-0.5C", "chemistry": "NCA", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_25C_0.5-1C",   "chemistry": "NCA", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_25C_0.5-2C",   "chemistry": "NCA", "temperature_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_35C_0.5-1C",   "chemistry": "NCA", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_35C_0.5-2C",   "chemistry": "NCA", "temperature_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2}
    ]

    print("\n>>> STEP 2: CONDITION-BY-CONDITION DIGITIZATION (33 Conditions)")
    print("For each condition:")
    print("  1. Left-click all '+' markers on that bar.")
    print("  2. Press Enter or middle-click when done with markers (if 0 markers, just press Enter).")
    print("  3. Click once on the TOP of the condition bar.")

    conditions_output = {}

    for idx, cond in enumerate(conditions, 1):
        cid = cond["condition_id"]
        chem = cond["chemistry"]
        rep = cond["replicate_count_metadata"]
        print(f"\n--- [{idx}/33] Condition: {cid} (Metadata Replicates: {rep}) ---")
        
        # 1. Collect '+' markers
        ax.set_title(f"[{idx}/33] {cid} (reps: {rep})\nClick ALL '+' markers, then press ENTER", fontsize=11, color="darkgreen")
        plt.draw()
        
        marker_clicks = plt.ginput(-1, timeout=-1)
        raw_markers = [{"x_px": round(p[0], 2), "y_px": round(p[1], 2)} for p in marker_clicks]
        for p in marker_clicks:
            ax.plot(p[0], p[1], 'ro', markersize=4)
        plt.draw()
        print(f"  Recorded {len(raw_markers)} '+' marker clicks: {raw_markers}")

        # 2. Collect bar top
        ax.set_title(f"[{idx}/33] {cid}\nClick ONCE on the TOP of the BAR", fontsize=11, color="navy")
        plt.draw()
        bar_clicks = plt.ginput(1, timeout=-1)
        bar_top = {"x_px": round(bar_clicks[0][0], 2), "y_px": round(bar_clicks[0][1], 2)}
        ax.plot(bar_clicks[0][0], bar_clicks[0][1], 'bs', markersize=5)
        plt.draw()
        print(f"  Recorded bar top click: {bar_top}")

        # Visual assessment
        visual_class = "MEASURED_PRESENT" if len(raw_markers) > 0 else "EXTRAPOLATED_ONLY"
        
        conditions_output[cid] = {
            "condition_id": cid,
            "chemistry": chem,
            "temperature_C": cond["temperature_C"],
            "soc_min": cond["soc_min"],
            "soc_max": cond["soc_max"],
            "charge_C": cond["charge_C"],
            "discharge_C": cond["discharge_C"],
            "replicate_count_metadata": rep,
            "raw_markers_px": raw_markers,
            "bar_top_px": bar_top,
            "visual_assessment": visual_class
        }

    plt.close(fig)

    # Step 3: Save raw pixel clicks JSON
    output_payload = {
        "operator": args.operator,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_image_filename": img_path.name,
        "source_image_sha256": img_sha256,
        "axis_calibration": calibration_data,
        "conditions": conditions_output
    }

    raw_json_path = artifacts_dir / "figure2a_raw_pixel_clicks.json"
    raw_json_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    print(f"\n===================================================================")
    print(f"SUCCESS: Raw pixel clicks saved to {raw_json_path}")
    print(f"===================================================================")

    # Step 4: Run deterministic transformer
    print("\nExecuting deterministic coordinate transformer (pixel_to_efc.py)...")
    trans_script = repo_root / "evidence" / "l0" / "scripts" / "pixel_to_efc.py"
    res = subprocess.run([sys.executable, str(trans_script)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"ERROR running pixel_to_efc.py: {res.stderr}")

if __name__ == "__main__":
    main()
