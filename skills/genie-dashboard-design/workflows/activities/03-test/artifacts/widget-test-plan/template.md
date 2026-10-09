# Widget Test Plan: [Dashboard Name]

**Inventory**: widget-inventory.md ([version]) · **Decisions**: design-decisions.md ([version])
**Baselines executed**: [YYYY-MM-DD] on [warehouse]

## Strategy

- [What exact-match vs tolerance vs invariant means for this dashboard]
- [Data window baselines were computed over; how drift between Test and Deploy
  days is handled — e.g., re-run baselines at Deploy, compare live vs baseline
  on the same day]

## Baseline Checks

One per widget minimum. ID convention: T-### mirrors its W-###.

### T-101 — verifies W-101 [Widget Title]

**Rule**: [exact match | within ±N% | invariant, e.g. "monotonic by month"]

```sql
-- deterministic baseline; encodes the design's aggregation rule verbatim
SELECT ...
```

**Baseline result** ([date]): [value(s)]
**Covers design rule**: [rule name from design-decisions.md]

## Dashboard-Level Checks

### T-901 — Filter cascade
[Set filter X to value Y; every non-exempt widget narrows; exempt W-### unchanged]

### T-902 — Counter/table agreement
[Counters equal the row counts / aggregates of their detail tables under identical filters]

### T-903 — Empty-slice behavior
[A filter combination with no data yields empty states, not errors]

## Theme Conformance Checks

[Restyle cycles only (Step Zero option 5) — delete this section otherwise.]

### T-801 — Theme colors applied
[Every widget's resolved canvas/background/font/accent equals the selected
theme's hex values in `workflows/resources/themes/<id>.json`]

### T-802 — Series palette matches
[Chart series colors equal `visualizationColors`, in order]

### T-803 — Contrast passes
[Text-on-background contrast checked in the theme's primary mode]

### T-804 — No banned styles
[No hex or chart type from the theme's `banned` list appears]

### T-805 — Hard-coded styling reconciled
[Every entry in design-decisions' reconciliation table resolved as stated]

## Out of Scope

- [Named exclusions with reasons — e.g., "pixel layout: covered by mockup approval"]
