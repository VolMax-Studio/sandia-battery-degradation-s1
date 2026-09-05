# Pinned Public Claim Specification: `sandia-battery-degradation-s1`

**Phase:** Phase 0 (Candidate L0 Discovery & Claim Pinning)  
**Publication:** Yuliya Preger, Heather M. Barkholtz, Armando Fresquez, Daniel L. Campbell, Benjamin W. Juba, Jessica Romàn-Kustas, Summer R. Ferreira, Babu Chalamala, *"Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions"*, *Journal of The Electrochemical Society* 167, 120532 (2020), pages 120532-1 to 120532-13.  
**DOI:** [`10.1149/1945-7111/abae37`](https://doi.org/10.1149/1945-7111/abae37)  
**OSTI Identifier:** `1650174` ([osti.gov/biblio/1650174](https://www.osti.gov/biblio/1650174))  
**Data Deposit:** [BatteryArchive.org](https://www.batteryarchive.org) (Sandia National Laboratories / SNL Dataset)  
**Bibliographic Evidence Records:** Official US DOE/SNL OSTI Record 1650174 ([`evidence/l0/source_pages/osti_1650174.json`](evidence/l0/source_pages/osti_1650174.json)) & Official Crossref DOI Metadata ([`evidence/l0/source_pages/crossref_10_1149_1945_7111_abae37.json`](evidence/l0/source_pages/crossref_10_1149_1945_7111_abae37.json)).

---

## 1. Verbatim Published Texts

### 1.1 Verbatim Abstract Text (Preger et al. 2020, p. 120532-1; OSTI 1650174):
> *"Energy storage systems with Li-ion batteries are increasingly deployed to maintain a robust and resilient grid and facilitate the integration of renewable energy resources. However, appropriate selection of cells for different applications is difﬁcult due to limited public data comparing the most commonly used off-the-shelf Li-ion chemistries under the same operating conditions. This article details a multi-year cycling study of commercial LiFePO4 (LFP), LiNixCoyAl1−x−yO2 (NCA), and LiNixMnyCo1−x−yO2 (NMC) cells, varying the discharge rate, depth of discharge (DOD), and environment temperature. The capacity and discharge energy retention, as well as the round-trip efﬁciency, were compared. Even when operated within manufacturer speciﬁcations, the range of cycling conditions had a profound effect on cell degradation, with time to reach 80% capacity varying by thousands of hours and cycle counts among cells of each chemistry. The degradation of cells in this study was compared to that of similar cells in previous studies to identify universal trends and to provide a standard deviation for performance. All cycling ﬁles have been made publicly available at batteryarchive.org, a recently developed repository for visualization and comparison of battery data, to facilitate future experimental and modeling efforts."*

### 1.2 Verbatim Figure 2 Caption (Preger et al. 2020, p. 120532-4):
> *"Figure 2. (a) Equivalent full cycle (EFC) count at 80% capacity for all cells and cycling conditions. Each bar represents the average EFC for all cells cycled at that condition. The values for individual cells are noted with a “+”. If a bar does not include values for individual cells, then those cells have not yet reached 80% capacity and the indicated EFC is extrapolated based on the present degradation rate for those cells. (b) Cumulative discharge energy at 80% capacity for all cells and cycling conditions. Each bar represents the average discharge energy for all cells cycled at that condition. (c) Round-trip efﬁciency (RTE) for all cells and cycling conditions. Each bar represents the average initial RTE for all cells cycled at that condition. The RTE at the end of the study is indicated with a dot. If a bar does not include a dot, then those cells have not yet reached 80% capacity."*

### 1.3 Verbatim Author Definition of EFC Basis (Preger et al. 2020, Section *Results and Discussion — Capacity and Energy Fade*, p. 120532-4):
> *"In this work, one EFC is based on the nominal capacity of the cell. Therefore, for each cell, the total capacity throughput was divided by the nominal capacity to get the total equivalent full cycle count."*

### 1.4 Verbatim Published EFC Ranges & Lifetime Statement (Preger et al. 2020, p. 120532-4):
> *"The LFP cells exhibit substantially longer cycle life spans under the examined conditions: 2500 to 9000 EFC vs 250 to 1500 EFC for NCA cells and 200 to 2500 EFC for NMC cells. Most of the LFP cells had not reached 80% capacity by the conclusion of this study for the NCA and NMC cells, and their longer-term degradation will be reported in a later work."*

---

## 2. Precise Stable Article Locators

| Item | Stable Journal Locator | Description |
| :--- | :--- | :--- |
| **Abstract & Scope** | `J. Electrochem. Soc. 167 120532`, p. 120532-1 | Public data availability at BatteryArchive.org and multi-chemistry comparison. |
| **Tested Battery Specifications** | `J. Electrochem. Soc. 167 120532`, Section *Experimental Conditions*, p. 120532-1 to 120532-2, Table I | A123 Systems APR18650M1A (LFP, 1.1 Ah), Panasonic NCR18650B (NCA, 3.2 Ah), LG Chem 18650HG2 / commercial (NMC, 3.0 Ah). |
| **Experimental Test Matrix** | `J. Electrochem. Soc. 167 120532`, Section *Experimental Conditions*, p. 120532-3, Table II | Matrix of DOD (0–100%, 20–80%, 40–60%), temperature (15°C, 25°C, 35°C), discharge rate (0.5C to 3C; NCA 3C excluded). |
| **Figure 2a (EFC at 80% Capacity)** | `J. Electrochem. Soc. 167 120532`, p. 120532-4 | Condition-level average bars with individual cell `+` markers and extrapolated bars. |
| **EFC Definition & Text Ranges** | `J. Electrochem. Soc. 167 120532`, Section *Results and Discussion*, p. 120532-4 to 120532-5 | Capacity throughput / nominal capacity, and per-chemistry EFC intervals. |
| **Figure 2c (Round-Trip Efficiency)** | `J. Electrochem. Soc. 167 120532`, p. 120532-4 | Initial and end-of-study RTE values. |

---

## 3. Flagship Audit Target Specification

* **Target A1 (Measured 80% EOL Event Reconstruction):**  
  Reconstruct the discrete 80% capacity retention crossing events ($N_{80}$ and cumulative $\text{EFC}_{80}$) directly from the deposited raw BatteryArchive time-series and cycle summary records for all measured cells.

* **Target A2 (Measured vs. Extrapolated Cohort Separation):**  
  Classify all 86 deposited cells into the measured cohort (cells that reached $\le 80\%$ initial capacity during the study) versus the projected/extrapolated cohort (cells that remained $> 80\%$ capacity at study termination), testing whether the published Figure 2a partition is deterministically reproduced from the telemetry.

---

## 4. Candidate Computational Interpretations — NOT YET FROZEN (To Be Pinned in Preregistration)

> [!NOTE]
> The author-defined basis for EFC is the total capacity throughput divided by nominal capacity. The exact computational implementation rules below represent candidate operationalizations for Phase 1 Preregistration and remain **OPEN**.

1. **Candidate Throughput Formulations:**
   - *Option A (Discharge-only throughput):* $\text{EFC}_k = \frac{\sum_{i=1}^k Q^{\text{discharge}}_i}{Q_{\text{nominal}}}$
   - *Option B (Average cycle throughput):* $\text{EFC}_k = \frac{\sum_{i=1}^k (Q^{\text{discharge}}_i + Q^{\text{charge}}_i)}{2 \times Q_{\text{nominal}}}$

2. **Baseline Discharge Capacity ($Q_0$ Candidate Options):**
   - *Option A:* Reference Performance Test (RPT) capacity check (3 charge/discharge cycles at 0.5C, 0–100% SOC).
   - *Option B:* Cycle 1 discharge capacity under designated test protocol.

3. **Discrete 80% Crossing ($N_{80}$ Candidate Options):**
   - *Option A:* First integer cycle where $Q_k \le 0.80 \times Q_0$.
   - *Option B:* Continuous linearly interpolated crossing between adjacent bounding cycles.

4. **Condition-Level Aggregation:**
   - Arithmetic mean of replicate cell $\text{EFC}_{80}$ values for each test condition in Table II.
