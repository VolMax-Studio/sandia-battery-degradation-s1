# Proposed representation-gate design — RB0 v1.0.2

Instrument: THROUGHPUT_REPRESENTATION_MAPPING_V1. Status: DESIGN_ONLY / NOT_IMPLEMENTED / NOT_EXECUTED. This is a distinct pre-RB1 gate, not an extra metric phase and not permission to inspect outcomes now.

## Order and objective

After RB0 approval and explicit gate authorization, freeze the representation decision procedure, source-protocol parameter mappings and reference-case plan. Determine whether throughput representation can be established from source evidence before investing in the role classifier. Review this result before role-classifier construction/freeze and its separate falsification. RB1 then requires separate GO; RB2–RB5 remain stopped.

No EFC, EFC80, retention threshold, Figure 2a comparison or full-corpus feasibility count is computed here. Review schema documentation, reset/counter semantics, interval associations and source protocol boundaries. Do not select cases or decision rules from capacity magnitudes, near-double values, threshold outcomes or model availability. Already reported anomalies may be documented as prior exposure, not presented as unseen validation cases.

## Proposed bounded reference cases

Fix 12 source-evidence cases, four for each chemistry (LFP, NCA, NMC). A case is an identified interval/channel and the documentation/adjacent interval evidence needed to decide representation; it is not a derived battery metric. Per chemistry cover the initial-block-to-working transition, an ordinary within-block interval, a documented reset/aggregation/overlap boundary if available, and a provenance/coverage ambiguity if available. Choose by documented protocol position, then canonical cell identity/source order; a capacity-value pattern is not a selection rule. Pin the case manifest before predictions.

These are requested evidence situations, not preassigned representation labels. If a required situation cannot be located independently of outcomes, retain a MISSING_SOURCE_CASE slot and report the scope limitation. Do not manufacture an overlap, aggregate or ambiguity to fill a category. Source states that have no independently resolvable cases remain UNTESTED and cannot receive a general validation claim. There is no requirement to fabricate every state in every chemistry.

## Independent reference and freeze

The author/specifier/implementer of the decision procedure is disqualified from producing or adjudicating its reference labels. This includes the author of this design. The operator must designate an adjudicator independent of instrument construction and blinded to predictions; no absolute institutional independence is asserted. Establish labels only from source evidence, sealing source locators, rationale, representation state or UNRESOLVED, interval coverage and channel applicability before predictions. Pin the procedure/parameter hashes and all reference-case hashes before a validation run. No reference labels are produced in this preparation.

## Decision vocabulary and report

Report PER_ROW_INCREMENT, AGGREGATED_DISJOINT_INCREMENT, OVERLAPPING_INCREMENT or REPRESENTATION_UNRESOLVED per channel/interval, with reason codes. Missing/unproven mapping yields unresolved; a cumulative counter requiring conversion is not automatically an increment. Existing THROUGHPUT_V1 requirements still govern valid-channel and coverage decisions. A documented disjoint aggregate may be counted once later; a near-double numeric value proves neither disjointness nor overlap.

The later gate record must contain case ID; source hashes and interval keys; frozen rule/parameter identity; independently adjudicated reference and evidence; predicted state and evidence; agreement/disagreement/abstention; untested states; and scope of any downstream prefix HALT. Record all cases, including missing/unknown ones. Do not calculate cumulative throughput to fill that last field: identify only the first unresolved/overlapping source interval and affected channels according to the contract.

A definite disagreement on a resolved reference is FAIL and remains immutable evidence, not a tuning signal. An unresolved reference or prediction cannot establish validity of that case; mark INCONCLUSIVE for its dependent path. PASS_SCOPED is permitted only for explicitly tested, independently resolved agreeing cases, with no definite disagreements, and must enumerate untested/unresolved scopes. It is not proof of universal increment semantics or all-86 feasibility. If the initial required transition is unresolved, HALT the affected EFC path; preserve any valid earlier prefix and do not relax the rule. Review determines whether any evidenced scope supports proceeding to role-classifier preparation; the gate itself grants no execution permission.

Do not repair, divide, subtract, drop, differencing-convert or tune cases to obtain a pass. Any proposed new procedure requires a new reviewed version and retains the previous gate record. Role classification cannot substitute for this validation, and this validation cannot substitute for the role classifier's 24-row test.

**STOP: proposed design only. No classifier implementation, reference labeling, gate execution or RB1–RB5 calculation is authorized by this revision.**
