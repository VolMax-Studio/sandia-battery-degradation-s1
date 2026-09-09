# sandia-battery-degradation-s1

An independent, pre-registered computational verification instance under the P10 verification method.

**Subject Claim:** Preger et al., *"Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions"*, *Journal of The Electrochemical Society* 167, 120532 (2020), DOI: [10.1149/1945-7111/abae37](https://doi.org/10.1149/1945-7111/abae37), OSTI: [1650174](https://www.osti.gov/biblio/1650174) — specifically the equivalent-full-cycle (EFC) values to 80% capacity retention reported in Figure 2a.

---

### Current status — 9 September 2026

**A1-H is administratively closed: IMPLEMENTATION NONCONFORMANCE.** No controlled §7 scientific verdict is issued. The preserved run's ZERO_0_OF_12 output is not accepted as a scientific result. A2 remains UNRESOLVED.

See [STATUS.md](STATUS.md), [operator-ratified closure](governance/run-002-review/A1H_CLOSURE.md), and the two separate [failure records](FAILURES.md). Frozen preregistration and engine bytes remain unchanged. Private source/custody artifacts are not distributed by this repository.

The POST_CORPUS_VIEW_EXPLORATORY 86-cell baseline now has [ratified RB0 v1.0.3](research/SANDIA_86_CELL_REFERENCE_BASELINE_v1/RB0_RATIFICATION.md). Only [representation instrument preparation](research/SANDIA_86_CELL_REFERENCE_BASELINE_v1/representation-preparation-v1.1/README.md) is authorized. The preparation package awaits Operator review; reference labels, predictions, gate execution and RB1–RB5 remain unauthorized.

---

## What Is Being Verified

Figure 2a of the source publication reports, per cycling condition, the equivalent full cycles at which commercial 18650 cells (LFP, NMC, NCA) reached 80% capacity retention. The figure caption states:
> *"Where a bar does not include values for individual cells, those cells had not yet reached 80% and the indicated EFC is extrapolated from the present degradation rate."*

For LFP specifically, the text states that lifetime was extrapolated based on the linear degradation rate at the time of publication.

This audit separates what was measured on laboratory cyclers from what was extended by an extrapolation ruler:

* **Target A1-H (Horizon-Independent Replicate Multiset Reconstruction):** Evaluates strictly those conditions where the digitized reference shows an empirical crossing marker for every replicate declared in metadata ($N_{\text{vis}} == N_{\text{rep}} > 0$). For those cells, the first 80% capacity crossing is a completed historical laboratory event: continued cycling after 2020 cannot alter that first crossing. This makes Target A1-H independent of the unresolved question of what exact cutoff date the authors held at paper submission.
* **Target A2 (Extrapolated Cohort Classification):** Blocked pending an authoritative, machine-actionable publication observation horizon.

---

## What Is Frozen

Every baseline artifact, reference digitizer reading, specification envelope, and execution contract is immutably frozen under cryptographic SHA-256 control:

| Artifact | Role | SHA-256 Digest |
| :--- | :--- | :--- |
| [`artifacts/figure2a_raw_pixel_clicks.json`](artifacts/figure2a_raw_pixel_clicks.json) | Raw digitizer coordinates | `ffdb638a314ff5071fcba443715ca228480cd818d4ec9c36ab7d32cb365628b6` |
| [`artifacts/figure2a_reference.csv`](artifacts/figure2a_reference.csv) | Reference comparator table | `4f939332492716d87a51a315cf9b8d40d72dff28a305ae5c30d9bcba9c21b18b` |
| [`artifacts/reference_partition_analysis.json`](artifacts/reference_partition_analysis.json) | Measured / extrapolated partition | `a19e06817aeb10f7c63e75ebbd3b5c603dda36582f887b442d28970f64d8a3ff` |
| [`artifacts/a1_h_eligibility_manifest.json`](artifacts/a1_h_eligibility_manifest.json) | Per-condition eligibility mapping | `38ca21adb628e0165f3b85e849feead29b4a095a0774a4fc34e3d6c7ac0056f2` |
| [`artifacts/specification_matrix.json`](artifacts/specification_matrix.json) | 12-model specification envelope | `a8fa7e4d7fddb76ff5ffd761b21901bab3f69a6077df4f254298a22c00de3812` |
| [`runs/run-002-a1h/a1_h_required_inputs.json`](runs/run-002-a1h/a1_h_required_inputs.json) | Derived required-input population | `e044432a2f14307d987ecde3695d9380416ab0192e8716848633697e9c3f1128` |
| [`runs/run-002-a1h/run_metadata.json`](runs/run-002-a1h/run_metadata.json) | Run rules, F31–F38, & cutoff governance | — |

All artifacts are verified against [`evidence/l0/derived_artifacts.sha256`](evidence/l0/derived_artifacts.sha256) and [`ARTIFACTS.json`](ARTIFACTS.json).

The required-input population was derived mechanically from the frozen cell listing and eligibility manifest before telemetry acquisition; it comprises exactly **5 conditions** and **12 required cells**:
1. `LFP_0-100_25C_0.5-3C` (4 cells: `SNL_18650_LFP_25C_0-100_0.5/3C_a` to `_d`)
2. `NCA_0-100_15C_0.5-2C` (2 cells: `SNL_18650_NCA_15C_0-100_0.5/2C_a`, `_b`)
3. `NCA_0-100_25C_0.5-2C` (2 cells: `SNL_18650_NCA_25C_0-100_0.5/2C_a`, `_b`)
4. `NMC_0-100_15C_0.5-1C` (2 cells: `SNL_18650_NMC_15C_0-100_0.5/1C_a`, `_b`)
5. `NMC_0-100_25C_0.5-2C` (2 cells: `SNL_18650_NMC_25C_0-100_0.5/2C_a`, `_b`)

---

## Stated Limitations of the Reference

Across the 33 conditions evaluated in the Figure 2a population:
* **3 conditions (9.1%)** exhibit physically impossible marker counts where digitized crossing count exceeds known metadata replicate count: `LFP_20-80_25C_0.5-3C` (2 markers vs 1 cell), `NMC_20-80_25C_0.5-3C` (3 markers vs 2 cells), and `NCA_0-100_35C_0.5-2C` (3 markers vs 2 cells). All three are formally excluded from Target A1-H due to unresolved reference defects.
* **11 conditions (33.3%)** exhibit marker deficits ($N_{\text{vis}} < N_{\text{rep}}$), attributable to visual overplotting/occlusion in the published raster, to cells not having reached 80% before the publication-era horizon, or a combination thereof. The composite label `INELIGIBLE_CARDINALITY_OR_HORIZON_UNRESOLVED` is documented as a known reference limitation for Target A2.
* **14 conditions (42.4%)** contain zero published crossing markers (purely extrapolated cohort; evaluated under Target A2).
* **5 conditions (15.2%)** exhibit exact cardinality ($N_{\text{vis}} == N_{\text{rep}} > 0$) and form the complete Target A1-H cohort.

> [!NOTE]
> The required-input population inherits the stated measurement, resolution, and classification uncertainty of the digitized reference (Rule F32). No condition or cell may be added or removed after telemetry observation on the basis of reinterpretation of the figure.

---

## The Access Finding

### `FINDING-L0-ACCESS-DRIFT-001`
The 2020 publication states that all cycling files were made publicly available at `batteryarchive.org`. The historically documented direct-download interface (per-cell `[cell_id]_cycle_data.csv` and `_timeseries.csv` under a static path) no longer resolves: **86 acquisition attempts returned HTTP 404**. The host currently directs users to request bulk CSV files by email (`info@batteryarchive.org`).

The SNL study remains publicly described and hosted by BatteryArchive; its data are actively visualized through the platform's dashboard interface. This represents an **access-layer interface change**, not evidence of concealment or suppression. A formal inquiry was dispatched to `info@batteryarchive.org` on 5 September 2026 requesting:
1. Supported bulk acquisition access for the 86 SNL cells,
2. Explicit reuse and redistribution licensing terms,
3. Authoritative laboratory observation cutoff date used for Figure 2a,
4. Exact calculation conventions for $Q_0$, $N_{80}$, and EFC.

Additionally, the dataset is longitudinally live rather than publication-frozen: BatteryArchive notes that cycling is ongoing, and subsequent Sandia publications describe multi-year continuation. Contemporary access to the live dataset does not by itself reproduce the evidentiary state available when Figure 2a was published in 2020.

---

## What Happens at the Cutoff

Rule F38 defines the deterministic closure logic:
`A1H_INPUT_READY = TRUE` if and only if, by **`2026-09-21T20:00:00+02:00`** (Europe/Belgrade, 12:00 MDT), every cell enumerated in `a1_h_required_inputs.json` has been acquired through a host-supported route, is non-empty (`byte_count > 0`), resolves uniquely to a canonical cell ID, passes the frozen engine input contract (`4007a07`), and has its SHA-256 captured.

If these conditions are not met:
* **Disposition:** `CLOSED_REQUIRED_INPUTS_NOT_ACQUIRED_BY_PREREGISTERED_CUTOFF`
* **Target A1-H Verdict:** `Not Demonstrated`
* **Public Limitation:** The acquisition window provided nine full U.S. business days plus the first half of 21 September 2026 following the Labor Day holiday. Resulting disposition applies strictly to this preregistered acquisition window and does not demonstrate that telemetry does not exist or could not become accessible later.
* **Supplemental Evidence Policy:** Evidence arriving after the cutoff opens `run-003-a1h-late-host-evidence`, which is supplemental only and does not retroactively alter `run-002`.

---

## Reproducing This Repository

To verify the complete cryptographic integrity, unit tests, and mechanical derivation from a clean checkout:

```bash
# 1. Clone repository
git clone https://github.com/VolMax-Studio/sandia-battery-degradation-s1.git
cd sandia-battery-degradation-s1

# 2. Verify all 31 SHA-256 checksums
sha256sum -c evidence/l0/derived_artifacts.sha256
sha256sum -c evidence/l0/external_sources.sha256

# 3. Execute verification engine test suite
python3 -m unittest discover -s evidence/l0/tests

# 4. Regenerate required-input manifest deterministically
python3 evidence/l0/scripts/generate_a1_h_required_inputs.py
```

The generator rebuilds `a1_h_required_inputs.json` byte-identically (`SHA256: e044432a...`) from frozen sources and prints an exhaustive 33-condition audit report.

---

## Data and Licensing

* **Telemetry Storage:** No raw telemetry files are committed to this repository (`runs/*/raw_data/` is strictly `.gitignore`d).
* **Source Publication:** Open Access via ECS / IOP Publishing under [CC BY-NC-ND 4.0](http://creativecommons.org/licenses/by-nc-nd/4.0/).
* **Platform Code:** BatteryArchive framework tools are licensed under GNU GPLv3 / NTESS retained rights (Contract DE-NA0003525).
* **Dataset Terms:** Attribution-based reuse under host terms; raw redistribution withheld pending formal confirmation.

---

## Status Vocabulary

Verdicts are drawn strictly from a controlled set:
* **`Verified`** — Claim reproduced within preregistered specifications and tolerances.
* **`Verified with Limitations`** — Claim reproduced with documented specification sensitivity or domain boundaries.
* **`Not Verified`** — Claim contradicted by empirical evidence under declared envelope.
* **`Not Demonstrated`** — Required empirical evidence was not obtainable within the declared evidence boundary. (A statement about evidence availability, not underlying physical truth).
* **`Unfalsifiable-as-Stated`** — Claim lacks necessary empirical or mathematical precision for testing.
* **`Deferred`** — Awaiting preregistered milestone or ongoing experimental protocol.

---

## Citation

```bibtex
@misc{nestorov2026sandia,
  author       = {Ivan Nestorov},
  title        = {Independent Computational Verification of the Sandia Commercial Li-Ion Battery Degradation Dataset (Preger et al. 2020)},
  year         = {2026},
  publisher    = {VolMax Studio Lab},
  howpublished = {\url{https://github.com/VolMax-Studio/sandia-battery-degradation-s1}},
  note         = {ORCID: 0009-0006-7940-9539}
}
```
