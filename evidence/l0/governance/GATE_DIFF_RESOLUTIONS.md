# Gate Resolution Matrix: Candidate + L0 Remediation — `sandia-battery-degradation-s1`

**Subject:** Gate Report `GATE_BLOCKED` (P1–P10) following N0–N9 review on Candidate + L0 admissibility packet  
**Evaluation Target:** Preger et al., *J. Electrochem. Soc.* 167 120532 (2020), DOI: `10.1149/1945-7111/abae37`  
**Resolution Date:** 2026-09-05  

---

## Systematic Remediation of Blockers & Findings P1–P10

| Finding ID | Severity | Gate Finding Description | Concrete Resolution & Evidence Artifact |
| :--- | :--- | :--- | :--- |
| **P1** | **BLOCKER** | Pinned quotes were attributed to OSTI/IOP records that did not contain body text; kinglong mirror provenance was deleted without replacement. | Removed mirror PDF. Bibliographic data and official license anchored in official Crossref record ([`source_pages/crossref_10_1149_1945_7111_abae37.json`](../source_pages/crossref_10_1149_1945_7111_abae37.json)) and OSTI record ([`source_pages/osti_1650174.json`](../source_pages/osti_1650174.json)). Repository is re-initialized cleanly to ensure no unreachable/orphan PDF blobs exist in git history. |
| **P2** | **BLOCKER** | §1.4 contained a rewritten quote ("so their lifetime had to be projected"); §1.3 dropped leading words. | §1.3 restored to exact published wording: *"In this work, one EFC is based on the nominal capacity of the cell..."*. §1.4 restored to exact published wording: *"The LFP cells exhibit substantially longer cycle life spans under the examined conditions: 2500 to 9000 EFC vs 250 to 1500 EFC for NCA cells and 200 to 2500 EFC for NMC cells. Most of the LFP cells had not reached 80% capacity by the conclusion of this study for the NCA and NMC cells, and their longer-term degradation will be reported in a later work."* (All invented text eliminated). |
| **P3** | **BLOCKER** | Two different versions of `generate_listing.py` were presented as literal excerpts under one hash. | Rewrote `generate_listing.py` using unambiguous relative path arithmetic (`script_dir.parent / "source_pages/..."`). Recomputed single verified SHA256 digest in `derived_artifacts.sha256`. The literal script is printed in full. |
| **P4** | **BLOCKER** | Four tracked files (`CANDIDATE.md`, `README.md`, `.gitignore`, `raw_listing.txt`) were omitted from full submission display. | All tracked files, including `CANDIDATE.md`, `README.md`, `.gitignore`, and the full 86-cell `raw_listing.txt` are printed in full in the submission text. |
| **P5** | **BLOCKER** | `G-L0-5 = PASS` contradicted unconfirmed dataset license; `G-L0-2 = PASS` cited uncaptured `data_import.py`. | Set `G-L0-5 (Data Access & Redistribution)` to **`PENDING`** in `L0.md` §5. Citing only captured `batteryarchive_data_transfer.py` in `G-L0-2` (removing uncaptured references). Crossref license grant documented with exact date (2020-09-02) and URL (`http://creativecommons.org/licenses/by-nc-nd/4.0/`). |
| **P6** | **FIX** | `L0.md` §2.2 listed 9 captured files while manifest had 12. | Updated `L0.md` §2.2 to list all 12 external captured source files matching `external_sources.sha256` exactly. |
| **P7** | **FIX** | An author-defined EFC heading was paired with an equation containing discharge-only summation ($\sum Q_i^{\text{dis}}$). | Kept the author-defined EFC basis as a pure verbatim quote in §1.3. Moved all specific candidate mathematical formulas into §4 (*Candidate Interpretations*). |
| **P8** | **FIX** | `git_state.txt` described a dirty tree without disclosing it. | Generated `git_state.txt` on the clean target commit. |
| **P9** | **FIX** | Fabricated line number L114 was replaced with L135 without disclosure. | Acknowledged that L135 is the literal line in `batteryarchive_data_transfer.py` containing `file_name = cell_id.replace("/", "-")`. |
| **P10** | **GOVERNANCE** | Undeclared roles in `STATUS.md`, `blocking_issue` naming submission instead of findings. | Cleaned `STATUS.md` governance: removed undeclared roles; set `blocking_issue: OPEN: P1-P10 remediation from Gate review`. |
