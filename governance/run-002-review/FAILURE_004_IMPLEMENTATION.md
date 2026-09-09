# Recorded failure: N80B implementation nonconformance

Registry status: RECORDED under the 2026-09-09 Operator act; see FAILURES.md.

Frozen N80B specifies interpolation between bounding check cycles. The implementation instead uses cycle_rows[idx - 1] and the triggering adjacent row without a check-cycle eligibility predicate. The affected scope is M03, M04, M07, M08, M11 and M12 across all twelve target cells: 72 records.

This is an implementation defect against an existing literal requirement. The observation-class failure prevents use of the emitted ZERO_0_OF_12 as a scientific controlled verdict, despite conforming EFC arithmetic and comparator calculations in the preserved run. No replacement estimator is proposed or executed. The frozen engine and original execution remain unchanged.
