# Candidate Evaluation: `sandia-battery-degradation-s1`

**Target Study:** Preger et al., *"Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions"*, *Journal of The Electrochemical Society* 167 120532 (2020), pages 120532-1 to 120532-13.  
**DOI:** [`10.1149/1945-7111/abae37`](https://doi.org/10.1149/1945-7111/abae37)  
**OSTI Identifier:** `1650174` ([osti.gov/biblio/1650174](https://www.osti.gov/biblio/1650174))  
**Primary Data Repository:** [BatteryArchive.org](https://www.batteryarchive.org) (Sandia National Laboratories / SNL Dataset)  
**Phase:** Candidate Evaluation & L0 Source Hunt  
**Evaluation Date:** 2026-09-05  

---

## 1. Candidate Justification & Domain Expansion

`sandia-battery-degradation-s1` is selected as the candidate for the third flagship P10 audit instance, expanding the portfolio across:
* **New Physical Domain:** Electrochemical engineering / battery degradation physics.
* **New Claimant:** Sandia National Laboratories (SNL) / US Department of Energy (DOE).
* **Direct Laboratory Telemetry:** Multi-year galvanostatic battery cycler telemetry (Arbin / Maccor time-series and cycle summaries), not vendor aggregated dashboards.
* **Direct Measurable Quantities:** Discharge capacity ($Q$), energy retention ($E$), round-trip efficiency (RTE), cycle count ($N$), and equivalent full cycles (EFC).

---

## 2. Verbatim Public Claims & Audit Scope

### Verbatim Published Abstract (Preger et al., p. 120532-1; OSTI 1650174):
> *"Energy storage systems with Li-ion batteries are increasingly deployed to maintain a robust and resilient grid and facilitate the integration of renewable energy resources. However, appropriate selection of cells for different applications is difﬁcult due to limited public data comparing the most commonly used off-the-shelf Li-ion chemistries under the same operating conditions. This article details a multi-year cycling study of commercial LiFePO4 (LFP), LiNixCoyAl1−x−yO2 (NCA), and LiNixMnyCo1−x−yO2 (NMC) cells, varying the discharge rate, depth of discharge (DOD), and environment temperature. The capacity and discharge energy retention, as well as the round-trip efﬁciency, were compared. Even when operated within manufacturer speciﬁcations, the range of cycling conditions had a profound effect on cell degradation, with time to reach 80% capacity varying by thousands of hours and cycle counts among cells of each chemistry. The degradation of cells in this study was compared to that of similar cells in previous studies to identify universal trends and to provide a standard deviation for performance. All cycling ﬁles have been made publicly available at batteryarchive.org, a recently developed repository for visualization and comparison of battery data, to facilitate future experimental and modeling efforts."*

### Verbatim Figure 2 Caption (Preger et al., p. 120532-4):
> *"Figure 2. (a) Equivalent full cycle (EFC) count at 80% capacity for all cells and cycling conditions. Each bar represents the average EFC for all cells cycled at that condition. The values for individual cells are noted with a “+”. If a bar does not include values for individual cells, then those cells have not yet reached 80% capacity and the indicated EFC is extrapolated based on the present degradation rate for those cells. (b) Cumulative discharge energy at 80% capacity for all cells and cycling conditions. Each bar represents the average discharge energy for all cells cycled at that condition. (c) Round-trip efﬁciency (RTE) for all cells and cycling conditions. Each bar represents the average initial RTE for all cells cycled at that condition. The RTE at the end of the study is indicated with a dot. If a bar does not include a dot, then those cells have not yet reached 80% capacity."*

### Flagship Audit Scope (Candidate Target A):
* **Target A1 (Measured 80% EOL Event Reconstruction):** Deterministically reconstruct the discrete 80% capacity retention crossing events from the deposited raw BatteryArchive telemetry for all measured cells.
* **Target A2 (Cohort Classification):** Cleanly separate the measured cohort from the projected/extrapolated cohort using published artifact criteria.

---

## 3. Primary Artifact Identity & Provenance

* **Primary Repository:** [BatteryArchive.org](https://www.batteryarchive.org)
* **Dataset Identifier:** `Sandia National Laboratories (SNL) Degradation Study` (`study = 'snl'`)
* **Cell Population:** 86 physical cells cataloged in [`evidence/l0/raw_listing.txt`](evidence/l0/raw_listing.txt).
* **Licensing / Access:**
  - Publication: `CC BY-NC-ND 4.0` (Crossref license record dated 2020-09-02; Copyright © 2020 The Author(s)).
  - Dataset Access: `public` (Citation to Preger et al. 2020 and BatteryArchive.org required; standalone redistribution unconfirmed).
  - Framework Software Tools: `GNU GPLv3 / NTESS Contract DE-NA0003525`.
* **Artifact Metadata & Hashes:** Formally documented in [`ARTIFACTS.json`](ARTIFACTS.json), [`evidence/l0/external_sources.sha256`](evidence/l0/external_sources.sha256), and [`evidence/l0/derived_artifacts.sha256`](evidence/l0/derived_artifacts.sha256).

---

## 4. Raw Data Schema & Cell Mapping

### Standardized Identifier Standards:
- **Database Cell ID:** `SNL_18650_{cathode}_{temperature}C_{min_soc}-{max_soc}_{charge_rate}/{discharge_rate}C_{replicate}`
- **Filesystem Filename Base:** `SNL_18650_{cathode}_{temperature}C_{min_soc}-{max_soc}_{charge_rate}-{discharge_rate}C_{replicate}`  
  *(where `/` in charge/discharge rate is converted to `-` per `data_transfer.py:L135`)*

Example:
* Database ID: `SNL_18650_LFP_25C_0-100_0.5/1C_a`
* Filename: `SNL_18650_LFP_25C_0-100_0.5-1C_a_cycle_data.csv`
  - Cathode: `LFP` (A123 Systems APR18650M1A, 1.1 Ah)
  - Temperature: `25°C`
  - SOC Range: `0–100%` (100% DOD)
  - Rates: `0.5C charge / 1C discharge`
  - Replicate: `a`

### Cycle Summary Columns (Declared by Framework):
`Cycle_Index`, `Test_Time (s)`, `Min_Current (A)`, `Max_Current (A)`, `Min_Voltage (V)`, `Max_Voltage (V)`, `Charge_Capacity (Ah)`, `Discharge_Capacity (Ah)`, `Charge_Energy (Wh)`, `Discharge_Energy (Wh)`.

---

## 5. Candidate Estimator Status & Discovery Rules

The L0 discovery phase confirms that the author basis for EFC is capacity throughput divided by nominal capacity (p. 120532-4), while flagging candidate implementation details as **OPEN** for Phase 1 Preregistration freeze:
1. **Baseline Capacity ($Q_0$):** RPT capacity check vs Cycle 1 discharge capacity.
2. **80% EOL Threshold Crossing ($N_{80}$):** Discrete first crossing vs linear interpolation.
3. **Cohort Partitioning:** Separation of measured 80% crossings (with `+` markers) from projected/extrapolated values (without `+` markers).

---

## 6. L0 STOP / HALT Invariants & Data Handling

The instance must immediately HALT at the L0 phase if any of the following occur:
1. **`L0_HALT_NO_RAW_DATA`:** The repository contains only smoothed/modelled curve fits rather than discrete raw cycler measurements.
2. **`L0_HALT_MAPPING_AMBIGUITY`:** Local CSV files cannot be bijectively mapped to published test conditions in Preger et al.
3. **`L0_HALT_INCOMPLETE_REPLICATES`:** Cell replicates reported in publication figures are missing or unflagged in the public data deposit.
4. **`L0_HALT_UNDEFINED_ESTIMATOR`:** Methods/SI lack sufficient detail to define $Q_0$ and $N_{80}$ without arbitrary tuning parameters.
5. **`L0_HALT_DATA_BLOB_LEAK`:** Raw telemetry CSV files are committed to git (prevented by `.gitignore` invariant).

---

## 7. Current Governance Status

* **Phase:** `Candidate Evaluation & L0 Source Hunt`
* **Execution Permitted:** `NO` (No analytical execution or preregistration freeze until L0 Gate review).
* **Current Action:** L0 dossier remediation complete; ready for Claude L0 Gate review.
