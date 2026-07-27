# Generating a Dashboard Mockup

Produce `docs/helix/02-design/dashboard-mockup.html` from the approved
widget-inventory, following `template.md`. Match the look and feel of
`example-appointment-analytics.html` — stakeholders should feel they are
looking at a published Databricks dashboard.

## Process

1. Read the widget inventory. Every W-### row becomes exactly one card with
   `data-widget-id="W-###"` on the correct page, in the stated row order.
   Composite cards (tables with their own sub-filters) may tag the `h3`.
2. Build the Databricks chrome: app bar, dashboard title row with published
   pill + MOCKUP tag, tabs named exactly as the inventory's pages.
3. Render the filter bar from the inventory's filter table. Wire the filters
   that change design understanding (a type selector, a threshold, a cascade)
   to re-render KPIs, chart data, and table rows from pre-baked scenario
   objects — 2–5 plausible scenarios beat a static picture at review time.
4. Draw charts with Chart.js (CDN script is the one allowed external ref).
   Fake data must be plausible and internally consistent: right magnitudes,
   right units, KPI values that agree with their charts and tables.
5. Add the footer: the single word "Mockup" — nothing else (no source objects,
   row counts, or styling notes).
6. Verify before the gate: open in a browser, click every tab, exercise every
   wired filter, and grep your own file for untagged cards.

## Rules

- Dark Databricks-style theme (CSS variables, like the canonical example);
  contrast readable on a projector.
- Semantic color: green = good, amber = watch, red = intervene — consistent
  across KPIs, chart fills, and table badges.
- Tables: sticky headers, scrollable body, badges for status/severity, an
  empty-state row for filter combinations with no data.
- Recommendation/insight note cards are welcome where Design has a point of
  view, but they are annotations — not widgets — and get no W-###.
- All person-level data is synthetic. No real MRNs, names, or DOBs, ever.

## Review handoff

Present alongside `design-decisions.md`. Revision requests at the gate edit the
mockup first, then sync the inventory if widgets were added/moved/retired.
