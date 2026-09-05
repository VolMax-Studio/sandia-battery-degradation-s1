#!/usr/bin/env python3
"""
Ultra-Simple 2-Step Figure 2a Digitizer
No 33 prompts. No pressing Enter after each marker.

Workflow:
Step 1: 4 Calibration clicks (Axis ticks).
Step 2: Click ALL '+' (krstiće) on the whole image. Press ENTER once when done.
Step 3: Click the TOP of each bar (vrh svakog stubića) from left to right. Press ENTER once when done.
The script automatically matches every '+' to its bar and generates the reference tables!
"""

import sys
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Ultra-Simple Human Digitization for Figure 2a")
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
    print(" Figure 2a Fast Digitizer (Ultra-Simple 2-Step Mode)")
    print(f" Operator: {args.operator}")
    print(f" Image:    {img_path.name}")
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

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.imshow(img)
    plt.tight_layout()

    # --- STEP 1: KALIBRACIJA (4 KLIKA) ---
    print(">>> 1. KALIBRACIJA OSA (samo 4 klika):")
    
    ax.set_title("1/4: Klikni na y=0 liniju VELIKOG (LFP) grafikona", fontsize=12, color="blue", fontweight="bold")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    lfp_y0 = pts[0][1]
    ax.axhline(lfp_y0, color="cyan", linestyle="--", alpha=0.7)
    print(f"  [OK] LFP y=0 tick: {lfp_y0:.1f} px")

    ax.set_title("2/4: Klikni na y=10,000 liniju VELIKOG (LFP) grafikona", fontsize=12, color="blue", fontweight="bold")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    lfp_ytop = pts[0][1]
    ax.axhline(lfp_ytop, color="cyan", linestyle="--", alpha=0.7)
    print(f"  [OK] LFP y=10,000 tick: {lfp_ytop:.1f} px")

    ax.set_title("3/4: Klikni na y=0 liniju MALOG (Inset) grafikona", fontsize=12, color="magenta", fontweight="bold")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    inset_y0 = pts[0][1]
    ax.axhline(inset_y0, color="magenta", linestyle="--", alpha=0.7)
    print(f"  [OK] Inset y=0 tick: {inset_y0:.1f} px")

    ax.set_title("4/4: Klikni na y=3,000 liniju MALOG (Inset) grafikona", fontsize=12, color="magenta", fontweight="bold")
    plt.draw()
    pts = plt.ginput(1, timeout=-1)
    inset_ytop = pts[0][1]
    ax.axhline(inset_ytop, color="magenta", linestyle="--", alpha=0.7)
    print(f"  [OK] Inset y=3,000 tick: {inset_ytop:.1f} px")

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

    # --- STEP 2: SVI KRSTIĆI ODJEDNOM ---
    print("\n>>> 2. KLIKNI SVE KRSTIĆE (+) NA CELOJ SLICI:")
    print("  - Samo klikći redom na svaki krstić (+) koji vidiš.")
    print("  - Kad isklikćeš SVE krstiće, pritisni ENTER samo JEDANPUT.")
    
    ax.set_title("KORAK 2: Klikni SVE krstiće (+) na celoj slici. Kad završiš, pritisni ENTER.", fontsize=13, color="darkgreen", fontweight="bold")
    plt.draw()
    
    all_marker_pts = plt.ginput(-1, timeout=-1)
    if all_marker_pts is None:
        all_marker_pts = []
    
    for p in all_marker_pts:
        ax.plot(p[0], p[1], 'ro', markersize=5)
    plt.draw()
    print(f"  [OK] Ukupno zabeleženo {len(all_marker_pts)} krstića!")

    # --- STEP 3: SVI VRHOVI STUBIĆA ODJEDNOM ---
    print("\n>>> 3. KLIKNI VRHOVE STUBIĆA S LEVA NA DESNO:")
    print("  - Klikni na vrh svakog stubića (bar) s leva na desno (12 LFP na velikom, pa 12 NMC i 9 NCA na malom).")
    print("  - Kad isklikćeš sve vrhove stubića, pritisni ENTER samo JEDANPUT.")
    
    ax.set_title("KORAK 3: Klikni VRHOVE STUBIĆA (s leva na desno). Kad završiš, pritisni ENTER.", fontsize=13, color="navy", fontweight="bold")
    plt.draw()
    
    all_bar_pts = plt.ginput(-1, timeout=-1)
    if all_bar_pts is None:
        all_bar_pts = []
    
    for p in all_bar_pts:
        ax.plot(p[0], p[1], 'bs', markersize=6)
    plt.draw()
    print(f"  [OK] Ukupno zabeleženo {len(all_bar_pts)} vrhova stubića!")

    plt.close(fig)

    # Sort bar clicks from left to right (by x)
    sorted_bars = sorted(all_bar_pts, key=lambda p: p[0])

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

    # Map markers to closest bar by x-coordinate
    conditions_output = {}
    num_bars = len(sorted_bars)
    print(f"\nProcessing {num_bars} bars against {len(conditions)} conditions...")

    for i, cond in enumerate(conditions):
        cid = cond["condition_id"]
        chem = cond["chemistry"]
        rep = cond["replicate_count_metadata"]
        
        if i < len(sorted_bars):
            bar_pt = sorted_bars[i]
            bar_top = {"x_px": round(bar_pt[0], 2), "y_px": round(bar_pt[1], 2)}
        else:
            bar_top = {"x_px": 0.0, "y_px": lfp_y0 if chem == "LFP" else inset_y0}

        # Find markers within horizontal reach of this bar
        bar_x = bar_top["x_px"]
        assigned_markers = []
        
        if num_bars > 1 and bar_x > 0:
            # Half-distance to adjacent bars
            left_bound = (sorted_bars[i-1][0] + bar_x) / 2.0 if i > 0 else bar_x - 30.0
            right_bound = (sorted_bars[i+1][0] + bar_x) / 2.0 if i < num_bars - 1 else bar_x + 30.0
            
            for m in all_marker_pts:
                if left_bound <= m[0] <= right_bound:
                    assigned_markers.append({"x_px": round(m[0], 2), "y_px": round(m[1], 2)})
        
        visual_class = "MEASURED_PRESENT" if len(assigned_markers) > 0 else "EXTRAPOLATED_ONLY"

        conditions_output[cid] = {
            "condition_id": cid,
            "chemistry": chem,
            "temperature_C": cond["temperature_C"],
            "soc_min": cond["soc_min"],
            "soc_max": cond["soc_max"],
            "charge_C": cond["charge_C"],
            "discharge_C": cond["discharge_C"],
            "replicate_count_metadata": rep,
            "raw_markers_px": assigned_markers,
            "bar_top_px": bar_top,
            "visual_assessment": visual_class
        }
        print(f"  [{i+1}/33] {cid}: {len(assigned_markers)} markers assigned, bar_y = {bar_top['y_px']}")

    # Save raw pixel clicks JSON
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
    print(f"USPEH: Sirovi pikseli sačuvani u {raw_json_path}")
    print(f"===================================================================")

    # Run deterministic transformer
    print("\nPokrećem automatski proračun (pixel_to_efc.py)...")
    trans_script = repo_root / "evidence" / "l0" / "scripts" / "pixel_to_efc.py"
    res = subprocess.run([sys.executable, str(trans_script)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"ERROR: {res.stderr}")

if __name__ == "__main__":
    main()
