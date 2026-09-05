#!/usr/bin/env python3
"""
Tkinter Visual Guided Digitizer for Figure 2a
Operator: Ivan

Features:
- Native GUI with big clickable buttons (Next, Prev, Clear, Save).
- Interactive condition list on the left with live marker counters.
- Visual highlighting of the active bar region on the image.
- Left-click to place marker (+), Right-click to remove marker.
- Pre-calibrated axes from Ivan's measurements.
- 100% deterministic, zero heuristics, zero fake bar tops, zero dropped clicks.
"""

import sys
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw

CONDITIONS = [
    # --- LFP (Main Plot, 12 conditions) ---
    {"condition_id": "LFP_40-60_25C_0.5-0.5C", "name": "LFP 40-60% 25C 0.5C", "chemistry": "LFP", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_40-60_25C_0.5-3C",   "name": "LFP 40-60% 25C 3C",   "chemistry": "LFP", "temp": "25C", "soc": "40-60%", "rate": "0.5-3C",   "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_20-80_25C_0.5-0.5C", "name": "LFP 20-80% 25C 0.5C", "chemistry": "LFP", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "main", "rep": 4, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_20-80_25C_0.5-3C",   "name": "LFP 20-80% 25C 3C",   "chemistry": "LFP", "temp": "25C", "soc": "20-80%", "rate": "0.5-3C",   "plot": "main", "rep": 1, "extrap": False, "bbox": (240, 480, 310, 800), "hint": "Veliki grafikon: 20-80% 3C stubić (~2 krstića oko 3400 EFC)"},
    {"condition_id": "LFP_0-100_15C_0.5-1C",   "name": "LFP 0-100% 15C 1C",   "chemistry": "LFP", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_15C_0.5-2C",   "name": "LFP 0-100% 15C 2C",   "chemistry": "LFP", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_25C_0.5-0.5C", "name": "LFP 0-100% 25C 0.5C", "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "main", "rep": 1, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_25C_0.5-1C",   "name": "LFP 0-100% 25C 1C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 4, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_25C_0.5-2C",   "name": "LFP 0-100% 25C 2C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_25C_0.5-3C",   "name": "LFP 0-100% 25C 3C",   "chemistry": "LFP", "temp": "25C", "soc": "0-100%", "rate": "0.5-3C",   "plot": "main", "rep": 4, "extrap": False, "bbox": (430, 440, 500, 800), "hint": "Veliki grafikon: 0-100% 25C 3C stubić (4 krstića oko 2800-4000 EFC)"},
    {"condition_id": "LFP_0-100_35C_0.5-1C",   "name": "LFP 0-100% 35C 1C",   "chemistry": "LFP", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "main", "rep": 4, "extrap": True, "bbox": (0, 0, 0, 0)},
    {"condition_id": "LFP_0-100_35C_0.5-2C",   "name": "LFP 0-100% 35C 2C",   "chemistry": "LFP", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "main", "rep": 2, "extrap": True, "bbox": (0, 0, 0, 0)},

    # --- NMC (Inset Plot, 12 conditions) ---
    {"condition_id": "NMC_40-60_25C_0.5-0.5C", "name": "NMC 40-60% 25C 0.5C", "chemistry": "NMC", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "extrap": False, "bbox": (540, 270, 590, 600), "hint": "Inset: NMC 40-60% 0.5C žuti puni stubić (~2 krstića oko 2150 EFC)"},
    {"condition_id": "NMC_40-60_25C_0.5-3C",   "name": "NMC 40-60% 25C 3C",   "chemistry": "NMC", "temp": "25C", "soc": "40-60%", "rate": "0.5-3C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (585, 220, 635, 600), "hint": "Inset: NMC 40-60% 3C žuti šrafirani stubić (~2 krstića oko 2550 EFC)"},
    {"condition_id": "NMC_20-80_25C_0.5-0.5C", "name": "NMC 20-80% 25C 0.5C", "chemistry": "NMC", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "inset", "rep": 4, "extrap": False, "bbox": (630, 310, 680, 600), "hint": "Inset: NMC 20-80% 0.5C žuti puni stubić (~4 krstića oko 800-2150 EFC)"},
    {"condition_id": "NMC_20-80_25C_0.5-3C",   "name": "NMC 20-80% 25C 3C",   "chemistry": "NMC", "temp": "25C", "soc": "20-80%", "rate": "0.5-3C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (675, 340, 725, 600), "hint": "Inset: NMC 20-80% 3C žuti šrafirani stubić (~2 krstića oko 850-1750 EFC)"},
    {"condition_id": "NMC_0-100_15C_0.5-1C",   "name": "NMC 0-100% 15C 1C",   "chemistry": "NMC", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (720, 520, 755, 600), "hint": "Inset: NMC 0-100% 15C 1C plavi kosi stubić (~2 krstića pri dnu)"},
    {"condition_id": "NMC_0-100_15C_0.5-2C",   "name": "NMC 0-100% 15C 2C",   "chemistry": "NMC", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (750, 520, 785, 600), "hint": "Inset: NMC 0-100% 15C 2C plavi vodoravni stubić (~2 krstića pri dnu)"},
    {"condition_id": "NMC_0-100_25C_0.5-0.5C", "name": "NMC 0-100% 25C 0.5C", "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "extrap": False, "bbox": (780, 500, 815, 600), "hint": "Inset: NMC 0-100% 25C 0.5C žuti puni stubić (~2 krstića oko 450 EFC)"},
    {"condition_id": "NMC_0-100_25C_0.5-1C",   "name": "NMC 0-100% 25C 1C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "extrap": False, "bbox": (810, 480, 845, 600), "hint": "Inset: NMC 0-100% 25C 1C žuti kosi stubić (~4 krstića oko 400-600 EFC)"},
    {"condition_id": "NMC_0-100_25C_0.5-2C",   "name": "NMC 0-100% 25C 2C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (840, 420, 875, 600), "hint": "Inset: NMC 0-100% 25C 2C žuti vodoravni stubić (~2 krstića oko 650-1050 EFC)"},
    {"condition_id": "NMC_0-100_25C_0.5-3C",   "name": "NMC 0-100% 25C 3C",   "chemistry": "NMC", "temp": "25C", "soc": "0-100%", "rate": "0.5-3C",   "plot": "inset", "rep": 4, "extrap": False, "bbox": (870, 490, 905, 600), "hint": "Inset: NMC 0-100% 25C 3C žuti tanki šrafirani stubić (~4 krstića oko 500-620 EFC)"},
    {"condition_id": "NMC_0-100_35C_0.5-1C",   "name": "NMC 0-100% 35C 1C",   "chemistry": "NMC", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "extrap": False, "bbox": (900, 480, 935, 600), "hint": "Inset: NMC 0-100% 35C 1C crveni kosi stubić (~4 krstića oko 600-660 EFC)"},
    {"condition_id": "NMC_0-100_35C_0.5-2C",   "name": "NMC 0-100% 35C 2C",   "chemistry": "NMC", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (930, 480, 965, 600), "hint": "Inset: NMC 0-100% 35C 2C crveni vodoravni stubić (~2 krstića oko 650 EFC)"},

    # --- NCA (Inset Plot, 9 conditions) ---
    {"condition_id": "NCA_40-60_25C_0.5-0.5C", "name": "NCA 40-60% 25C 0.5C", "chemistry": "NCA", "temp": "25C", "soc": "40-60%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "extrap": False, "bbox": (985, 360, 1030, 600), "hint": "Inset: NCA 40-60% 0.5C žuti puni stubić (~2 krstića oko 1450-1600 EFC)"},
    {"condition_id": "NCA_20-80_25C_0.5-0.5C", "name": "NCA 20-80% 25C 0.5C", "chemistry": "NCA", "temp": "25C", "soc": "20-80%", "rate": "0.5-0.5C", "plot": "inset", "rep": 4, "extrap": False, "bbox": (1035, 480, 1080, 600), "hint": "Inset: NCA 20-80% 0.5C žuti puni stubić (~4 krstića oko 650 EFC)"},
    {"condition_id": "NCA_0-100_15C_0.5-1C",   "name": "NCA 0-100% 15C 1C",   "chemistry": "NCA", "temp": "15C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (1095, 480, 1130, 600), "hint": "Inset: NCA 0-100% 15C 1C plavi kosi stubić (~2 krstića oko 450-600 EFC)"},
    {"condition_id": "NCA_0-100_15C_0.5-2C",   "name": "NCA 0-100% 15C 2C",   "chemistry": "NCA", "temp": "15C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (1125, 490, 1160, 600), "hint": "Inset: NCA 0-100% 15C 2C plavi vodoravni stubić (~2 krstića oko 500 EFC)"},
    {"condition_id": "NCA_0-100_25C_0.5-0.5C", "name": "NCA 0-100% 25C 0.5C", "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-0.5C", "plot": "inset", "rep": 2, "extrap": False, "bbox": (1155, 540, 1190, 600), "hint": "Inset: NCA 0-100% 25C 0.5C žuti puni stubić (~2 krstića oko 240 EFC)"},
    {"condition_id": "NCA_0-100_25C_0.5-1C",   "name": "NCA 0-100% 25C 1C",   "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "extrap": False, "bbox": (1185, 500, 1220, 600), "hint": "Inset: NCA 0-100% 25C 1C žuti kosi stubić (~4 krstića oko 400-500 EFC)"},
    {"condition_id": "NCA_0-100_25C_0.5-2C",   "name": "NCA 0-100% 25C 2C",   "chemistry": "NCA", "temp": "25C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (1215, 490, 1250, 600), "hint": "Inset: NCA 0-100% 25C 2C žuti vodoravni stubić (~2 krstića oko 550 EFC)"},
    {"condition_id": "NCA_0-100_35C_0.5-1C",   "name": "NCA 0-100% 35C 1C",   "chemistry": "NCA", "temp": "35C", "soc": "0-100%", "rate": "0.5-1C",   "plot": "inset", "rep": 4, "extrap": False, "bbox": (1245, 510, 1280, 600), "hint": "Inset: NCA 0-100% 35C 1C crveni kosi stubić (~4 krstića oko 400-460 EFC)"},
    {"condition_id": "NCA_0-100_35C_0.5-2C",   "name": "NCA 0-100% 35C 2C",   "chemistry": "NCA", "temp": "35C", "soc": "0-100%", "rate": "0.5-2C",   "plot": "inset", "rep": 2, "extrap": False, "bbox": (1275, 490, 1310, 600), "hint": "Inset: NCA 0-100% 35C 2C crveni vodoravni stubić (~2 krstića oko 580 EFC)"},
]

class DigitizerGUI:
    def __init__(self, root, img_path, operator="Ivan"):
        self.root = root
        self.root.title("Figure 2a Precision Guided Digitizer (Ivan)")
        self.root.geometry("1450x920")

        self.img_path = Path(img_path).resolve()
        self.operator = operator
        self.img_sha256 = hashlib.sha256(self.img_path.read_bytes()).hexdigest()
        
        # Load and prepare image
        self.orig_img = Image.open(self.img_path)
        self.orig_w, self.orig_h = self.orig_img.size
        
        # Scale for display
        self.display_scale = 0.85
        self.disp_w = int(self.orig_w * self.display_scale)
        self.disp_h = int(self.orig_h * self.display_scale)
        self.scaled_img = self.orig_img.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        
        # Calibration defaults from Ivan's measurements
        self.cal_data = {
            "main_plot_lfp": {
                "y_px_0": 781.0,
                "y_px_max": 6.5,
                "efc_max": 10000.0,
                "delta_axis": 25.0
            },
            "inset_plot_nmc_nca": {
                "y_px_0": 592.2,
                "y_px_max": 216.8,
                "efc_max": 3000.0,
                "delta_axis": 10.0
            }
        }

        # Measured conditions
        self.measured_conds = [c for c in CONDITIONS if not c.get("extrap", False)]
        self.current_idx = 0
        
        # Dict: cid -> list of (x_orig, y_orig)
        self.clicks = {c["condition_id"]: [] for c in CONDITIONS}

        self.setup_ui()
        self.select_condition(0)

    def setup_ui(self):
        # Top Banner
        top_frame = tk.Frame(self.root, bg="#1a237e", pady=10)
        top_frame.pack(fill=tk.X)

        self.title_lbl = tk.Label(top_frame, text="", font=("Helvetica", 14, "bold"), fg="white", bg="#1a237e")
        self.title_lbl.pack()
        self.hint_lbl = tk.Label(top_frame, text="", font=("Helvetica", 11, "italic"), fg="#ffeb3b", bg="#1a237e")
        self.hint_lbl.pack()

        # Main horizontal paned window
        main_paned = tk.Frame(self.root)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel: Condition list
        left_frame = tk.Frame(main_paned, width=320, bg="#f5f5f5")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(left_frame, text="23 Merena Stanja", font=("Helvetica", 12, "bold"), bg="#f5f5f5").pack(pady=5)
        
        # Listbox with scrollbar
        list_scroll = tk.Scrollbar(left_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cond_listbox = tk.Listbox(left_frame, yscrollcommand=list_scroll.set, font=("Courier", 10), width=35, height=30)
        self.cond_listbox.pack(fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.cond_listbox.yview)
        self.cond_listbox.bind('<<ListboxSelect>>', self.on_list_select)

        # Right panel: Image Canvas + Controls
        right_frame = tk.Frame(main_paned)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right_frame, width=self.disp_w, height=self.disp_h, bg="#333", cursor="crosshair")
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

        # Bottom Control Buttons
        btn_frame = tk.Frame(self.root, bg="#eeeeee", pady=10)
        btn_frame.pack(fill=tk.X)

        self.btn_prev = tk.Button(btn_frame, text="◀ PRETHODNI STUBIĆ (B)", font=("Helvetica", 11, "bold"), bg="#cfd8dc", padx=15, pady=8, command=self.prev_condition)
        self.btn_prev.pack(side=tk.LEFT, padx=15)

        self.btn_clear = tk.Button(btn_frame, text="✖ Obriši klikove za ovaj stubić", font=("Helvetica", 10), bg="#ffcdd2", fg="#b71c1c", padx=10, pady=8, command=self.clear_current)
        self.btn_clear.pack(side=tk.LEFT, padx=10)

        self.status_bar_lbl = tk.Label(btn_frame, text="", font=("Helvetica", 11, "bold"), bg="#eeeeee")
        self.status_bar_lbl.pack(side=tk.LEFT, padx=20)

        self.btn_save = tk.Button(btn_frame, text="💾 SNIMI I ZAVRŠI SVE", font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white", padx=20, pady=8, command=self.save_and_finish)
        self.btn_save.pack(side=tk.RIGHT, padx=15)

        self.btn_next = tk.Button(btn_frame, text="SLEDEĆI STUBIĆ ▶ (SPACE)", font=("Helvetica", 11, "bold"), bg="#2196f3", fg="white", padx=20, pady=8, command=self.next_condition)
        self.btn_next.pack(side=tk.RIGHT, padx=10)

        # Keyboard bindings
        self.root.bind("<space>", lambda e: self.next_condition())
        self.root.bind("<Return>", lambda e: self.next_condition())
        self.root.bind("<b>", lambda e: self.prev_condition())
        self.root.bind("<B>", lambda e: self.prev_condition())

        self.refresh_listbox()

    def refresh_listbox(self):
        self.cond_listbox.delete(0, tk.END)
        for i, c in enumerate(self.measured_conds):
            cid = c["condition_id"]
            cnt = len(self.clicks[cid])
            mark = f"[{cnt} +]" if cnt > 0 else "[  0  ]"
            txt = f"{i+1:2d}. {mark} {c['name']}"
            self.cond_listbox.insert(tk.END, txt)
            if cnt > 0:
                self.cond_listbox.itemconfig(i, {'bg': '#e8f5e9'})

    def select_condition(self, idx):
        if 0 <= idx < len(self.measured_conds):
            self.current_idx = idx
            self.cond_listbox.selection_clear(0, tk.END)
            self.cond_listbox.selection_set(idx)
            self.cond_listbox.see(idx)
            
            c = self.measured_conds[idx]
            cid = c["condition_id"]
            clicks_count = len(self.clicks[cid])
            
            self.title_lbl.config(text=f"[{idx+1}/{len(self.measured_conds)}] {c['name']}  ({c['plot'].upper()} GRAFIKON)")
            self.hint_lbl.config(text=f"Hint: {c.get('hint', '')}  |  Kliknuto: {clicks_count} krstića na ovom stubiću")
            self.status_bar_lbl.config(text=f"Ukupno isklikano: {sum(len(v) for v in self.clicks.values())} krstića")

            self.redraw_canvas()

    def on_list_select(self, event):
        sel = self.cond_listbox.curselection()
        if sel:
            self.select_condition(sel[0])

    def next_condition(self):
        if self.current_idx < len(self.measured_conds) - 1:
            self.select_condition(self.current_idx + 1)
        else:
            self.select_condition(self.current_idx)
            messagebox.showinfo("Kraj", "Došli ste do poslednjeg stubića! Proverite klikove i pritisnite 'SNIMI I ZAVRŠI SVE'.")

    def prev_condition(self):
        if self.current_idx > 0:
            self.select_condition(self.current_idx - 1)

    def clear_current(self):
        cid = self.measured_conds[self.current_idx]["condition_id"]
        self.clicks[cid] = []
        self.refresh_listbox()
        self.select_condition(self.current_idx)

    def on_canvas_left_click(self, event):
        x_disp = event.x
        y_disp = event.y
        x_orig = round(x_disp / self.display_scale, 2)
        y_orig = round(y_disp / self.display_scale, 2)

        cid = self.measured_conds[self.current_idx]["condition_id"]
        self.clicks[cid].append((x_orig, y_orig))
        print(f"Dodat krstić za {cid}: ({x_orig}, {y_orig}) [Ukupno za stubić: {len(self.clicks[cid])}]")
        
        self.refresh_listbox()
        self.select_condition(self.current_idx)

    def on_canvas_right_click(self, event):
        cid = self.measured_conds[self.current_idx]["condition_id"]
        if self.clicks[cid]:
            rem = self.clicks[cid].pop()
            print(f"Obrisan krstić za {cid}: {rem}")
            self.refresh_listbox()
            self.select_condition(self.current_idx)

    def redraw_canvas(self):
        # Create composite image with drawings
        draw_img = self.scaled_img.copy()
        draw = ImageDraw.Draw(draw_img)

        curr_c = self.measured_conds[self.current_idx]
        cid = curr_c["condition_id"]

        # Draw highlight box for active condition if bbox given
        if "bbox" in curr_c and curr_c["bbox"] != (0, 0, 0, 0):
            bx1, by1, bx2, by2 = curr_c["bbox"]
            dx1 = int(bx1 * self.display_scale)
            dy1 = int(by1 * self.display_scale)
            dx2 = int(bx2 * self.display_scale)
            dy2 = int(by2 * self.display_scale)
            draw.rectangle([dx1, dy1, dx2, dy2], outline="#ff9800", width=3)

        # Draw all clicked markers across all conditions
        for cond_id, pts in self.clicks.items():
            is_active = (cond_id == cid)
            col = "#ff1744" if is_active else "#757575"
            r = 5 if is_active else 3
            
            for pt in pts:
                px = int(pt[0] * self.display_scale)
                py = int(pt[1] * self.display_scale)
                draw.ellipse([px-r, py-r, px+r, py+r], fill=col, outline="white", width=1)
                # Cross
                draw.line([px-r-2, py, px+r+2, py], fill="white", width=1)
                draw.line([px, py-r-2, px, py+r+2], fill="white", width=1)

        self.tk_img = ImageTk.PhotoImage(draw_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def save_and_finish(self):
        total_clicks = sum(len(v) for v in self.clicks.values())
        if total_clicks < 20:
            if not messagebox.askyesno("Upozorenje", f"Zabeleženo je samo {total_clicks} krstića. Da li ste sigurni da želite da snimite?"):
                return

        repo_root = Path(__file__).resolve().parents[3]
        artifacts_dir = repo_root / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        conditions_output = {}
        for cond in CONDITIONS:
            cid = cond["condition_id"]
            pts = self.clicks[cid]
            visual_class = "MEASURED_PRESENT" if len(pts) > 0 else "EXTRAPOLATED_ONLY"
            
            raw_markers = [
                {"x_px": p[0], "y_px": p[1], "plot": cond["plot"]}
                for p in pts
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
            messagebox.showerror("Greška", f"Greška pri proračunu:\n{res.stderr}")
        else:
            messagebox.showinfo("Uspešno", f"Uspešno snimljeno {total_clicks} krstića!\nReferentne tabele su generisane.")
            self.root.destroy()

def main():
    parser = argparse.ArgumentParser(description="Tkinter Guided Figure 2a Precision Digitizer")
    parser.add_argument("--image", type=str, default="/tmp/figure2_crop.png", help="Path to Figure 2 image")
    parser.add_argument("--operator", type=str, default="Ivan", help="Operator name")
    args = parser.parse_args()

    root = tk.Tk()
    app = DigitizerGUI(root, args.image, args.operator)
    root.mainloop()

if __name__ == "__main__":
    main()
