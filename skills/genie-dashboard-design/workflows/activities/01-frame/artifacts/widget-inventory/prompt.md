# Generating a Widget Inventory

Derive `docs/helix/01-frame/widget-inventory.md` from the approved
dashboard-brief using `template.md`.

If the brief's Source Documents table lists a data dictionary or existing
mockup/wireframe, mine them before inventing rows from scratch: a data
dictionary gives field names and grain for the Source column verbatim; an
existing mockup gives candidate widgets, layout, and page groupings.
Reconcile those candidates against the brief's KPIs rather than treating them
as final — a widget from an old mockup that no longer maps to a defined KPI
gets flagged in Open Questions, not carried over silently.

If a Tableau workbook (.twb/.twbx) is listed, follow
`assets/tableau-intake.md`: each worksheet
placed on a dashboard is normally one candidate row, with chart type
(from its mark class) and aggregation (from its field encodings) already
decided rather than guessed. If the widget's measure is a calculated field
flagged `lod` in that guide, carry the brief's `[NEEDS CLARIFICATION]`
marker into the row's Metric & aggregation cell instead of inventing one —
its scope isn't decided yet. If it's flagged `table_calc` and it genuinely
drives the widget's value (a trend delta, a rank), state the aggregation as
what it will become — a window function — not the Tableau formula; Test
still verifies it before Build sees it.

## Rules

- One row per widget the dashboard will contain. KPI tiles count individually.
- Assign W-### ids by page block (W-1xx, W-2xx, …). Ids are permanent for the
  life of the dashboard — Design, Test, Build, and Deploy all reference them.
- The "Metric & aggregation" cell must be executable by a stranger:
  "sum of max(charge_amount) per claim_id", not "total billed".
- The Filters cell names which global filters reach this widget. A widget
  exempt from a filter is a design decision — record why.
- Keep pages under 12 widgets; propose a split page if the count grows past it.

## Layout heuristics (from the design checklist)

- KPI counters first row, 3–5 per row; trends and distributions next;
  drill-down tables last.
- Chart type matches metric shape: time series → line, comparison → bar,
  part-of-whole → donut, detail → table.
- Every page answers one question; a widget that doesn't serve the page's
  purpose moves or dies.
