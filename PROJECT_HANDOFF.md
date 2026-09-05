# Project Handoff

## Identity

Project: sandia-battery-degradation-s1
Repository: VolMax-Studio/sandia-battery-degradation-s1
Branch: main
Phase: preregistration_drafting
Preregistration commit: None (Pre-Preregistration Drafting Phase)
Deadline: TBD (Set by Operator)

## Phase

Phase 1 Preregistration Drafting — Execution State: NOT AUTHORIZED (L0 Complete / Gate PASS)

Portfolio status: ACTIVE / FLAGSHIP INSTANCE

Architecture:
External physical laboratory telemetry audit of Sandia National Laboratories (SNL) commercial battery degradation dataset (Preger et al., J. Electrochem. Soc. 2020 167 120532, OSTI 1650174) hosted at BatteryArchive.org.

Audit Class:
External public-artifact audit.
Claimant: Sandia National Laboratories (SNL) / US Department of Energy (DOE).

## Exact Claim Under Test (Candidate Target A)

Verbatim Published Abstract (Preger et al. 2020, J. Electrochem. Soc. 167 120532, p. 120532-1; OSTI 1650174):
"Energy storage systems with Li-ion batteries are increasingly deployed to maintain a robust and resilient grid and facilitate the integration of renewable energy resources. However, appropriate selection of cells for different applications is difﬁcult due to limited public data comparing the most commonly used off-the-shelf Li-ion chemistries under the same operating conditions. This article details a multi-year cycling study of commercial LiFePO4 (LFP), LiNixCoyAl1−x−yO2 (NCA), and LiNixMnyCo1−x−yO2 (NMC) cells, varying the discharge rate, depth of discharge (DOD), and environment temperature. The capacity and discharge energy retention, as well as the round-trip efﬁciency, were compared. Even when operated within manufacturer speciﬁcations, the range of cycling conditions had a profound effect on cell degradation, with time to reach 80% capacity varying by thousands of hours and cycle counts among cells of each chemistry. The degradation of cells in this study was compared to that of similar cells in previous studies to identify universal trends and to provide a standard deviation for performance. All cycling ﬁles have been made publicly available at batteryarchive.org, a recently developed repository for visualization and comparison of battery data, to facilitate future experimental and modeling efforts."

Quantitative Object (Figure 2a, p. 120532-4):
- Target A1: Deterministic reconstruction of measured cell-level 80% capacity retention crossing events ($N_{80}$ and $\text{EFC}_{80}$).
- Target A2: Deterministic classification of measured cohort vs projected/extrapolated cohort.

Detailed Claim Specification: CLAIM_PIN.md

## Evidence Boundary

Public artifacts documented in ARTIFACTS.json, external_sources.sha256, and derived_artifacts.sha256:
- Authoritative OSTI Record 1650174 (`source_pages/osti_1650174.json`).
- Crossref DOI Metadata Record (`source_pages/crossref_10_1149_1945_7111_abae37.json`).
- BatteryArchive.org Sandia National Laboratories dataset metadata (`batteryarchive_metadata.csv`).
- Complete cell inventory: 86 SNL cells cataloged in `evidence/l0/raw_listing.txt`.
- Captured web pages in `evidence/l0/source_pages/`.

## Gate Status

Gate model/person: Claude
Gate outcome: PASS (Candidate L0 Admissibility Complete)
Blocking findings: None. G-L0-5 pending dataset redistribution confirmation (no raw data download permitted until resolved).

## Next Single Action

Formulate Phase 1 preregistration (EFC estimator pinning, Q0/N80 crossing rules, and Figure 2a visual ground truth reference partition).
