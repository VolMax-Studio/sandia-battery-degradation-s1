#!/usr/bin/env python3
"""
Target A1-H Computational Verification Engine
Specification-Robustness Envelope over 12 Candidate Estimator Models

Features:
- Reads cycle summary data per cell.
- Extracts Q0 under candidate rules (Q0A, Q0B, Q0C).
- Computes cumulative throughput (EFCA, EFCB).
- Evaluates 80% EOL crossing under discrete (N80A) and interpolated (N80B) rules.
- Emits transparent intermediate cell-level audit records.
- Computes unordered sorted multiset residuals d_{c,j}^{(m)} against frozen Figure 2a reference.
- Computes specification-by-condition pass matrix, global consistency flags, and robustness scores.
"""

import sys
import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Nominal capacity by chemistry (Preger et al. 2020 Table I)
NOMINAL_CAPACITIES_AH = {
    "LFP": 1.1,
    "NMC": 3.0,
    "NCA": 3.2
}

def extract_q0(cycle_rows: List[Dict[str, float]], q0_type: str) -> float:
    """
    Extract baseline initial capacity Q0.
    In SNL degradation protocol, initial cycles (1-3) represent 0.5C RPT capacity checks (0-100% SOC).
    """
    if len(cycle_rows) == 0:
        raise ValueError("Cannot extract Q0 from empty cycle records")

    # Get initial discharge capacities
    dis_caps = [r["Discharge_Capacity (Ah)"] for r in cycle_rows[:3] if "Discharge_Capacity (Ah)" in r]
    if not dis_caps:
        # Fallback to alternate column naming if present
        dis_caps = [r.get("Discharge_Capacity", 0.0) for r in cycle_rows[:3]]

    if not dis_caps:
        raise ValueError("Discharge capacity channel missing from cycle records")

    if q0_type == "Q0A":
        return dis_caps[0]
    elif q0_type == "Q0B":
        return sum(dis_caps) / len(dis_caps)
    elif q0_type == "Q0C":
        return dis_caps[-1]
    else:
        raise ValueError(f"Unknown Q0 formulation: {q0_type}")

def compute_cumulative_efc(cycle_rows: List[Dict[str, float]], q_nominal: float, efc_type: str) -> List[float]:
    """
    Compute cumulative EFC series for all cycles in order.
    """
    efc_series = []
    cum_dis = 0.0
    cum_chg = 0.0

    for r in cycle_rows:
        dis = r.get("Discharge_Capacity (Ah)", r.get("Discharge_Capacity", 0.0))
        chg = r.get("Charge_Capacity (Ah)", r.get("Charge_Capacity", 0.0))
        
        cum_dis += dis
        cum_chg += chg

        if efc_type == "EFCA":
            efc_val = cum_dis / q_nominal
        elif efc_type == "EFCB":
            efc_val = (cum_dis + cum_chg) / (2.0 * q_nominal)
        else:
            raise ValueError(f"Unknown EFC throughput formulation: {efc_type}")

        efc_series.append(efc_val)

    return efc_series

def find_80pct_crossing(
    cycle_rows: List[Dict[str, float]],
    efc_series: List[float],
    q0: float,
    n80_type: str
) -> Tuple[str, Optional[int], Optional[float]]:
    """
    Find 80% EOL crossing event.
    Returns: (status: 'OBSERVED' | 'NO_CROSSING', cycle_index, reconstructed_efc80)
    """
    threshold_q80 = 0.80 * q0
    
    for idx, r in enumerate(cycle_rows):
        dis_cap = r.get("Discharge_Capacity (Ah)", r.get("Discharge_Capacity", 0.0))
        
        # Skip initial baseline check cycles (index 0, 1, 2) to avoid false trigger on check formation
        if idx < 3:
            continue

        if dis_cap <= threshold_q80:
            cycle_num = int(r.get("Cycle_Index", idx + 1))
            
            if n80_type == "N80A":
                # Discrete first crossing
                efc80 = efc_series[idx]
                return ("OBSERVED", cycle_num, round(efc80, 2))
            
            elif n80_type == "N80B":
                # Linear continuous interpolation between bracketing cycles
                if idx > 0:
                    prev_cap = cycle_rows[idx - 1].get("Discharge_Capacity (Ah)", cycle_rows[idx - 1].get("Discharge_Capacity", 0.0))
                    prev_efc = efc_series[idx - 1]
                    curr_efc = efc_series[idx]
                    
                    if prev_cap != dis_cap:
                        frac = (threshold_q80 - prev_cap) / (dis_cap - prev_cap)
                        frac = max(0.0, min(1.0, frac))
                        interp_efc = prev_efc + frac * (curr_efc - prev_efc)
                    else:
                        interp_efc = curr_efc
                else:
                    interp_efc = efc_series[idx]
                
                return ("OBSERVED", cycle_num, round(interp_efc, 2))
            else:
                raise ValueError(f"Unknown N80 crossing rule: {n80_type}")

    return ("NO_CROSSING", None, None)

