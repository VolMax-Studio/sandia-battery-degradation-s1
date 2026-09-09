# THROUGHPUT_REPRESENTATION_MAPPING_V1 — rules for freeze review

Version: 1.1 preparation candidate. Governing contract: ratified RB0 v1.0.3 at fa61d1ea5dcdc650dae03e5b6a7186b0cfc4ea74, with the separately recorded Operator flow interpretation. Status: PREPARED_FOR_OPERATOR_REVIEW; NOT FROZEN FOR EXECUTION. This document and its decision table specify an instrument; no implementation, predictions, labels or gate execution are delivered.

## Input unit and evidence contract

Decide per source interval and per channel (charge Ah, discharge Ah), retaining source-member SHA and data-row key. Preserve row order and original bytes. Inputs to the eventual instrument are independently traceable source facts, not the sealed reference answers: source field definition, units, increment-versus-counter meaning, reset semantics, operation coverage, sample/row association, interval endpoints, overlap/disjointness evidence, and directional-flow evidence. Every fact is TRUE/FALSE/UNKNOWN with an exact source locator and rule/parameter identity. Absence is UNKNOWN, not FALSE. These facts must be pinned before predictions and may not be populated by copying the adjudicator's representation/flow label.

Schema names alone do not establish increments. Monotonic values, near-double capacity, the apparent usefulness of an EFC curve, threshold outcomes, Figure 2a, or expected feasibility cannot establish interval semantics. Do not infer scientific roles. Do not execute the public SoH/EFC utility or adopt its heuristic around empty cycles. No source-protocol statement found so far is represented as a complete counter/reset specification.

## Representation decision order (specification only)

Apply in this order for each interval/channel; an unresolved result is not a guessed valid increment.

1. Unmatched source identities, missing units or contradictory/unknown interval association: REPRESENTATION_UNRESOLVED, with the specific missing fact. This is not a source-corruption verdict merely because documentation is incomplete.
2. If documentation/source association definitively establishes reuse of the same increment in overlapping intervals: OVERLAPPING_INCREMENT. Mere overlapping wall-clock bounds without unambiguous increment identity do not prove duplicated throughput.
3. If counter semantics are cumulative or require conversion/reset reconstruction unsupported by RB0: REPRESENTATION_UNRESOLVED / UNSUPPORTED_COUNTER_REPRESENTATION. Do not difference counters or subtract another row.
4. If source evidence establishes complete per-row incremental coverage of exactly one operation, with no overlap or missing coverage: PER_ROW_INCREMENT.
5. If source evidence establishes a complete aggregate of multiple operations, mutually disjoint both within the aggregate and against adjoining represented intervals: AGGREGATED_DISJOINT_INCREMENT. A large value is not such evidence; a valid disjoint aggregate is counted only once if later scientific execution is authorized.
6. Otherwise: REPRESENTATION_UNRESOLVED / INCREMENT_REPRESENTATION_UNRESOLVED or OPERATION_BOUNDARY_AGGREGATION_UNRESOLVED, as supported by the evidence gap.

PER_ROW_INCREMENT/AGGREGATED_DISJOINT_INCREMENT are representation decisions, not automatic throughput admission: finite/nonnegative values, valid channel units and complete coverage are still required by RB0. OVERLAPPING_INCREMENT or unresolved representation halts the affected future prefix at that interval; valid earlier intervals are retained. No EFC prefix is calculated in preparation or in representation feasibility.

## Flow-state sub-decision inside the same instrument

Flow determination is part of this instrument and shares its freeze/reference/gate obligations. It is neither a third untested instrument nor scientific role classification. Its input scope is the exact same source interval and complete protocol/timeseries coverage, with source-established current polarity and documented acquisition resolution/coverage. No current threshold is borrowed from the role classifier's ±0.05 corroboration condition.

