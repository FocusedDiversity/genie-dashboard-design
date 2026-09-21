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

## Out of Scope

- [Named exclusions with reasons — e.g., "pixel layout: covered by mockup approval"]
