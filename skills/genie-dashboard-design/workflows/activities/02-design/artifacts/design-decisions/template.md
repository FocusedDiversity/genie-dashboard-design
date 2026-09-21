# Design Decisions: [Dashboard Name]

**Mockup**: dashboard-mockup.html ([version/date])
**Inventory**: widget-inventory.md ([version/date])

## Theme Selection

- **Theme**: [theme id from `workflows/resources/themes/`, e.g. `wanderbricks`]
- **Why**: [audience/persona fit — cite the catalog's persona-fit reasoning,
  not just "stakeholder liked it"]
- **Mode**: [light | dark | both — which is the primary review surface]
- **Per-widget overrides**: [any widget with its own background/border, and
  why — e.g., "W-201 gets its own emphasis background per the theme's
  set-border-to-match-background rule"; or "none"]

## Layout Choices

- [Page order and why; KPI-row placement; which widgets got full width and why]
- [Navigation pattern: tabs vs pages; anything exempt from the standard grid]

## Chart Type Rationale

| Widget | Type chosen | Why (and what it beat) |
|---|---|---|
| W-### | [line/bar/donut/table] | [reason — e.g., "trend question → line; bar hid the seasonality"] |

## Aggregation Rules

State each rule so a stranger could write SQL from it. These become Test checks.

- **[Rule name]** (W-###, W-###): [e.g., "charge_amount repeats per claim line;
  all charge sums take max(charge_amount) per claim_id first"]
- **Dedupe**: [e.g., "latest snapshot_ts per business key within a snapshot_date"]
- **Null/zero handling**: [e.g., "paid_amount null AND 0 both count as denied"]

## Filter Flow

- [Which global filters reach which widgets; exempt widgets named with reasons]
- [Page-local filters and their datasets; cascading behavior]

## Accessibility

- [Color + non-color encodings; direction glyphs paired with text; contrast notes]

## Rejected Alternatives

| Alternative | Rejected because |
|---|---|
| [real option that was on the table] | [the actual reason] |
