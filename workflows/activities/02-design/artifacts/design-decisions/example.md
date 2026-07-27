# Design Decisions: Synaptiq Healthcare Analytics

**Mockup**: dashboard-mockup.html (v1.0, 2026-07-27)
**Inventory**: widget-inventory.md (v1.0, 2026-07-27)

## Layout Choices

- Members before Claims: enrollment context frames spend questions.
- KPI counters top row on both pages; the monthly trend (W-203) takes full
  width because the billed/paid gap is the page's headline story.

## Chart Type Rationale

| Widget | Type chosen | Why (and what it beat) |
|---|---|---|
| W-103 | donut | 3-category payer mix is a part-of-whole read; beat a bar that implied ranking |
| W-104 | bar | age bands are ordered categories; beat a donut with too many slices |
| W-203 | dual line | billed vs paid divergence over time is the question; beat stacked bars that hid the gap |

## Aggregation Rules

- **Charge-once-per-claim** (W-201, W-203): charge_amount repeats on every claim
  line; all charge aggregations take max(charge_amount) per claim_id before
  summing. Same rule for paid_amount.
- **Denied means unpaid** (W-202): paid_amount null and paid_amount = 0 both
  count as denied; denominator is all distinct claim_id in the filter window.
- **Member = person** (W-101–W-104): member counts are distinct person_id;
  never row counts of eligibility spans.

## Filter Flow

- Date Range, Payer Type, State reach every widget except W-101 (lifetime
  total is date-exempt by definition; noted in its subtitle).
- No page-local filters in v1.

## Accessibility

- Donut segments labeled with name + percent, not color-legend-only.
- Trend lines differ by dash pattern as well as color.

## Rejected Alternatives

| Alternative | Rejected because |
|---|---|
| Single combined page | 12+ widgets forced scrolling past the KPI row; split by audience question instead |
| Denial rate by paid_amount < billed | conflates partial payment with denial; stakeholder confirmed unpaid-only definition |
