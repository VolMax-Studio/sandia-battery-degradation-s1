# PREREGISTRATION DRAFT v1: `sandia-battery-degradation-s1`

> [!IMPORTANT]
> **Status: DRAFT v1 (Not Frozen / Pre-Execution)**  
> **Phase:** Phase 1 Preregistration Drafting  
> **Execution State:** `NOT_AUTHORIZED` (No raw telemetry acquisition or analytical computation permitted before formal freeze and Operator sign-off).

---

## 1. Instance Identity & Audit Object

* **Instance:** `sandia-battery-degradation-s1`
* **Claimant Institution:** Sandia National Laboratories (SNL), Albuquerque, NM, USA.
* **Evaluated Study:** Yuliya Preger, Heather M. Barkholtz, Armando Fresquez, Daniel L. Campbell, Benjamin W. Juba, Jessica Romàn-Kustas, Summer R. Ferreira, Babu Chalamala, *"Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions"*, *Journal of The Electrochemical Society* 167, 120532 (2020), pages 120532-1 to 120532-13.
* **DOI:** [`10.1149/1945-7111/abae37`](https://doi.org/10.1149/1945-7111/abae37) | **OSTI ID:** `1650174`
* **Primary Public Data Repository:** [BatteryArchive.org](https://www.batteryarchive.org) (SNL commercial degradation dataset).
* **Audit Architecture:** External physical laboratory cycler telemetry audit against published lifetime endpoints and cohort partition.

---

## 2. Frozen Population Specification

The evaluation population is frozen by cryptographic hash from captured L0 evidence artifacts:
* `evidence/l0/source_pages/batteryarchive_metadata.csv` (SHA256: `690fe03ad84ebebc04b4e5d55b0e32f5aa112f8ce1eebd25130b586f785303ae`)
* `evidence/l0/raw_listing.txt` (SHA256: `c7967e949cb699a119ad47fd3bcc56b06c33cf985634daa5bc835f4518868a7f`)

### Cell Population Breakdown (86 Cells Total):
1. **LFP (30 cells):** A123 Systems APR18650M1A ($Q_{\text{nominal}} = 1.1\text{ Ah}$, $V_{\text{nominal}} = 3.3\text{ V}$)
2. **NMC (32 cells):** LG Chem 18650HG2 / commercial ($Q_{\text{nominal}} = 3.0\text{ Ah}$, $V_{\text{nominal}} = 3.6\text{ V}$)
3. **NCA (24 cells):** Panasonic NCR18650B ($Q_{\text{nominal}} = 3.2\text{ Ah}$, $V_{\text{nominal}} = 3.6\text{ V}$)

**Population Invariant:** No additional cells may be added, and no constituent cells may be silently dropped. If any cell artifact is missing or corrupted:
`HALT_POPULATION_ARTIFACT_MISMATCH`

---

## 3. Core Invariant: Frozen 2020 Observation Horizon & Dual Stream Architecture

As captured in [`evidence/l0/source_pages/batteryarchive_study_summaries.html`](evidence/l0/source_pages/batteryarchive_study_summaries.html#L121):
> *"The dataset from Sandia National Labs used in the publication ... consists of commercial 18650 NCA, NMC, and LFP cells cycled to 80% capacity (although cycling is still ongoing)."*

Because laboratory cycling continued after the 2020 publication date:
1. **2020 Data Horizon Cutoff:** All Figure 2a comparison targets (Target A1 and Target A2) are evaluated strictly against observations recorded up to the publication's 2020 observation horizon.
2. **Dual Telemetry Stream Requirement (172 Files Total):**
   - Cycle summary records (`[filename_base]_cycle_data.csv`) contain cycle metrics and elapsed `Test_Time (s)` without calendar timestamps.
   - Time-series stream records (`[filename_base]_timeseries.csv`) contain `Date_Time` and `Test_Time (s)`.
   - Applying the 2020 observation horizon requires capturing both cycle summaries (86 files) and timeseries streams (86 files), deriving the per-cell calendar start timestamp, and censoring observations timestamped past the 2020 cutoff.
3. If a definitive 2020 observation horizon cutoff date cannot be established from captured literature/metadata artifacts:
   `HALT_OBSERVATION_HORIZON_UNDETERMINED`

---

## 4. Audit Targets & Quantitative Objects

### Target A1 — Reconstructed Measured 80% EOL Multiset Reconstruction
For each test condition in Figure 2a containing observed 80% capacity crossings within the 2020 horizon:
1. Reconstruct cell-level discrete 80% crossing events ($N_{80}$ and cumulative $\text{EFC}_{80}$) directly from raw telemetry.
2. Form the reconstructed condition-level multiset:
   $$\mathcal{S}^{\text{P10}}_c = \left\{ \text{EFC}_{80,(1)}^{\text{P10}}, \dots, \text{EFC}_{80,(k)}^{\text{P10}} \right\}$$
3. Compare $\mathcal{S}^{\text{P10}}_c$ to the published digitized `+` marker multiset from Figure 2a:
   $$\mathcal{S}^{\text{pub}}_c = \left\{ \text{EFC}_{(1)}^{\text{pub}}, \dots, \text{EFC}_{(m)}^{\text{pub}} \right\}$$
4. **Overplotting & Cardinality Resolution ($m \neq k$):**
   - When visual marker cardinality matches reconstructed count ($m = k$), evaluate pair-wise sorted absolute differences under condition-specific tolerance $\tau_c$.
   - When visual marker cardinality does not match the reconstructed count ($m \neq k$) due to ink overplotting ($m < k$), visual ambiguity, or observation horizon truncation ($m > k$): assign `A1_REFERENCE_CARDINALITY_UNRESOLVED` for that condition.

### Target A2 — Condition-Level Measured vs. Extrapolated Partition Agreement
For each published Figure 2a condition, classify the condition based on telemetry observations within the 2020 horizon:
* `TELEMETRY_MEASURED_PRESENT` — At least one constituent replicate cell reached $\le 80\% Q_0$ within the 2020 horizon.
* `TELEMETRY_NO_OBSERVED_CROSSING` — No constituent replicate cell reached $\le 80\% Q_0$ within the 2020 horizon.

Compare this telemetry-derived classification to the frozen published reference classification:
* `MEASURED_PRESENT` — Figure 2a bar contains one or more individual `+` markers.
* `EXTRAPOLATED_ONLY` — Figure 2a bar contains no individual `+` markers (extrapolated EFC bar).

**Primary A2 Metric:** Condition-level mismatch count:
$$M_{\text{A2}} = \#\left\{ c \in \mathcal{C}_{\text{resolved}} : \text{Class}^{\text{P10}}(c) \neq \text{Class}^{\text{pub}}(c) \right\}$$

---

## 5. Frozen Reference Artifact Protocol (`figure2a_reference.csv`)

Prior to telemetry acquisition, create and commit `artifacts/figure2a_reference.csv` under the following protocol:

### 5.1 Two-Reader Partial-Blind Extraction
1. Condition bars and markers from Figure 2a are segmented and assigned randomized identifiers ($R001, R002, \dots$) with condition labels masked.
2. **Disclosed Constraint:** Due to y-axis scaling (LFP reaching ~9000 EFC vs NMC/NCA ~2500 EFC), magnitude discloses chemistry class; the blind prevents label-based shortcutting while acknowledging magnitude cues.
3. Two independent readers extract:
   - `plus_marker_count`
   - `plus_efc_positions`
   - `bar_efc_value`
   - `published_class` (`MEASURED_PRESENT`, `EXTRAPOLATED_ONLY`, `UNRESOLVED`)
4. Inter-reader discrepancies are flagged as `UNRESOLVED` without post-hoc consensus negotiation.

### 5.2 Condition-Specific Tolerance ($\tau_c$)
For each condition $c$, tolerance is established from graphical pixel resolution ($\delta_{\text{pixel}}$), inter-reader spread ($\Delta_{\text{reader}}$), and axis tick resolution ($\delta_{\text{axis}}$):
$$\tau_c = \max\left( \delta_{\text{pixel}}(c), \Delta_{\text{reader}}(c) \right) + \delta_{\text{axis}}$$

### 5.3 Trivial Baseline Pre-Declaration & Discrimination Gate
Before evaluating telemetry, compute the classification performance of three pre-declared fixed trivial baselines against `figure2a_reference.csv`:
1. **Majority-Class Baseline:** Predicts the single most frequent class (`MEASURED_PRESENT` or `EXTRAPOLATED_ONLY`) for all conditions.
2. **Direct Chemistry Prior (Baseline 2A):** Predicts `EXTRAPOLATED_ONLY` for all LFP conditions, and `MEASURED_PRESENT` for all NMC and NCA conditions.
3. **Inverted Chemistry Prior (Baseline 2B):** Predicts `MEASURED_PRESENT` for all LFP conditions, and `EXTRAPOLATED_ONLY` for all NMC and NCA conditions.

**A2 Discrimination Gate:** If any of the three pre-declared trivial baselines achieves $M_{\text{A2}} = 0$ (zero mismatches against the reference partition):
* Verdict: `Not Demonstrated — zero discriminatory power`
* A2 cannot be cited as evidence of telemetry reconstruction.

### 5.4 Condition-Specific A1 Power Analysis (M4)
Prior to telemetry acquisition, compute the within-condition marker spread $S_c = \max(\mathcal{S}^{\text{pub}}_c) - \min(\mathcal{S}^{\text{pub}}_c)$ for all multi-marker conditions in `figure2a_reference.csv`. If $S_c \le \tau_c$, the multiset structure provides zero distinguishing power between permutations; report the power classification in the reference table.

---

## 6. Computational Estimator Rules

### 6.1 EFC Operationalization Basis
* Candidate A (Discharge Throughput): $\text{EFC}_k = \frac{\sum_{i=1}^k Q^{\text{discharge}}_i}{Q_{\text{nominal}}}$
* Candidate B (Average Cycle Throughput): $\text{EFC}_k = \frac{\sum_{i=1}^k (Q^{\text{discharge}}_i + Q^{\text{charge}}_i)}{2 \times Q_{\text{nominal}}}$
*(Exact formulation to be pinned from article body prior to freeze).*

### 6.2 Baseline Capacity ($Q_0$)
* Candidate A: First RPT capacity check (0.5C, 0–100% SOC cycle).
* Candidate B: Cycle 1 discharge capacity under designated cycling protocol.
*(Exact formulation to be pinned from article body prior to freeze).*

### 6.3 80% EOL Crossing Rule ($N_{80}$)
Candidate formulations:
* Candidate A (Discrete Crossing): First integer cycle where $Q_k / Q_0 \le 0.80$.
* Candidate B (Linear Interpolation): Continuous linearly interpolated crossing between bounding cycles.
*(Exact formulation to be pinned from article body prior to freeze).*

For cells where $\min_k (Q_k / Q_0) > 0.80$ within the 2020 horizon:
Disposition: `A1_NOT_EVALUATED_NO_OBSERVED_CROSSING`

---

## 7. Controlled Verdict Definitions

| Target | Controlled Verdict | Criterion |
| :--- | :--- | :--- |
| **Target A1** | **Verified** | A published numerical table comparator exists in the article/SI, and reconstructed cell $\text{EFC}_{80}$ values match within frozen numerical tolerance $\tau_{\text{num}}$ for all resolved conditions. |
| | **Verified with Limitations** | Published comparator is graphical (digitized raster from Figure 2a), and reconstructed multiset $\mathcal{S}^{\text{P10}}_c$ matches digitized markers $\mathcal{S}^{\text{pub}}_c$ within graphical tolerance $\tau_c$ for all resolved conditions. |
| | **Not Verified** | Reconstructed $\text{EFC}_{80}$ values diverge from published comparator beyond the applicable frozen tolerance ($\tau_{\text{num}}$ for numerical table comparator, or $\tau_c$ for digitized graphical comparator). |
| | **Not Demonstrated** | Deposited telemetry or reference artifacts lack required resolution/fields to compute crossing, or cardinality cannot be resolved. |
| **Target A2** | **Verified** | Telemetry condition classification achieves $M_{\text{A2}} = 0$ mismatches against resolved reference conditions, AND passes the Discrimination Gate. |
| | **Not Verified** | Telemetry classification produces $M_{\text{A2}} \ge 1$ mismatches against resolved reference partition. |
| | **Not Demonstrated** | Reference partition unresolved or trivial baseline achieves $M_{\text{A2}} = 0$ (zero discriminatory power). |

> [!NOTE]
> **Comparator Provenance & Ceiling (SI Lookup Finding):**  
> Desk-level verification of the published Supplementary Information ([`stacks.iop.org/JES/167/120532/mmedia`](https://stacks.iop.org/JES/167/120532/mmedia)) confirms that SI artifacts contain exclusively Table SI (ICP-OES cathode composition) and Table SII (cell self-heating data). No machine-readable numerical table of Figure 2a cell-level $\text{EFC}_{80}$ values was published in the article or SI. Consequently, the public comparator for Target A1 is the digitized raster multiset from Figure 2a under tolerance $\tau_c$, establishing `Verified with Limitations` as the applicable ceiling for successful reconstruction against public artifacts.

---

## 8. Halting Invariants

Execution immediately halts with an explicit terminal disposition if any of the following occur:
* `HALT_LICENSE_NOT_RESOLVED`: Data acquisition attempted without authorized access.
* `HALT_OBSERVATION_HORIZON_UNDETERMINED`: 2020 cutoff date cannot be uniquely established.
* `HALT_EFC_OPERATIONALIZATION_UNDERDETERMINED`: Multiple conflicting EFC formulas remain unresolvable from literature.
* `HALT_Q0_UNDERDETERMINED`: $Q_0$ baseline definition cannot be uniquely determined from literature.
* `HALT_REFERENCE_PARTITION_NOT_FROZEN`: Reference CSV missing or uncommitted before telemetry acquisition.
* `HALT_POPULATION_ARTIFACT_MISMATCH`: Constituent cell missing from repository or schema incompatible.
* `HALT_RAW_ARTIFACT_INTEGRITY_FAIL`: Downloaded telemetry SHA256 digest differs from acquisition manifest.

---

## 9. Evidentiary Invariant (FAILURES.md #002 Enforced)

> Any text claimed to be literal source text or literal command output must originate directly from a preserved source artifact or captured command stream; manually reconstructed or synthetic evidence is strictly inadmissible.
