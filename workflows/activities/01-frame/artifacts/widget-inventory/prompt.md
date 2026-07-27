# Generating a Widget Inventory

Derive `docs/helix/01-frame/widget-inventory.md` from the approved
dashboard-brief using `template.md`.

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
