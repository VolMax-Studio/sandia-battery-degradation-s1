# PREREGISTRATION DRAFT v2: `sandia-battery-degradation-s1`

> [!IMPORTANT]
> **Status: DRAFT v2 (Not Frozen / Pre-Execution / Human Digitization Pending)**  
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

## 3. Core Invariant: Observation Horizon & Dual Stream Architecture

As captured in [`evidence/l0/source_pages/batteryarchive_study_summaries.html`](evidence/l0/source_pages/batteryarchive_study_summaries.html#L121):
> *"The dataset from Sandia National Labs used in the publication ... consists of commercial 18650 NCA, NMC, and LFP cells cycled to 80% capacity (although cycling is still ongoing)."*

Because laboratory cycling continued after the 2020 publication date:
1. **Observation Horizon Cutoff Requirement:** All Figure 2a comparison targets (Target A1 and Target A2) are evaluated strictly against observations recorded up to the study observation cutoff horizon.
2. **Horizon Invariant:** The publication date (`2020-09-02`) represents article appearance, not the physical laboratory data collection cutoff. Until a definitive observation horizon cutoff timestamp is formally confirmed via host communication ([`evidence/l0/governance/COMMUNICATIONS.md`](evidence/l0/governance/COMMUNICATIONS.md)) or primary metadata:
   `HALT_OBSERVATION_HORIZON_UNDETERMINED`
3. **Dual Telemetry Stream Requirement (172 Files Total):**
   - Cycle summary records (`[filename_base]_cycle_data.csv`) contain cycle metrics and elapsed `Test_Time (s)` without calendar timestamps.
   - Time-series stream records (`[filename_base]_timeseries.csv`) contain `Date_Time` and `Test_Time (s)`.
   - Applying the observation horizon requires capturing both cycle summaries (86 files) and timeseries streams (86 files), deriving the per-cell calendar start timestamp, and censoring observations timestamped past the confirmed cutoff.

---

## 4. Audit Targets & Quantitative Objects

### Target A1 — Reconstructed Measured 80% EOL Multiset Reconstruction
For each test condition in Figure 2a containing observed 80% capacity crossings within the observation horizon:
1. Reconstruct cell-level discrete 80% crossing events ($N_{80}$ and cumulative $\text{EFC}_{80}$) directly from raw telemetry.
2. Form the reconstructed condition-level multiset:
   $$\mathcal{S}^{\text{P10}}_c = \left\{ \text{EFC}_{80,(1)}^{\text{P10}}, \dots, \text{EFC}_{80,(k)}^{\text{P10}} \right\}$$
3. Compare $\mathcal{S}^{\text{P10}}_c$ to the digitized `+` marker multiset from Figure 2a:
   $$\mathcal{S}^{\text{pub}}_c = \left\{ \text{EFC}_{(1)}^{\text{pub}}, \dots, \text{EFC}_{(m)}^{\text{pub}} \right\}$$
4. **Decoupled Cardinality & Overplotting Resolution ($m \neq k$):**
   - When visual marker cardinality equals reconstructed count ($m = k$), the condition is evaluable for paired multiset reconstruction under condition-specific tolerance $\tau_c$ (`a1_reference_status = EXACT_CARDINALITY_MATCH`).
   - When visual marker cardinality does not match the reconstructed count ($m < k$ due to ink overplotting/mixed points, or $m > k$ due to anomalous counts exceeding metadata): assign `a1_reference_status = A1_REFERENCE_CARDINALITY_UNRESOLVED`. This excludes the condition from A1 paired multiset evaluation without invalidating condition-level classification for Target A2.

### Target A2 — Condition-Level Measured vs. Extrapolated Partition Agreement
For each published Figure 2a condition, classify the condition based on telemetry observations within the observation horizon:
* `TELEMETRY_MEASURED_PRESENT` — At least one constituent replicate cell reached $\le 80\% Q_0$ within the observation horizon.
* `TELEMETRY_NO_OBSERVED_CROSSING` — No constituent replicate cell reached $\le 80\% Q_0$ within the observation horizon.

Compare this telemetry-derived classification to the reference classification:
* `MEASURED_PRESENT` — Figure 2a bar contains one or more individual `+` markers (`a2_reference_status = RESOLVED`).
* `EXTRAPOLATED_ONLY` — Figure 2a bar contains zero individual `+` markers (`a2_reference_status = RESOLVED`).
* `UNRESOLVED` — Visually undecidable condition bar (`a2_reference_status = UNRESOLVED`).

**Primary A2 Metric:** Condition-level mismatch count across resolved conditions:
$$M_{\text{A2}} = \#\left\{ c \in \mathcal{C}_{\text{resolved}} : \text{Class}^{\text{P10}}(c) \neq \text{Class}^{\text{pub}}(c) \right\}$$

---

## 5. Reference Artifact Protocol (Human-Assisted Raw Pixel Capture Architecture)

To prevent synthetic or unverified measurements (FAILURES #002 / #003), `artifacts/figure2a_reference.csv` is generated exclusively from raw human-captured pixel coordinates via a deterministic transformation script:

### 5.1 Evidentiary Traceability Chain
1. **Source Image Manifest:** Pinned in [`artifacts/figure2a_source_manifest.json`](artifacts/figure2a_source_manifest.json) with publisher URL, DOI, exact crop SHA256 (`6426967ea7bdc106836273b034a236a04bc398e221d579a3aa66226232d7616b`), and dimensions (no copyrighted publisher binaries committed to git).
2. **Raw Pixel Coordinate Capture:** Interactive digitization session records operator identity, timestamp, axis calibration bounds ($y_{\text{px}, 0}, y_{\text{px}, \text{max}}$), and marker click coordinates $(x_{\text{px}}, y_{\text{px}})$ into `artifacts/figure2a_raw_pixel_clicks.json`. Canonical SHA-256 digest: `03f46254729dce6707f902f0c52aed438db36d1a682ebe629b644b78919909f0`.
3. **Deterministic Coordinate Transform:** [`evidence/l0/scripts/pixel_to_efc.py`](evidence/l0/scripts/pixel_to_efc.py) executes linear transformation from pixel space to physical EFC space, deriving $\tau_c$, spreads, and decoupled target statuses.
4. **Frozen-Reference Invariant:** No Figure 2a click coordinate, condition assignment, calibration rule, tolerance rule, or reference classification may be modified after reference commit `8c8f0d9` on the basis of subsequently observed BatteryArchive telemetry.

### 5.2 Mathematical Transformation & Optical Uncertainty
For each plot panel (Main LFP plot: $0$--$10{,}000\text{ EFC}$; Inset NMC/NCA plot: $0$--$3{,}000\text{ EFC}$):
$$\text{Scale} = \frac{\text{EFC}_{\text{max}}}{|y_{\text{px}, 0} - y_{\text{px}, \text{max}}|}, \quad \text{EFC}(y_{\text{px}}) = \text{EFC}_{\text{max}} \times \frac{y_{\text{px}, 0} - y_{\text{px}}}{y_{\text{px}, 0} - y_{\text{px}, \text{max}}}$$
$$\tau_c = (2 \cdot \text{Scale}) + \delta_{\text{axis}}$$

### 5.3 Decoupled Reference Schema (`figure2a_reference.csv`)
* `condition_id`: Condition identifier string
* `chemistry`: Cathode chemistry (`LFP`, `NMC`, `NCA`)
* `temperature_C`, `soc_min`, `soc_max`, `charge_C`, `discharge_C`: Condition parameters
* `replicate_count_metadata`: Replicate cell count from L0 metadata inventory
* `visual_plus_count`: Number of distinct `+` markers clicked in raw pixel capture
* `digitized_marker_efc`: Semicolon-delimited list of deterministically computed marker EFC values
* `cardinality_status`: `EXACT_CARDINALITY_MATCH`, `OVERPLOTTED_OR_MIXED`, `EXTRAPOLATED_MATCH`, `ANOMALOUS_COUNT_EXCEEDS_METADATA`, `CARDINALITY_UNRESOLVED`
* `a2_published_class`: `MEASURED_PRESENT`, `EXTRAPOLATED_ONLY`, `UNRESOLVED`
* `a2_reference_status`: `RESOLVED`, `UNRESOLVED`
* `a1_reference_status`: `EXACT_CARDINALITY_MATCH`, `A1_REFERENCE_CARDINALITY_UNRESOLVED`, `N/A_EXTRAPOLATED`
* `axis_efc_per_pixel`: Measured scale factor ($\delta_{\text{pixel}}$)
* `tau_c`: Optical uncertainty tolerance
* `within_marker_spread`: Within-condition marker spread $S_c = \max(\mathcal{S}^{\text{pub}}_c) - \min(\mathcal{S}^{\text{pub}}_c)$
* `a1_power_classification`: `HIGH_POWER` ($S_c > 2\tau_c$), `MODERATE_POWER` ($\tau_c < S_c \le 2\tau_c$), `LOW_POWER` ($S_c \le \tau_c$), `N/A_EXTRAPOLATED`

### 5.4 Trivial Baseline Pre-Declaration & Discrimination Gate
Before evaluating telemetry, compute the classification performance of three pre-declared fixed trivial baselines against the verified reference partition:
1. **Majority-Class Baseline:** Predicts the most frequent class for all conditions.
2. **Direct Chemistry Prior (Baseline 2A):** Predicts `EXTRAPOLATED_ONLY` for all LFP conditions, and `MEASURED_PRESENT` for all NMC and NCA conditions.
3. **Inverted Chemistry Prior (Baseline 2B):** Predicts `MEASURED_PRESENT` for all LFP conditions, and `EXTRAPOLATED_ONLY` for all NMC and NCA conditions.

**A2 Discrimination Gate:** If any pre-declared trivial baseline achieves $M_{\text{A2}} = 0$, Target A2 is flagged as `Not Demonstrated — zero discriminatory power`.

---

## 6. Computational Estimator Rules (Candidate Formulations / OPEN Status)

> [!NOTE]
> Aligned with `L0.md` criterion `G-L0-4B: OPEN`. Estimator formulations remain open candidate hypotheses pending host confirmation or admissible primary pinning prior to formal preregistration freeze.

### 6.1 Candidate EFC Operationalization Formulations
* **Candidate A (Discharge Throughput Basis):**
  $$\text{EFC}_k = \frac{\sum_{i=1}^k Q^{\text{discharge}}_i}{Q_{\text{nominal}}}$$
* **Candidate B (Average Cycle Throughput Basis):**
  $$\text{EFC}_k = \frac{\sum_{i=1}^k (Q^{\text{discharge}}_i + Q^{\text{charge}}_i)}{2 \times Q_{\text{nominal}}}$$

### 6.2 Candidate Baseline Capacity ($Q_0$) Formulations
* **Candidate A (Reference Performance Test):** $Q_0$ measured during the 0.5C RPT capacity check (3 cycles, 0–100% SOC).
* **Candidate B (Initial Cycling Capacity):** $Q_0$ defined as Cycle 1 discharge capacity under designated test protocol.

### 6.3 Candidate 80% EOL Crossing Rule ($N_{80}$) Formulations
* **Candidate A (Discrete First Crossing):** $N_{80} = \min \left\{ k \in \mathbb{N} : Q_k \le 0.80 \times Q_0 \right\}$, $\text{EFC}_{80} = \text{EFC}_{N_{80}}$.
* **Candidate B (Linear Interpolation Crossing):** Continuous linear interpolation between bounding cycles $(k-1, k)$.

For cells where $\min_k (Q_k / Q_0) > 0.80$ within the observation horizon:
Disposition: `A1_NOT_EVALUATED_NO_OBSERVED_CROSSING`

---

## 7. Controlled Verdict Definitions

| Target | Controlled Verdict | Criterion |
| :--- | :--- | :--- |
| **Target A1** | **Verified** | A published numerical table comparator exists in the article/SI, and reconstructed cell $\text{EFC}_{80}$ values match within frozen numerical tolerance $\tau_{\text{num}}$ for all resolved conditions. |
| | **Verified with Limitations** | Published comparator is graphical (digitized raster from Figure 2a), and reconstructed multiset $\mathcal{S}^{\text{P10}}_c$ matches digitized markers $\mathcal{S}^{\text{pub}}_c$ within graphical tolerance $\tau_c$ for all resolved conditions ($m=k$). |
| | **Not Verified** | Reconstructed $\text{EFC}_{80}$ values diverge from published comparator beyond the applicable frozen tolerance ($\tau_{\text{num}}$ for numerical table, or $\tau_c$ for digitized graphical comparator). |
| | **Not Demonstrated** | Deposited telemetry or reference artifacts lack required resolution/fields to compute crossing, or cardinality cannot be resolved ($m \neq k$). |
| **Target A2** | **Verified** | Telemetry condition classification achieves $M_{\text{A2}} = 0$ mismatches against resolved reference conditions, AND passes the Discrimination Gate. |
| | **Not Verified** | Telemetry classification produces $M_{\text{A2}} \ge 1$ mismatches against resolved reference partition. |
| | **Not Demonstrated** | Reference partition unresolved or trivial baseline achieves $M_{\text{A2}} = 0$ (zero discriminatory power). |

> [!NOTE]
> **Comparator Ceiling:** Because SI lookup confirmed no machine-readable numerical table was published in the study or SI, the public comparator for Target A1 is the digitized raster multiset from Figure 2a under tolerance $\tau_c$, establishing `Verified with Limitations` as the applicable ceiling for successful reconstruction against public artifacts.

---

## 8. Halting Invariants

Execution immediately halts with an explicit terminal disposition if any of the following occur:
* `HALT_LICENSE_NOT_RESOLVED`: Data acquisition attempted without authorized access.
* `HALT_OBSERVATION_HORIZON_UNDETERMINED`: Observation horizon cutoff date cannot be established.
* `HALT_EFC_OPERATIONALIZATION_UNDERDETERMINED`: EFC formulation remains unpinned at freeze.
* `HALT_Q0_UNDERDETERMINED`: $Q_0$ baseline definition remains unpinned at freeze.
* `HALT_REFERENCE_PARTITION_NOT_FROZEN`: Reference CSV missing or uncommitted before telemetry acquisition.
* `HALT_POPULATION_ARTIFACT_MISMATCH`: Constituent cell missing from repository or schema incompatible.
* `HALT_RAW_ARTIFACT_INTEGRITY_FAIL`: Downloaded telemetry SHA256 digest differs from acquisition manifest.

---

## 9. Evidentiary & Governance Invariants (FAILURES #001, #002, #003 Enforced)

1. Any text claimed to be literal source text or literal command output must originate directly from a preserved source artifact or captured command stream; synthetic evidence is strictly inadmissible.
2. Hardcoded or simulated measurement dictionaries masquerading as optical readings are strictly prohibited. All graphical ground truth values must originate from verifiable raw pixel coordinates ($x_{\text{px}}, y_{\text{px}}$) transformed via reproducible code.
3. Git history is strictly append-only. Rewriting previously logged commits via `git commit --amend` or unapproved filter operations is prohibited.
