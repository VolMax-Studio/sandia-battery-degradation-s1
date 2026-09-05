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

### Target A1-H — Horizon-Independent Replicate Multiset Reconstruction
Target A1-H evaluates numerical reproduction of 80% EOL crossing events on the subset of conditions where all constituent replicate cells reached $\le 80\% Q_0$ prior to the publication-era cutoff (`a1_reference_status = EXACT_CARDINALITY_MATCH`).

Because all constituent replicates in these conditions were observed crossing 80% retention in the published Figure 2a, their initial historical crossing events ($N_{80}$ and cumulative $\text{EFC}_{80}$) are immutable historical milestones independent of whether subsequent cycling continued after the 2020 publication date.

For each Target A1-H eligible condition ($c \in \mathcal{C}_{\text{A1-H}}$):
1. Reconstruct cell-level discrete crossing events ($N_{80}$ and cumulative $\text{EFC}_{80}$) directly from raw telemetry.
2. Form the reconstructed condition-level multiset:
   $$\mathcal{S}^{\text{P10}}_c = \left\{ \text{EFC}_{80,(1)}^{\text{P10}}, \dots, \text{EFC}_{80,(k)}^{\text{P10}} \right\}$$
3. Compare $\mathcal{S}^{\text{P10}}_c$ to the digitized `+` marker multiset from Figure 2a:
   $$\mathcal{S}^{\text{pub}}_c = \left\{ \text{EFC}_{(1)}^{\text{pub}}, \dots, \text{EFC}_{(k)}^{\text{pub}} \right\}$$
4. Evaluation is performed under the condition-specific optical tolerance $\tau_c$ across the full Specification-Robustness Envelope (§6).

### Target A2 — Full 33-Condition Partition Classification (Observation-Horizon Dependent)
For each of the 33 published Figure 2a conditions, classify the condition based on telemetry observations within the confirmed observation horizon:
* `TELEMETRY_MEASURED_PRESENT` — At least one constituent replicate cell reached $\le 80\% Q_0$ within the observation horizon.
* `TELEMETRY_NO_OBSERVED_CROSSING` — No constituent replicate cell reached $\le 80\% Q_0$ within the observation horizon.

Compare this telemetry-derived classification to the reference classification:
* `MEASURED_PRESENT` — Figure 2a bar contains one or more individual `+` markers (`a2_reference_status = RESOLVED`).
* `EXTRAPOLATED_ONLY` — Figure 2a bar contains zero individual `+` markers (`a2_reference_status = RESOLVED`).
* `UNRESOLVED` — Visually undecidable condition bar (`a2_reference_status = UNRESOLVED`).

**Target A2 Dependency Resolution:**
* If observation horizon is confirmed via host communication: evaluate condition mismatch count $M_{\text{A2}}$.
* If observation horizon remains undetermined from public artifacts: Target A2 resolves strictly to `Not Demonstrated — publication observation horizon unavailable from public evidence` without impeding the execution or verdicts of Target A1-H.

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

## 6. Specification-Robustness Envelope for Computational Estimators

Rather than selecting a single interpretation or conditioning execution on author confirmation, this preregistration formally defines an exhaustive **Specification-Robustness Envelope** spanning all candidate estimator formulations supported by the published text:

$$\mathcal{M} = \mathcal{Q}_0 \times \mathcal{N}_{80} \times \mathcal{EFC} \quad (|\mathcal{M}| = 3 \times 2 \times 2 = 12 \text{ candidate specifications})$$

### 6.1 Baseline Capacity Formulations ($\mathcal{Q}_0$)
* **$Q_0^{(A)}$ (First RPT Check):** Discharge capacity of the first 0.5C Reference Performance Test capacity-check cycle ($0$--$100\%$ SOC).
* **$Q_0^{(B)}$ (Mean RPT Check):** Arithmetic mean of discharge capacity across the three initial 0.5C RPT capacity-check cycles.
* **$Q_0^{(C)}$ (Final RPT Check):** Discharge capacity of the third (final) initial 0.5C RPT capacity-check cycle.

