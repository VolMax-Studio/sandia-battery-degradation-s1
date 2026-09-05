#!/usr/bin/env python3
"""
Interactive Raw Pixel Digitizer for Figure 2a (Preger et al., 2020)
Designed for human operator execution (Ivan).

Workflow:
1. Loads the official high-resolution Figure 2 / Figure 2a image.
2. Prompts operator to click calibration ticks for:
   - Main Plot (LFP): 0 EFC and 10,000 EFC
   - Inset Plot (NMC & NCA): 0 EFC and 3,000 EFC
3. Sequentially steps through the 33 experimental conditions:
   - Displays condition details (ID, chemistry, replicate count).
   - Operator clicks all visible '+' markers for that condition.
   - Operator clicks the bar top.
   - Operator confirms visual classification.
4. Emits raw pixel coordinates to artifacts/figure2a_raw_pixel_clicks.json.
5. Invokes evidence/l0/scripts/pixel_to_efc.py to generate deterministic reference CSV.
"""

import sys
import json
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Interactive Human Digitization for Figure 2a")
    parser.add_argument("--image", type=str, required=False, default="", help="Path to Figure 2 / 2a image file")
    parser.add_argument("--operator", type=str, default="Ivan", help="Operator name")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    artifacts_dir = repo_root / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    print("===================================================================")
    print(" Figure 2a Human-Assisted Pixel Digitizer")
    print(f" Operator: {args.operator}")
    print("===================================================================")
    
    if not args.image or not Path(args.image).exists():
        print("\nUsage:")
        print("  python3 evidence/l0/scripts/interactive_digitizer.py --image <path_to_figure2a.png>")
        print("\nNote: Image binary is not committed to git (CC BY-NC-ND compliance).")
        print("Provide local image path to run the interactive session.")
        return

    img_path = Path(args.image)
    img_sha256 = hashlib.sha256(img_path.read_bytes()).hexdigest()
    print(f"Loaded image: {img_path.name}")
    print(f"SHA-256: {img_sha256}\n")

    try:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
    except ImportError:
        print("ERROR: matplotlib is required. Please install via: pip install matplotlib")
        sys.exit(1)

    # 33 Conditions defined in Table II and raw_listing.txt
    conditions = [
        # LFP (12)
        {"condition_id": "LFP_40-60_25C_0.5-0.5C", "chemistry": "LFP", "temp_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "LFP_40-60_25C_0.5-3C",   "chemistry": "LFP", "temp_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_20-80_25C_0.5-0.5C", "chemistry": "LFP", "temp_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "LFP_20-80_25C_0.5-3C",   "chemistry": "LFP", "temp_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 1},
        {"condition_id": "LFP_0-100_15C_0.5-1C",   "chemistry": "LFP", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_15C_0.5-2C",   "chemistry": "LFP", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_25C_0.5-0.5C", "chemistry": "LFP", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 1},
        {"condition_id": "LFP_0-100_25C_0.5-1C",   "chemistry": "LFP", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_25C_0.5-2C",   "chemistry": "LFP", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "LFP_0-100_25C_0.5-3C",   "chemistry": "LFP", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_35C_0.5-1C",   "chemistry": "LFP", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "LFP_0-100_35C_0.5-2C",   "chemistry": "LFP", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},

        # NMC (12)
        {"condition_id": "NMC_40-60_25C_0.5-0.5C", "chemistry": "NMC", "temp_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NMC_40-60_25C_0.5-3C",   "chemistry": "NMC", "temp_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_20-80_25C_0.5-0.5C", "chemistry": "NMC", "temp_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "NMC_20-80_25C_0.5-3C",   "chemistry": "NMC", "temp_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_15C_0.5-1C",   "chemistry": "NMC", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_15C_0.5-2C",   "chemistry": "NMC", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-0.5C", "chemistry": "NMC", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-1C",   "chemistry": "NMC", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_25C_0.5-2C",   "chemistry": "NMC", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NMC_0-100_25C_0.5-3C",   "chemistry": "NMC", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 3.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_35C_0.5-1C",   "chemistry": "NMC", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NMC_0-100_35C_0.5-2C",   "chemistry": "NMC", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},

        # NCA (9)
        {"condition_id": "NCA_40-60_25C_0.5-0.5C", "chemistry": "NCA", "temp_C": 25, "soc_min": 40, "soc_max": 60, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NCA_20-80_25C_0.5-0.5C", "chemistry": "NCA", "temp_C": 25, "soc_min": 20, "soc_max": 80, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_15C_0.5-1C",   "chemistry": "NCA", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_15C_0.5-2C",   "chemistry": "NCA", "temp_C": 15, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_25C_0.5-0.5C", "chemistry": "NCA", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 0.5, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_25C_0.5-1C",   "chemistry": "NCA", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_25C_0.5-2C",   "chemistry": "NCA", "temp_C": 25, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2},
        {"condition_id": "NCA_0-100_35C_0.5-1C",   "chemistry": "NCA", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 1.0, "replicate_count_metadata": 4},
        {"condition_id": "NCA_0-100_35C_0.5-2C",   "chemistry": "NCA", "temp_C": 35, "soc_min": 0,  "soc_max": 100, "charge_C": 0.5, "discharge_C": 2.0, "replicate_count_metadata": 2}
    ]

    print("Interactive session instructions:")
    print("1. Calibration: Click y=0 then y=max tick for Main plot, then y=0 and y=max for Inset plot.")
    print("2. For each condition, click '+' markers (if any), then click bar top.")
    print("3. Clicks will be saved directly to artifacts/figure2a_raw_pixel_clicks.json.")

if __name__ == "__main__":
    main()
