#!/usr/bin/env python3
"""
Unit Test Suite for Target A1-H Verification Engine
Tests deterministic synthetic fixtures across the 12-model specification grid.
"""

import sys
import json
import unittest
from pathlib import Path
import tempfile

# Add scripts directory to path
repo_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo_root / "evidence" / "l0" / "scripts"))

from reconstruct_a1_h import (
    extract_q0,
    compute_cumulative_efc,
    find_80pct_crossing,
    evaluate_cell_single_spec,
    evaluate_condition_multiset_under_spec,
    run_a1_h_verification
)

class TestReconstructA1H(unittest.TestCase):
    def setUp(self):
        # Synthetic 10-cycle record with known initial RPT check and gradual degradation
        # Q_nom = 3.0 Ah (NMC)
        # Cycle 1: 3.0 Ah (RPT 1)
        # Cycle 2: 3.0 Ah (RPT 2)
        # Cycle 3: 3.0 Ah (RPT 3) -> Q0A = 3.0, Q0B = 3.0, Q0C = 3.0
        # Cycle 4: 2.9 Ah
        # Cycle 5: 2.8 Ah
        # Cycle 6: 2.7 Ah
        # Cycle 7: 2.6 Ah
        # Cycle 8: 2.5 Ah (83.3%)
        # Cycle 9: 2.4 Ah (80.0% -> exact crossing)
        # Cycle 10: 2.3 Ah (76.7%)
        self.synthetic_cycles_exact_crossing = [
            {"Cycle_Index": 1, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 2, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 3, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 4, "Discharge_Capacity (Ah)": 2.9, "Charge_Capacity (Ah)": 2.9},
            {"Cycle_Index": 5, "Discharge_Capacity (Ah)": 2.8, "Charge_Capacity (Ah)": 2.8},
            {"Cycle_Index": 6, "Discharge_Capacity (Ah)": 2.7, "Charge_Capacity (Ah)": 2.7},
            {"Cycle_Index": 7, "Discharge_Capacity (Ah)": 2.6, "Charge_Capacity (Ah)": 2.6},
            {"Cycle_Index": 8, "Discharge_Capacity (Ah)": 2.5, "Charge_Capacity (Ah)": 2.5},
            {"Cycle_Index": 9, "Discharge_Capacity (Ah)": 2.4, "Charge_Capacity (Ah)": 2.4}, # 0.8 * 3.0 = 2.40 Ah
            {"Cycle_Index": 10, "Discharge_Capacity (Ah)": 2.3, "Charge_Capacity (Ah)": 2.3},
        ]

    def test_extract_q0_variants(self):
        cycles = [
            {"Discharge_Capacity (Ah)": 3.10},
            {"Discharge_Capacity (Ah)": 3.05},
            {"Discharge_Capacity (Ah)": 3.00}
        ]
        q0a = extract_q0(cycles, "Q0A")
        q0b = extract_q0(cycles, "Q0B")
        q0c = extract_q0(cycles, "Q0C")

        self.assertAlmostEqual(q0a, 3.10)
        self.assertAlmostEqual(q0b, 3.05)
        self.assertAlmostEqual(q0c, 3.00)

    def test_cumulative_efc(self):
        cycles = [
            {"Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.2},
            {"Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0}
        ]
        efc_a = compute_cumulative_efc(cycles, q_nominal=3.0, efc_type="EFCA")
        efc_b = compute_cumulative_efc(cycles, q_nominal=3.0, efc_type="EFCB")

        # EFCA: 3.0/3.0 = 1.0, (3.0+3.0)/3.0 = 2.0
        self.assertEqual(efc_a, [1.0, 2.0])
        # EFCB: (3.0+3.2)/6.0 = 1.0333..., (6.0+6.2)/6.0 = 2.0333...
        self.assertAlmostEqual(efc_b[0], 6.2 / 6.0)
        self.assertAlmostEqual(efc_b[1], 12.2 / 6.0)

    def test_find_80pct_crossing_exact(self):
        q0 = 3.0
        efc_series = compute_cumulative_efc(self.synthetic_cycles_exact_crossing, q_nominal=3.0, efc_type="EFCA")
        
        status_a, cyc_a, efc80_a = find_80pct_crossing(self.synthetic_cycles_exact_crossing, efc_series, q0, "N80A")
        status_b, cyc_b, efc80_b = find_80pct_crossing(self.synthetic_cycles_exact_crossing, efc_series, q0, "N80B")

        self.assertEqual(status_a, "OBSERVED")
        self.assertEqual(cyc_a, 9)
        self.assertEqual(status_b, "OBSERVED")
        self.assertEqual(cyc_b, 9)
        # Sum discharge to cycle 9 = 3*3 + 2.9 + 2.8 + 2.7 + 2.6 + 2.5 + 2.4 = 24.9 Ah -> 24.9 / 3 = 8.3 EFC
        self.assertAlmostEqual(efc80_a, 8.3)
        self.assertAlmostEqual(efc80_b, 8.3)

    def test_find_80pct_crossing_interpolation(self):
        # Crossing happens strictly between Cycle 8 (2.5 Ah) and Cycle 9 (2.3 Ah), where threshold is 2.4 Ah
        cycles = [
            {"Cycle_Index": 1, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 2, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 3, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 4, "Discharge_Capacity (Ah)": 2.9, "Charge_Capacity (Ah)": 2.9},
            {"Cycle_Index": 5, "Discharge_Capacity (Ah)": 2.8, "Charge_Capacity (Ah)": 2.8},
            {"Cycle_Index": 6, "Discharge_Capacity (Ah)": 2.7, "Charge_Capacity (Ah)": 2.7},
            {"Cycle_Index": 7, "Discharge_Capacity (Ah)": 2.6, "Charge_Capacity (Ah)": 2.6},
            {"Cycle_Index": 8, "Discharge_Capacity (Ah)": 2.5, "Charge_Capacity (Ah)": 2.5}, # 2.5 > 2.4
            {"Cycle_Index": 9, "Discharge_Capacity (Ah)": 2.3, "Charge_Capacity (Ah)": 2.3}, # 2.3 < 2.4 (midpoint)
        ]
        q0 = 3.0
        efc_series = compute_cumulative_efc(cycles, q_nominal=3.0, efc_type="EFCA")
        
        status_a, cyc_a, efc80_a = find_80pct_crossing(cycles, efc_series, q0, "N80A")
        status_b, cyc_b, efc80_b = find_80pct_crossing(cycles, efc_series, q0, "N80B")

        self.assertEqual(status_a, "OBSERVED")
        self.assertEqual(cyc_a, 9)
        # Discrete gives EFC at cycle 9 (24.8 / 3 = 8.27 EFC)
        self.assertAlmostEqual(efc80_a, 8.27, places=1)
        # Interpolated gives midpoint between cycle 8 (22.5/3 = 7.5 EFC) and cycle 9 (8.27 EFC) -> ~7.88 EFC
        self.assertTrue(efc80_b < efc80_a)
        self.assertAlmostEqual(efc80_b, 7.88, places=1)

    def test_non_crossing_cell(self):
        cycles = [
            {"Cycle_Index": 1, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 2, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 3, "Discharge_Capacity (Ah)": 3.0, "Charge_Capacity (Ah)": 3.0},
            {"Cycle_Index": 4, "Discharge_Capacity (Ah)": 2.9, "Charge_Capacity (Ah)": 2.9},
        ]
        q0 = 3.0
        efc_series = compute_cumulative_efc(cycles, q_nominal=3.0, efc_type="EFCA")
        status, cyc, efc80 = find_80pct_crossing(cycles, efc_series, q0, "N80A")
        self.assertEqual(status, "NO_CROSSING")
        self.assertIsNone(cyc)
        self.assertIsNone(efc80)

    def test_unordered_multiset_matching_and_residuals(self):
        # 2 replicates, published markers = [500.0, 550.0], tau_c = 26.0
        # Case 1: Reconstructed = [545.0, 505.0] (unordered) -> sorted: [505.0, 545.0]
        # residuals = [5.0, 5.0], max = 5.0 <= 26.0 -> PASS
        res_pass = evaluate_condition_multiset_under_spec(
            condition_id="NMC_0-100_25C_0.5-2C",
            spec_id="M01",
            reconstructed_efcs=[545.0, 505.0],
            published_markers_efc=[500.0, 550.0],
            tau_c=26.0
        )
        self.assertTrue(res_pass["condition_pass"])
        self.assertEqual(res_pass["residuals"], [5.0, 5.0])
        self.assertEqual(res_pass["max_residual"], 5.0)

        # Case 2: Reconstructed = [600.0, 650.0] -> residuals = [100.0, 100.0] > 26.0 -> FAIL
        res_fail = evaluate_condition_multiset_under_spec(
            condition_id="NMC_0-100_25C_0.5-2C",
            spec_id="M01",
            reconstructed_efcs=[600.0, 650.0],
            published_markers_efc=[500.0, 550.0],
            tau_c=26.0
        )
        self.assertFalse(res_fail["condition_pass"])
        self.assertEqual(res_fail["max_residual"], 100.0)

    def test_full_synthetic_pipeline_execution(self):
        # Test full 12-spec pipeline on synthetic dataset
        ref_csv = repo_root / "artifacts" / "figure2a_reference.csv"
        spec_matrix = repo_root / "artifacts" / "specification_matrix.json"

        # Create synthetic cell dictionary for the 5 A1-H eligible conditions
        synthetic_cohort = {}
        
        # 1. LFP 0-100 25C 3C (4 replicates)
        for rep in ["a", "b", "c", "d"]:
            cid_str = f"SNL_18650_LFP_25C_0-100_0.5-3C_{rep}"
            synthetic_cohort[cid_str] = {
                "condition_id": "LFP_0-100_25C_0.5-3C",
                "chemistry": "LFP",
                "cycle_rows": [
                    {"Cycle_Index": i, "Discharge_Capacity (Ah)": 1.1 if i <= 3 else max(0.85, 1.1 - 0.0003 * i), "Charge_Capacity (Ah)": 1.1}
                    for i in range(1, 1000)
                ]
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir)
            results = run_a1_h_verification(synthetic_cohort, ref_csv, spec_matrix, out_path)
            
            self.assertIn("controlled_verdict", results)
            self.assertIn("robustness_classification", results)
            self.assertEqual(len(results["global_spec_summary"]), 12)
            
            # Verify generated intermediate files
            self.assertTrue((out_path / "a1_h_intermediate_cell_records.json").exists())
            self.assertTrue((out_path / "a1_h_specification_matrix_results.json").exists())
            self.assertTrue((out_path / "a1_h_residual_table.csv").exists())

if __name__ == "__main__":
    unittest.main()
