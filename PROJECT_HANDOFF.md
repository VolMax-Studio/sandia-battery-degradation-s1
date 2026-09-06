# Project Handoff

## Identity

Project: sandia-battery-degradation-s1
Repository: VolMax-Studio/sandia-battery-degradation-s1
Branch: main
Phase: execution_preparation
Preregistration commit: de01a7e (Target A1-H & Specification Envelope Frozen)
Deadline: 2026-09-21T20:00:00+02:00 (HOST_INPUT_CUTOFF)

## Phase

Phase 2 Execution Preparation — State: WAITING_FOR_SUPPORTED_ACQUISITION_ROUTE (Engine Frozen: 4007a07 / Run: run-002-a1h / Required Inputs: 12 cells, SHA256: e044432a...1128)

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

## Gate Status & Governance Clearance

* **Gate model/person:** NONE — Claude retired from this instance.
* **Ratification Status:** RATIFIED — HOST_INPUT_CUTOFF FREEZE on tree `f2b50e2` (Ivan, 2026-09-06T10:00:43+02:00).
* **G-L0-5A (Analytical Use):** PASS — Public analytical-use basis established; host bulk access requested from info@batteryarchive.org.
* **G-L0-5B (Redistribution):** PROHIBITED_PENDING_CONFIRMATION — Raw BatteryArchive files MUST NOT be redistributed in public repository. Repository contains only acquisition manifests, hashes, code, and derived audit outputs.
* **Acquisition State:** WAITING_FOR_SUPPORTED_ACQUISITION_ROUTE (FINDING-L0-ACCESS-DRIFT-001 in `evidence/l0/findings/ACCESS_DRIFT.md`).
* **Required Inputs Manifest:** `runs/run-002-a1h/a1_h_required_inputs.json` (SHA256: `e044432a2f14307d987ecde3695d9380416ab0192e8716848633697e9c3f1128`; 5 conditions, 12 cells).
* **Target A1-H Execution:** UNBLOCKED (Evaluates 5 exact-cardinality conditions / 12 cells across 12-model specification envelope).
* **Target A2 Execution:** AWAITING_AUTHORITATIVE_HORIZON_BOUNDARY (F35: explicit cutoff date, per-cell censoring index, or frozen snapshot; 11 marker-deficit conditions subject to composite label limitation).
* **Git State Construction Rule:** `evidence/l0/governance/git_state.txt` records preceding commit milestone by construction and does not self-reference the containing commit.
* **Host Input Cutoff:** `2026-09-21T20:00:00+02:00` (Europe/Belgrade) / `12:00 America/Denver` (9.5 U.S. business days post-Labor-Day).
* **Late Evidence Policy:** SUPPLEMENTAL_ONLY (Post-cutoff evidence opens `run-003-a1h-late-host-evidence`; does not supersede `run-002`).

## Next Single Action

Await host response/bulk transfer from info@batteryarchive.org by 2026-09-21T20:00:00+02:00, ingest raw cycler telemetry files for the 12 required cells into run-002-a1h, generate raw acquisition manifest, and execute the frozen A1-H 12-model verification engine.
