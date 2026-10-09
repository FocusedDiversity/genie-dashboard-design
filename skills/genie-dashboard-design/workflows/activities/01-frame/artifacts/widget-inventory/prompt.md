# Generating a Widget Inventory

Derive `dashboards/<slug>/docs/helix/01-frame/widget-inventory.md` from the
approved dashboard-brief using `template.md`.

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

If a Lakeview dashboard export (.lvdash.json) is listed, follow
`assets/lakeview-intake.md`. This inventory is a census of what already
exists, not a proposal: every widget in the file gets a row, its title is
copied verbatim, and its metric comes from the dataset column's `description`
and `expression` rather than being re-derived. Record each widget's `name`
from the file in the Source Widget column — that binding is the only way
Deploy can map a check back to a real widget. Text widgets (section headers)
and `filter-*` widgets are widgets too; inventory them, and note any styling a
text widget hard-codes in HTML, because that styling won't move when the theme
does. A widget you would not have designed still gets a row — in a restyle it
is a parking-lot item for a later cycle, never a silent deletion.

## Rules

- One row per widget the dashboard will contain. KPI tiles count individually.
- Assign W-### ids by page block (W-1xx, W-2xx, …). Ids are permanent for the
  life of the dashboard — Design, Test, Build, and Deploy all reference them.
- The "Metric & aggregation" cell must be executable by a stranger:
  "sum of max(charge_amount) per claim_id", not "total billed".
- The Filters cell names which global filters reach this widget. A widget
  exempt from a filter is a design decision — record why.
- Keep pages under 12 widgets; propose a split page if the count grows past it.
- The Source Widget column is required when the inventory was extracted from an
  existing dashboard, and empty otherwise. Never reuse it for a new widget.

## Layout heuristics (from the design checklist)

- KPI counters first row, 3–5 per row; trends and distributions next;
  drill-down tables last.
- Chart type matches metric shape: time series → line, comparison → bar,
  part-of-whole → donut, detail → table.
- Every page answers one question; a widget that doesn't serve the page's
  purpose moves or dies.
