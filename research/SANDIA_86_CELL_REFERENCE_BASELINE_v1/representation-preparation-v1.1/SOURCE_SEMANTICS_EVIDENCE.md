# Source-semantics resolution — preparation v1.1

SOURCE_PARAMETERS: **UNESTABLISHED (0 bound / 6 unresolved)**. This is a documentary-resolution result, not instrument predictions or scientific metrics. Values remain explicit nulls. Exact source hashes and line locators are in SOURCE_SEMANTICS_EVIDENCE.json.

| Parameter | Status | Documentary limitation |
|---|---|---|
| current_polarity_convention | UNESTABLISHED | Charge/discharge protocol rates are described, but no signed-current export-column polarity convention is stated. Do not infer polarity from observed signs. |
| current_zero_code_semantics_and_resolution | UNESTABLISHED | The helper tests literal zeros heuristically; equipment names do not establish channel-specific zero-code meaning, resolution or logging validity. Heuristic comparison is not calibration evidence. |
| sampling_cadence_and_coverage_rule | UNESTABLISHED | Protocol durations and cycle-round structure do not specify acquisition logging cadence, event-driven sampling or complete-coverage criteria. |
| interval_endpoint_inclusion | UNESTABLISHED | File naming and protocol ordering do not specify inclusive/exclusive sample endpoints or whether row boundaries overlap in recorded increments. |
| counter_reset_convention | UNESTABLISHED | Neither source supplies export counter/reset conventions defining per-row versus cumulative quantities. The public EFC helper is not a counter-semantics specification. |
| timeseries_to_cycle_association_rule | UNESTABLISHED | Matched filenames identify the cell; shared Cycle_Index alone does not resolve repeated indices or sample-to-row association. No duplicate-safe association rule is documented. |

The official SNL methods page adds protocol context but does not establish these export semantics. No manufacturer default was transferred to this dataset. No data-value inspection was used to close a documentary gap. This scope does not prove that no external or unpublished specification exists.
