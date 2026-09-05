#!/usr/bin/env python3
"""
Figure 2a Guided Precision Digitizer (Sandia Degradation S1)
Operator: Ivan

Features:
- Step 1: 4 Calibration clicks (LFP 0/10k, Inset 0/3k).
- Step 2: Guided walkthrough over conditions with auto-zoom on the active bar section.
- Left-click: Add marker (+).
- Right-click: Undo / remove last marker.
- Space / Enter: Advance to next bar.
- 'b': Go back to previous bar.
- 's': Skip condition (mark 0 markers / extrapolated).
- Fully tagged raw output: every click has condition_id and plot ('main' or 'inset').
- Zero heuristics, zero fake bar tops, zero dropped clicks.
"""

import sys
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

CONDITIONS = [
    # --- LFP (Main Plot, 12 conditions) ---
    {"condition_id": "LFP_40-60_25C_0.5-0.5C", "chemistry": "LFP", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "main", "rep": 2, "default_extrap": True, "zoom": (50, 500, 0, 1000)},
    {"condition_id": "LFP_40-60_25C_0.5-3C",   "chemistry": "LFP", "temp": "25C", "soc": "40-60%", "rate": "0.5-3C",   "plot": "main", "rep": 2, "default_extrap": True, "zoom": (50, 500, 0, 1000)},
    {"condition_id": "LFP_20-80_25C_0.5-0.5C", "chemistry": "LFP", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "main", "rep": 4, "default_extrap": True, "zoom": (50, 500, 0, 1000)},
    {"condition_id": "LFP_20-80_25C_0.5-3C",   "chemistry": "LFP", "temp": "25C", "soc": "20-80%", "rate": "0.5-3C",   "plot": "main", "rep": 1, "default_extrap": False, "zoom": (150, 550, 200, 850), "hint": "LFP 20-80% 3C (~2 '+' markers near 3400 EFC)"},
    {"condition_id": "LFP_0-100_15C_0.5-1C",   "chemistry": "LFP", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 2, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_15C_0.5-2C",   "chemistry": "LFP", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_25C_0.5-0.5C", "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "main", "rep": 1, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_25C_0.5-1C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 4, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_25C_0.5-2C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_25C_0.5-3C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-3C",   "plot": "main", "rep": 4, "default_extrap": False, "zoom": (250, 600, 200, 850), "hint": "LFP 0-100% 25C 3C (4 '+' markers near 2800-4000 EFC)"},
    {"condition_id": "LFP_0-100_35C_0.5-1C",   "chemistry": "LFP", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 4, "default_extrap": True, "zoom": (250, 600, 0, 1000)},
    {"condition_id": "LFP_0-100_35C_0.5-2C",   "chemistry": "LFP", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "default_extrap": True, "zoom": (250, 600, 0, 1000)},

    # --- NMC (Inset Plot, 12 conditions) ---
    {"condition_id": "NMC_40-60_25C_0.5-0.5C", "chemistry": "NMC", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (700, 1150, 200, 620), "hint": "NMC 40-60% 0.5C (solid yellow bar, ~2 '+' markers)"},
    {"condition_id": "NMC_40-60_25C_0.5-3C",   "chemistry": "NMC", "temp": "25C", "soc": "40-60%", "rate": "0.5-3C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (700, 1150, 200, 620), "hint": "NMC 40-60% 3C (hatched yellow bar, ~2 '+' markers)"},
    {"condition_id": "NMC_20-80_25C_0.5-0.5C", "chemistry": "NMC", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (700, 1150, 200, 620), "hint": "NMC 20-80% 0.5C (solid yellow bar, ~4 '+' markers)"},
    {"condition_id": "NMC_20-80_25C_0.5-3C",   "chemistry": "NMC", "temp": "25C", "soc": "20-80%", "rate": "0.5-3C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (700, 1150, 200, 620), "hint": "NMC 20-80% 3C (hatched yellow bar, ~2 '+' markers)"},
    {"condition_id": "NMC_0-100_15C_0.5-1C",   "chemistry": "NMC", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 15C 1C (blue diagonal bar, ~2 '+' markers)"},
    {"condition_id": "NMC_0-100_15C_0.5-2C",   "chemistry": "NMC", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 15C 2C (blue horizontal bar, ~2 '+' markers)"},
    {"condition_id": "NMC_0-100_25C_0.5-0.5C", "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 25C 0.5C (solid yellow bar, ~2 '+' markers)"},
    {"condition_id": "NMC_0-100_25C_0.5-1C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 25C 1C (yellow diagonal bar, ~4 '+' markers)"},
    {"condition_id": "NMC_0-100_25C_0.5-2C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 25C 2C (yellow horizontal bar, ~2 '+' markers)"},
    {"condition_id": "NMC_0-100_25C_0.5-3C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-3C",   "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 25C 3C (yellow diagonal thin bar, ~4 '+' markers)"},
    {"condition_id": "NMC_0-100_35C_0.5-1C",   "chemistry": "NMC", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 35C 1C (red diagonal bar, ~4 '+' markers)"},
    {"condition_id": "NMC_0-100_35C_0.5-2C",   "chemistry": "NMC", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (750, 1200, 350, 620), "hint": "NMC 0-100% 35C 2C (red horizontal bar, ~2 '+' markers)"},

    # --- NCA (Inset Plot, 9 conditions) ---
    {"condition_id": "NCA_40-60_25C_0.5-0.5C", "chemistry": "NCA", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1050, 1420, 200, 620), "hint": "NCA 40-60% 0.5C (solid yellow bar, ~2 '+' markers)"},
    {"condition_id": "NCA_20-80_25C_0.5-0.5C", "chemistry": "NCA", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (1050, 1420, 200, 620), "hint": "NCA 20-80% 0.5C (solid yellow bar, ~4 '+' markers)"},
    {"condition_id": "NCA_0-100_15C_0.5-1C",   "chemistry": "NCA", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 15C 1C (blue diagonal bar, ~2 '+' markers)"},
    {"condition_id": "NCA_0-100_15C_0.5-2C",   "chemistry": "NCA", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 15C 2C (blue horizontal bar, ~2 '+' markers)"},
    {"condition_id": "NCA_0-100_25C_0.5-0.5C", "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 25C 0.5C (solid yellow bar, ~2 '+' markers)"},
    {"condition_id": "NCA_0-100_25C_0.5-1C",   "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 25C 1C (yellow diagonal bar, ~4 '+' markers)"},
    {"condition_id": "NCA_0-100_25C_0.5-2C",   "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 25C 2C (yellow horizontal bar, ~2 '+' markers)"},
    {"condition_id": "NCA_0-100_35C_0.5-1C",   "chemistry": "NCA", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 35C 1C (red diagonal bar, ~4 '+' markers)"},
    {"condition_id": "NCA_0-100_35C_0.5-2C",   "chemistry": "NCA", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "default_extrap": False, "zoom": (1100, 1420, 350, 620), "hint": "NCA 0-100% 35C 2C (red horizontal bar, ~2 '+' markers)"},
]

class DigitizerApp:
    def __init__(self, img_path, operator="Ivan"):
        self.img_path = Path(img_path).resolve()
        self.operator = operator
        self.img_sha256 = hashlib.sha256(self.img_path.read_bytes()).hexdigest()
        self.img = mpimg.imread(str(self.img_path))
        self.h, self.w = self.img.shape[:2]

        # Only walk through the 23 measured conditions interactively
        # (The 10 extrapolated LFP conditions are registered automatically as 0 markers)
        self.measured_cond_indices = [i for i, c in enumerate(CONDITIONS) if not c.get("default_extrap", False)]
        self.current_step = "CALIBRATION"
        self.cal_clicks = []  # [lfp_y0, lfp_ytop, inset_y0, inset_ytop]
        self.cal_data = {}
        
        # Condition clicks dict: cid -> list of (x, y)
        self.condition_clicks = {c["condition_id"]: [] for c in CONDITIONS}
        self.current_cond_idx = 0  # index in measured_cond_indices

        self.fig, self.ax = plt.subplots(figsize=(15, 9))
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        self.plot_lines = []
        self.marker_plots = []
        self.update_view()

    def update_view(self):
        self.ax.clear()
        self.ax.imshow(self.img)

        if self.current_step == "CALIBRATION":
            self.ax.set_xlim(0, self.w)
            self.ax.set_ylim(self.h, 0)
            
            cal_prompts = [
                "[1/4] Klikni na y=0 (dno ose) VELIKOG LFP grafikona",
                "[2/4] Klikni na y=10,000 (vrh ose) VELIKOG LFP grafikona",
                "[3/4] Klikni na y=0 (dno ose) MALOG Inset grafikona",
                "[4/4] Klikni na y=3,000 (vrh ose) MALOG Inset grafikona"
            ]
            step_idx = len(self.cal_clicks)
            title = f"KALIBRACIJA OSA ({step_idx+1}/4):\n{cal_prompts[step_idx]}"
            self.ax.set_title(title, fontsize=13, color="darkblue", fontweight="bold")

            # Draw calibration lines clicked so far
            for idx, y in enumerate(self.cal_clicks):
                col = "cyan" if idx < 2 else "magenta"
                self.ax.axhline(y, color=col, linestyle="--", linewidth=1.5)

        elif self.current_step == "MEASUREMENT":
            cond_global_idx = self.measured_cond_indices[self.current_cond_idx]
            cond = CONDITIONS[cond_global_idx]
            cid = cond["condition_id"]
            clicks = self.condition_clicks[cid]

            # Set zoom for active condition
            if "zoom" in cond:
                xmin, xmax, ymin, ymax = cond["zoom"]
                self.ax.set_xlim(xmin, xmax)
                self.ax.set_ylim(ymax, ymin)
            else:
                self.ax.set_xlim(0, self.w)
                self.ax.set_ylim(self.h, 0)

            # Draw clicked markers for this condition
            for m in clicks:
                self.ax.plot(m[0], m[1], 'ro', markersize=8, markeredgecolor='black', markeredgewidth=1.5)
                self.ax.plot(m[0], m[1], 'w+', markersize=8, markeredgewidth=1.5)

            status_txt = f"[{self.current_cond_idx+1}/{len(self.measured_cond_indices)}] {cid} ({cond['plot'].upper()} Plot)\n"
            status_txt += f"Hint: {cond.get('hint', '')} | Zabeleženo: {len(clicks)} krstića\n"
            status_txt += "LEVI KLIK = Dodaj krstić | DESNI KLIK = Obriši | SPACE / ENTER = Sledeći stubić | B = Prethodni"
            self.ax.set_title(status_txt, fontsize=12, color="darkgreen", fontweight="bold")

        elif self.current_step == "FINISHED":
            self.ax.set_xlim(0, self.w)
            self.ax.set_ylim(self.h, 0)
            total_m = sum(len(m) for m in self.condition_clicks.values())
            title = f"USPEH! Isklikano {total_m} krstića za 23 stanja.\nPritisni 'S' ili zatvori prozor za snimanje i proračun."
            self.ax.set_title(title, fontsize=14, color="darkblue", fontweight="bold")

        self.fig.canvas.draw()

    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        x = round(event.xdata, 2)
        y = round(event.ydata, 2)

        if self.current_step == "CALIBRATION":
            if event.button == 1:  # Left click
                self.cal_clicks.append(y)
                print(f"Calibration click [{len(self.cal_clicks)}/4]: y = {y} px")
                if len(self.cal_clicks) == 4:
                    self.cal_data = {
                        "main_plot_lfp": {
                            "y_px_0": self.cal_clicks[0],
                            "y_px_max": self.cal_clicks[1],
                            "efc_max": 10000.0,
                            "delta_axis": 25.0
                        },
                        "inset_plot_nmc_nca": {
                            "y_px_0": self.cal_clicks[2],
                            "y_px_max": self.cal_clicks[3],
                            "efc_max": 3000.0,
                            "delta_axis": 10.0
                        }
                    }
                    self.current_step = "MEASUREMENT"
                    self.current_cond_idx = 0
                self.update_view()

        elif self.current_step == "MEASUREMENT":
            cond_global_idx = self.measured_cond_indices[self.current_cond_idx]
            cid = CONDITIONS[cond_global_idx]["condition_id"]

            if event.button == 1:  # Left click: Add marker
                self.condition_clicks[cid].append((x, y))
                print(f"  + Added marker for {cid}: ({x}, {y}) [Total: {len(self.condition_clicks[cid])}]")
                self.update_view()
            elif event.button == 3:  # Right click: Remove last marker
                if self.condition_clicks[cid]:
                    removed = self.condition_clicks[cid].pop()
                    print(f"  - Removed marker for {cid}: {removed}")
                    self.update_view()

    def on_key(self, event):
        if self.current_step == "MEASUREMENT":
            if event.key in (" ", "enter"):
                cond_global_idx = self.measured_cond_indices[self.current_cond_idx]
                cid = CONDITIONS[cond_global_idx]["condition_id"]
                print(f"Done with {cid}: {len(self.condition_clicks[cid])} markers.")
                
                if self.current_cond_idx < len(self.measured_cond_indices) - 1:
                    self.current_cond_idx += 1
                    self.update_view()
                else:
                    self.current_step = "FINISHED"
                    self.update_view()
                    self.save_and_export()
            elif event.key == "b":
                if self.current_cond_idx > 0:
                    self.current_cond_idx -= 1
                    self.update_view()
            elif event.key == "s":  # Skip / mark 0 markers
                cond_global_idx = self.measured_cond_indices[self.current_cond_idx]
                cid = CONDITIONS[cond_global_idx]["condition_id"]
                self.condition_clicks[cid] = []
                print(f"Skipped {cid} (0 markers).")
                if self.current_cond_idx < len(self.measured_cond_indices) - 1:
                    self.current_cond_idx += 1
                    self.update_view()
                else:
                    self.current_step = "FINISHED"
                    self.update_view()
                    self.save_and_export()
        elif self.current_step == "FINISHED":
            if event.key in ("s", "q", "enter"):
                plt.close(self.fig)

    def save_and_export(self):
        repo_root = Path(__file__).resolve().parents[3]
        artifacts_dir = repo_root / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        conditions_output = {}
        for cond in CONDITIONS:
            cid = cond["condition_id"]
            clicks = self.condition_clicks[cid]
            visual_class = "MEASURED_PRESENT" if len(clicks) > 0 else "EXTRAPOLATED_ONLY"
            
            # Form clean explicit marker dicts
            raw_markers = [
                {"x_px": m[0], "y_px": m[1], "plot": cond["plot"]}
                for m in clicks
            ]

            conditions_output[cid] = {
                "condition_id": cid,
                "chemistry": cond["chemistry"],
                "temperature_C": int(cond["temp"].replace("C", "")),
                "soc_min": int(cond["soc"].split("-")[0].replace("%", "")),
                "soc_max": int(cond["soc"].split("-")[1].replace("%", "")),
                "charge_C": float(cond["rate"].split("-")[0].replace("C", "")),
                "discharge_C": float(cond["rate"].split("-")[1].replace("C", "")),
                "replicate_count_metadata": cond["rep"],
                "plot_location": cond["plot"],
                "raw_markers_px": raw_markers,
                "visual_assessment": visual_class
            }

        output_payload = {
            "operator": self.operator,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_image_filename": self.img_path.name,
            "source_image_sha256": self.img_sha256,
            "axis_calibration": self.cal_data,
            "conditions": conditions_output
        }

        raw_json_path = artifacts_dir / "figure2a_raw_pixel_clicks.json"
        raw_json_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
        print("\n" + "="*70)
        print(f"USPEH: Sirovi pikseli sačuvani u: {raw_json_path}")
        print("="*70)

        # Run pixel_to_efc.py
        trans_script = repo_root / "evidence" / "l0" / "scripts" / "pixel_to_efc.py"
        res = subprocess.run([sys.executable, str(trans_script)], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"ERROR: {res.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Guided Figure 2a Precision Digitizer")
    parser.add_argument("--image", type=str, default="/tmp/figure2_crop.png", help="Path to Figure 2 image")
    parser.add_argument("--operator", type=str, default="Ivan", help="Operator name")
    args = parser.parse_args()

    app = DigitizerApp(args.image, args.operator)
    plt.show()

if __name__ == "__main__":
    main()