def evaluate_cell_single_spec(
    cell_id: str,
    condition_id: str,
    chemistry: str,
    cycle_rows: List[Dict[str, float]],
    spec: Dict[str, str]
) -> Dict[str, Any]:
    """
    Evaluate single cell under single specification model.
    """
    q_nom = NOMINAL_CAPACITIES_AH.get(chemistry, 1.0)
    q0 = extract_q0(cycle_rows, spec["q0"])
    q80_thresh = round(0.80 * q0, 4)
    efc_series = compute_cumulative_efc(cycle_rows, q_nom, spec["efc"])
    status, cycle_idx, efc80 = find_80pct_crossing(cycle_rows, efc_series, q0, spec["n80"])

    return {
        "cell_id": cell_id,
        "condition_id": condition_id,
        "chemistry": chemistry,
        "spec_id": spec["spec_id"],
        "spec_code": spec["code"],
        "q0_type": spec["q0"],
        "q0_value_ah": round(q0, 4),
        "q80_threshold_ah": q80_thresh,
        "n80_rule": spec["n80"],
        "efc_type": spec["efc"],
        "crossing_status": status,
        "crossing_cycle": cycle_idx,
        "reconstructed_efc80": efc80
    }

def evaluate_condition_multiset_under_spec(
    condition_id: str,
    spec_id: str,
    reconstructed_efcs: List[float],
    published_markers_efc: List[float],
    tau_c: float
) -> Dict[str, Any]:
    """
    Evaluate sorted unordered multiset comparison against published Figure 2a markers under tau_c.
    """
    if len(reconstructed_efcs) != len(published_markers_efc):
        return {
            "condition_id": condition_id,
            "spec_id": spec_id,
            "cardinality_status": "CARDINALITY_MISMATCH",
            "evaluable": False,
            "reconstructed_multiset": reconstructed_efcs,
            "published_multiset": published_markers_efc,
            "residuals": [],
            "max_residual": None,
            "tau_c": tau_c,
            "condition_pass": False
        }

    # Sort ascending for canonical unordered multiset pairing
    recon_sorted = sorted(reconstructed_efcs)
    pub_sorted = sorted(published_markers_efc)

    residuals = [round(abs(r - p), 2) for r, p in zip(recon_sorted, pub_sorted)]
    max_res = max(residuals) if residuals else 0.0
    cond_pass = (max_res <= tau_c)

    return {
        "condition_id": condition_id,
        "spec_id": spec_id,
        "cardinality_status": "EXACT_CARDINALITY_MATCH",
        "evaluable": True,
        "reconstructed_multiset": recon_sorted,
        "published_multiset": pub_sorted,
        "residuals": residuals,
        "max_residual": max_res,
        "tau_c": tau_c,
        "condition_pass": cond_pass
    }