### 6.2 80% EOL Crossing Rule Formulations ($\mathcal{N}_{80}$)
* **$N_{80}^{(A)}$ (Discrete First Crossing):** Earliest cycle index $k$ such that $Q_k \le 0.80 \times Q_0$, with $\text{EFC}_{80} = \text{EFC}_k$.
* **$N_{80}^{(B)}$ (Linear Interpolation Crossing):** Continuous linear interpolation between bounding check cycles $(k-1, k)$ where $Q_k$ crosses $0.80 \times Q_0$.

### 6.3 Cumulative EFC Throughput Formulations ($\mathcal{EFC}$)
* **$\text{EFC}^{(A)}$ (Discharge Throughput Basis):**
  $$\text{EFC}_k = \frac{\sum_{i=1}^k Q^{\text{discharge}}_i}{Q_{\text{nominal}}}$$
* **$\text{EFC}^{(B)}$ (Two-Way Throughput Basis):**
  $$\text{EFC}_k = \frac{\sum_{i=1}^k (Q^{\text{discharge}}_i + Q^{\text{charge}}_i)}{2 \times Q_{\text{nominal}}}$$

---

## 7. Controlled Verdict Definitions

| Target | Controlled Verdict | Criterion |
| :--- | :--- | :--- |
| **Target A1-H** | **Verified (Full Robustness)** | Reconstructed multiset $\mathcal{S}^{\text{P10}}_c$ matches digitized Figure 2a markers $\mathcal{S}^{\text{pub}}_c$ within optical tolerance $\tau_c$ across **all 12 specifications** in $\mathcal{M}$ for all eligible exact-cardinality conditions. |
| | **Verified with Specification Sensitivity** | Reconstructed multiset matches within $\tau_c$ under a non-empty proper subset of specifications $\mathcal{M}' \subset \mathcal{M}$, identifying the exact implementation sensitivity of the published claim. |
| | **Not Verified** | Reconstructed multiset diverges from Figure 2a beyond tolerance $\tau_c$ across **all specifications** in $\mathcal{M}$. |
| | **Not Demonstrated** | Deposited telemetry lacks required channels to evaluate crossing events. |
| **Target A2** | **Verified** | Telemetry condition classification achieves $M_{\text{A2}} = 0$ mismatches against resolved reference conditions within confirmed observation horizon, AND passes the Discrimination Gate. |
| | **Not Verified** | Telemetry classification produces $M_{\text{A2}} \ge 1$ mismatches against resolved reference partition within confirmed observation horizon. |
| | **Not Demonstrated** | Observation horizon remains undetermined from public artifacts, reference partition unresolved, or trivial baseline achieves $M_{\text{A2}} = 0$. |

---

## 8. Halting Invariants

Execution immediately halts with an explicit terminal disposition if any of the following occur:
* `HALT_LICENSE_NOT_RESOLVED`: Data acquisition attempted without authorized access.
* `HALT_REFERENCE_PARTITION_NOT_FROZEN`: Reference CSV missing or uncommitted before telemetry acquisition.
* `HALT_POPULATION_ARTIFACT_MISMATCH`: Constituent cell missing from repository or schema incompatible.
* `HALT_RAW_ARTIFACT_INTEGRITY_FAIL`: Downloaded telemetry SHA256 digest differs from acquisition manifest.

---

## 9. Evidentiary & Governance Invariants (FAILURES #001, #002, #003 Enforced)

1. Any text claimed to be literal source text or literal command output must originate directly from a preserved source artifact or captured command stream; synthetic evidence is strictly inadmissible.
2. Hardcoded or simulated measurement dictionaries masquerading as optical readings are strictly prohibited. All graphical ground truth values must originate from verifiable raw pixel coordinates ($x_{\text{px}}, y_{\text{px}}$) transformed via reproducible code.
3. Git history is strictly append-only. Rewriting previously logged commits via `git commit --amend` or unapproved filter operations is prohibited.