- BIDIRECTIONAL_FLOW: direct source evidence establishes charge-direction and discharge-direction flow in the complete interval.
- CHARGE_DIRECTION_ONLY: direct evidence establishes charge-direction flow and no discharge-direction flow over the complete interval.
- NO_FLOW: direct evidence establishes neither directional flow over the complete interval.
- FLOW_STATE_UNRESOLVED: required polarity, coverage, resolution or directional facts are absent/contradictory, or no listed state can be justified. This vocabulary is retained exactly from the Operator interpretation; do not add a discharge-only class silently. A supported directional-channel fact can still be retained as evidence, but the instrument must not force an interval into a different named state.

A zero code in a channel or a gap in samples is not proof of no flow. Exact zero-current source codes require documented meaning and complete coverage; unknown resolution, inactive logging periods or unestablished sample association cannot justify TRUE_ZERO_THROUGHPUT. No noise/deadband threshold, sampling cadence or endpoint-inclusion convention is invented in this preparation. Missing source-bound parameters remain null and yield unresolved decisions under the later frozen rules.

TRUE_ZERO_THROUGHPUT is justified per channel only when the measured zero and independent direct evidence of no directional flow apply to that channel over its complete covered interval. NO_FLOW can justify both channels; CHARGE_DIRECTION_ONLY can justify zero discharge. This does not by itself authorize measured charge validity, capacity-check status or Q_k eligibility. A valid measured throughput increment can remain valid with ROLE_UNDETERMINED, under the existing orthogonality rule.

## Gate decision specification and safeguards

The later gate compares instrument output against independently sealed reference representation AND flow states, not against labels supplied by any author/specifier/implementer of these rules. All instrument-construction contributors, including the contract author and contributing reviewers, are disqualified from reference adjudication. No adjudicator is designated here.

For every chemistry in PASS_SCOPED, both a documented initial-block-to-working transition and an ordinary within-block interval must have resolved independent references and definite agreeing predictions. Require zero definite disagreements among all resolved cases in that claimed chemistry; at least six mandatory agreements for all three chemistries. Empty/unresolved-only scope cannot pass. Missing/abstained mandatory cases exclude that chemistry. Correctly recognizing an overlap still halts its dependent throughput path.

Before execution, the final twelve-case plan must cover at least one independently resolved NO_FLOW and one CHARGE_DIRECTION_ONLY case where source-verifiable candidates can be established without outcome selection. Flow coverage uses two explicitly reserved optional slots and must be source-row disjoint from all six mandatory windows; the sample size remains twelve. Optional chemistry assignments follow source identity and preserve the final four-per-chemistry requirement. If coverage cannot be established, record UNTESTED/UNRESOLVED explicitly and do not claim validation of the missing flow/zero scope. Representation PASS_SCOPED never silently validates untested flow decisions; report the two coverage scopes separately. Definite flow disagreement is a finding of this instrument and is included in its chemistry-scoped disagreement record.

No labels, predictions, disagreements, PASS/FAIL/INCONCLUSIVE outcomes or all-86 feasibility count have been generated. No tuning on the reference sample, no substituted cases after predictions and no numerical repair is permitted. Any pre-execution completion/reassignment of the candidate manifest requires a versioned rationale independent of outcomes and an updated hash before final freeze.

## Stop and readiness

This is preparation for review, not execution freeze. The current manifest has twelve slots: six source-anchored candidate windows (transition [3,4], ordinary [5,6], mutually disjoint) with unconfirmed protocol strata, two explicit optional flow reservations and four optional halt-evidence reservations, all six still missing source-case locations. Optional chemistry assignment remains pending; final four-per-chemistry quotas are unchanged. NO_FLOW and CHARGE_DIRECTION_ONLY reference coverage is NOT_ESTABLISHED. These facts neither establish absence of candidates in the corpus nor satisfy the gate. The source-bound resolution/cadence/endpoint facts and qualified independent adjudicator remain unestablished. Review must decide how to complete or accept an explicitly limited evidence scope before any execution authorization. RB1–RB5 remain unauthorized.

Preparation v1.1 readiness specifically records NMC early-row/A1-H-target exposure and untested prefix-stop branches. Any later NMC scope must carry the specific exposure limitation; PASS_SCOPED must not imply validation of an untested halt branch. Source-semantics evidence leaves all six source-bound parameters null/UNESTABLISHED. No representation decision rule, numeric threshold or ratified RB0 quantity rule changed.