def run_a1_h_verification(
    cell_data_dict: Dict[str, Dict[str, Any]],
    ref_csv_path: Path,
    spec_matrix_path: Path,
    output_dir: Path
) -> Dict[str, Any]:
    """
    Full Target A1-H Verification Pipeline over all cells, conditions, and 12 specifications.
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Load specifications
    spec_data = json.loads(spec_matrix_path.read_text(encoding="utf-8"))
    specs = spec_data["specifications"]

    # Load Figure 2a reference table
    with open(ref_csv_path, encoding="utf-8") as f:
        ref_rows = list(csv.DictReader(f))

    ref_by_cond = {r["condition_id"]: r for r in ref_rows}
    a1_h_eligible_conds = [r["condition_id"] for r in ref_rows if r["a1_reference_status"] == "EXACT_CARDINALITY_MATCH"]

    # 1. Compute cell-level intermediate records across all 12 specs
    cell_records = []
    cell_results_by_cond_spec: Dict[Tuple[str, str], List[float]] = {}

    for cell_id, cinfo in cell_data_dict.items():
        cid = cinfo["condition_id"]
        chem = cinfo["chemistry"]
        cycle_rows = cinfo["cycle_rows"]

        for spec in specs:
            rec = evaluate_cell_single_spec(cell_id, cid, chem, cycle_rows, spec)
            cell_records.append(rec)
            
            if rec["crossing_status"] == "OBSERVED" and rec["reconstructed_efc80"] is not None:
                key = (cid, spec["spec_id"])
                if key not in cell_results_by_cond_spec:
                    cell_results_by_cond_spec[key] = []
                cell_results_by_cond_spec[key].append(rec["reconstructed_efc80"])

    # Write intermediate cell records
    cell_rec_path = output_dir / "a1_h_intermediate_cell_records.json"
    cell_rec_path.write_text(json.dumps(cell_records, indent=2), encoding="utf-8")

    # 2. Condition-by-Specification Matrix Evaluation
    matrix_results: Dict[str, Dict[str, Any]] = {}
    residual_rows = []

    for cid in a1_h_eligible_conds:
        cond_ref = ref_by_cond[cid]
        pub_markers_str = cond_ref.get("digitized_marker_efc", "")
        pub_markers = [float(x) for x in pub_markers_str.split(";") if x.strip()]
        tau_c = float(cond_ref.get("tau_c", 50.8))

        matrix_results[cid] = {
            "condition_id": cid,
            "chemistry": cond_ref["chemistry"],
            "published_markers": pub_markers,
            "tau_c": tau_c,
            "specifications": {}
        }

        for spec in specs:
            sid = spec["spec_id"]
            recon_efcs = cell_results_by_cond_spec.get((cid, sid), [])
            
            eval_res = evaluate_condition_multiset_under_spec(cid, sid, recon_efcs, pub_markers, tau_c)
            matrix_results[cid]["specifications"][sid] = eval_res

            residual_rows.append({
                "condition_id": cid,
                "chemistry": cond_ref["chemistry"],
                "spec_id": sid,
                "spec_code": spec["code"],
                "evaluable": eval_res["evaluable"],
                "published_markers": ";".join(map(str, eval_res["published_multiset"])),
                "reconstructed_efcs": ";".join(map(str, eval_res["reconstructed_multiset"])),
                "residuals": ";".join(map(str, eval_res["residuals"])),
                "max_residual": eval_res["max_residual"],
                "tau_c": tau_c,
                "condition_pass": eval_res["condition_pass"]
            })

    # Write residual table CSV
    res_csv_path = output_dir / "a1_h_residual_table.csv"
    if residual_rows:
        with open(res_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(residual_rows[0].keys()))
            writer.writeheader()
            writer.writerows(residual_rows)

    # 3. Global Robustness Summary
    global_spec_summary = {}
    num_a1_h_conds = len(a1_h_eligible_conds)

    for spec in specs:
        sid = spec["spec_id"]
        passing_conds = sum(1 for cid in a1_h_eligible_conds if matrix_results[cid]["specifications"][sid]["condition_pass"])
        is_global_match = (passing_conds == num_a1_h_conds and num_a1_h_conds > 0)
        
        global_spec_summary[sid] = {
            "spec_id": sid,
            "spec_code": spec["code"],
            "passing_conditions_count": passing_conds,
            "total_evaluable_conditions": num_a1_h_conds,
            "pass_rate_pct": round(passing_conds / num_a1_h_conds * 100.0, 2) if num_a1_h_conds > 0 else 0.0,
            "full_global_match": is_global_match
        }

    global_passing_specs_count = sum(1 for s in global_spec_summary.values() if s["full_global_match"])
    
    if global_passing_specs_count == 12:
        robustness_class = "FULL_12_OF_12"
        verdict = "Verified"
    elif global_passing_specs_count > 0:
        robustness_class = f"SPECIFICATION_SENSITIVE ({global_passing_specs_count}/12)"
        verdict = "Verified with Limitations"
    else:
        # Check if any conditions pass under individual specs
        any_cond_pass = any(s["passing_conditions_count"] > 0 for s in global_spec_summary.values())
        if any_cond_pass:
            robustness_class = "PARTIAL_CONDITION_ONLY (0/12 Global)"
            verdict = "Not Verified"
        else:
            robustness_class = "ZERO_0_OF_12"
            verdict = "Not Verified"

    full_output = {
        "artifact": "a1_h_specification_matrix_results",
        "generated_at": spec_data.get("generated_at", ""),
        "total_evaluable_a1_h_conditions": num_a1_h_conds,
        "eligible_condition_ids": a1_h_eligible_conds,
        "controlled_verdict": verdict,
        "robustness_classification": robustness_class,
        "global_spec_summary": global_spec_summary,
        "condition_matrix": matrix_results
    }

    matrix_json_path = output_dir / "a1_h_specification_matrix_results.json"
    matrix_json_path.write_text(json.dumps(full_output, indent=2), encoding="utf-8")

    return full_output

def main():
    parser = argparse.ArgumentParser(description="Target A1-H Computational Verification Engine")
    parser.add_argument("--ref", type=str, default="artifacts/figure2a_reference.csv", help="Path to reference CSV")
    parser.add_argument("--specs", type=str, default="artifacts/specification_matrix.json", help="Path to specification matrix")
    parser.add_argument("--outdir", type=str, default="artifacts", help="Output directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    ref_path = (repo_root / args.ref).resolve()
    specs_path = (repo_root / args.specs).resolve()
    out_dir = (repo_root / args.outdir).resolve()

    print(f"Target A1-H Verification Engine Initialized.")
    print(f"Reference: {ref_path}")
    print(f"Specs:     {specs_path}")
    print(f"Run Status: NOT_AUTHORIZED (Engine is frozen for pre-execution verification)")

if __name__ == "__main__":
    main()
