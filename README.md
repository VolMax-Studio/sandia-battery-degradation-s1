# sandia-battery-degradation-s1

**Independent Computational Audit of the Sandia National Laboratories Commercial Li-Ion Battery Degradation Dataset**

[![Phase: Candidate L0](https://img.shields.io/badge/Phase-Candidate%20L0-yellow)](#phase)
[![Claimant: Sandia National Labs](https://img.shields.io/badge/Claimant-Sandia%20%2F%20DOE-blue)](#provenance)
[![Paper: JES 2020](https://img.shields.io/badge/DOI-10.1149%2F1945--7111%2Fabae37-blue)](https://doi.org/10.1149/1945-7111/abae37)
[![Data: BatteryArchive.org](https://img.shields.io/badge/Data-BatteryArchive.org-brightgreen)](https://www.batteryarchive.org)

---

## 1. Overview

This repository hosts the candidate evaluation, L0 provenance specification, and reproducibility audit for the commercial battery cycling study conducted by Sandia National Laboratories:

> Y. Preger, H. M. Barkholtz, A. Fresquez, D. L. Campbell, B. W. Juba, J. Romàn-Kustas, S. R. Ferreira, and B. Chalamala, *"Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions"*, **Journal of The Electrochemical Society** 167, 120532 (2020), pages 120532-1 to 120532-13. DOI: [`10.1149/1945-7111/abae37`](https://doi.org/10.1149/1945-7111/abae37). OSTI: [`1650174`](https://www.osti.gov/biblio/1650174).

---

## 2. Target Scope (Candidate Target A)

- **Domain:** Physical Electrochemical Battery Degradation.
- **Chemistries:** LFP (A123 Systems), NMC (LG Chem), NCA (Panasonic) 18650 cylindrical cells.
- **Target A1 (Measured EOL Reconstruction):** Reconstruct discrete 80% capacity retention crossing events ($N_{80}$, cumulative $\text{EFC}_{80}$) directly from deposited BatteryArchive galvanostatic cycler telemetry.
- **Target A2 (Cohort Classification):** Cleanly separate measured 80% crossing cells from projected/extrapolated cells based on published artifact criteria.
- **Data Source:** Raw multi-year cycler time-series and cycle summary data archived at [BatteryArchive.org](https://www.batteryarchive.org).

---

## 3. Governance Phase

Current phase: **Candidate Evaluation & L0 Source Hunt (Pre-Preregistration)**.  
No numerical analysis, tolerance setting, or analytical execution is authorized until formal L0 Gate review by Claude and Operator approval.
