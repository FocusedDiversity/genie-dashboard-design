# Generating a Widget Test Plan

Write `dashboards/<slug>/docs/helix/03-test/widget-test-plan.md` from
`template.md`, derived from the approved inventory and design-decisions. This
happens BEFORE any Genie prompt is written — the Build entry gate depends on it.

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
- If a source Tableau workbook supplied a custom-SQL data source (a `<relation
  type="text">` — see `assets/tableau-intake.md`),
  treat its SQL as a draft only: run it, don't assume it's correct just
  because it's what Tableau used.
- Every `[NEEDS CLARIFICATION: Tableau LOD expression ...]` marker carried
  from Frame gets its own baseline query here, written from a verified
  understanding of what the calculation means (confirmed with the
  stakeholder) — never a translation of the Tableau formula text itself, since
  LOD scoping doesn't map 1:1 to SQL. A Tableau table calculation that drives
  a widget's value (a trend delta, a rank) does map to SQL — as a window
  function — but still gets its own baseline query here rather than being
  assumed correct because the formula looked simple.
- Every aggregation rule in design-decisions.md appears in at least one check;
  if a rule has no check, either write the check or move the rule out of
  design authority.
- These baselines double as the Deploy verification script and the Iterate
  drift monitor — write them to be re-run, not run once.

## Restyle cycles

If the brief's Source Documents table lists a Lakeview dashboard export, this
plan carries two families of checks and both are required — see
`assets/restyle-cycle.md`.

**Invariance (`T-1xx`…, the normal per-widget numbering)**: the baselines are
run against the dashboard *as it is today*, before the theme changes, and the
recorded results become the contract. Deploy re-runs the identical queries
after the restyle and they must match exactly — no tolerance, because nothing
about a color change can legitimately move a number. State the rule as "exact
match vs. pre-restyle baseline" rather than a business tolerance.

**Conformance (`T-8xx`)**: these check appearance, so they are inspection
steps rather than SQL. Write one per property worth failing over:

- every widget's resolved canvas/background/font/accent color equals the
  selected theme's hex value in `workflows/resources/themes/<id>.json`
- the chart series palette matches `visualizationColors` in order
- text contrast passes in the theme's primary mode
- no hex or chart type on the theme's `banned` list appears anywhere (themes
  that declare one — see `house-style.json` — make this mechanical)
- every hard-coded style flagged in design-decisions' reconciliation table is
  resolved the way that table says it is

Baselines for a restyle live beside the plan as `.sql` files when they're long
enough to hurt readability; reference them by filename from the check.
