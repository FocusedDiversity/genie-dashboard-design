# Generating a Widget Test Plan

Write `docs/helix/03-test/widget-test-plan.md` from `template.md`, derived from
the approved inventory and design-decisions. This happens BEFORE any Genie
prompt is written — the Build entry gate depends on it.

## Process

1. For each W-### widget, write deterministic baseline SQL that encodes the
   design's aggregation rule verbatim (the dedupe window function, the
   null-handling predicate, the per-claim max — spelled out, not implied).
2. Run every baseline against the warehouse. Record the result and date in the
   plan. A plan with unexecuted baselines does not pass the Test gate.
3. Choose the expected-result rule per check: exact match for counts and sums,
   tolerance for averages/rates ([±0.1pp] style), invariants where values move
   daily (row counts > 0, spread within bounds, monotonic date axis).
4. Add dashboard-level checks: filter cascade (with the design's exempt
   widgets), counter/table agreement, empty-slice behavior.
5. List what is out of scope, with reasons.

## Rules

- One T-### per W-### minimum; number them to mirror (T-101 ↔ W-101).
- Baseline SQL must be runnable by copy-paste — full table paths, no
  placeholders.
- Every aggregation rule in design-decisions.md appears in at least one check;
  if a rule has no check, either write the check or move the rule out of
  design authority.
- These baselines double as the Deploy verification script and the Iterate
  drift monitor — write them to be re-run, not run once.
