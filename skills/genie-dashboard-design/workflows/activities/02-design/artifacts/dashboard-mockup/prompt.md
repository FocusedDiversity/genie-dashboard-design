# Generating a Dashboard Mockup

Produce `dashboards/<slug>/docs/helix/02-design/dashboard-mockup.html` from the
approved widget-inventory, following `template.md`. Match the look and feel of
`example.html` — stakeholders should feel they are
looking at a published Databricks dashboard.

**Prerequisite**: a theme must already be selected and recorded in
`design-decisions.md` (see that artifact's "Step Zero: Theme Selection"). If
it isn't, stop and run that step first — the mockup is built from the chosen
theme, not a default.

If the brief's Source Documents table lists an existing mockup or wireframe,
treat it as the layout starting point: reproduce its tab structure and widget
placement wherever it's compatible with the approved inventory, and record any
deviation (and why) in `design-decisions.md`. It informs layout, not chrome —
colors/fonts/corner-radius still come from the selected theme.

The same applies to a Tableau workbook's dashboard `<zones>` tree (see
`assets/tableau-intake.md`): its tab names and
per-worksheet grid positions are the layout starting point, reconciled against
the approved inventory the same way. Any dashboard action or parameter
control the workbook used for interactivity gets rebuilt as a normal wired
filter here — it doesn't carry over as-is.

If the brief's Source Documents table lists a Lakeview dashboard export, the
layout is fixed, not a starting point — see `assets/restyle-cycle.md`.
Reproduce the live dashboard exactly: same pages in the same order, same
widgets with the same titles, same grid positions from the intake's `position`
values. The only thing that differs from production is the theme, so that the
stakeholder is comparing appearance and nothing else. Anything you would
normally improve about the layout is a parking-lot item, not a mockup change.

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

- **Theme is not improvised**: derive all chrome colors, the chart series
  palette, corner radius, header alignment, and font stack from
  `workflows/resources/themes/<selected-id>.json` using the mapping table in
  `workflows/resources/README.md` (that theme's `defaultMode` variant by
  default). Chart.js series use `visualizationColors` in order. Font is
  declared with system fallbacks — never loaded from a CDN. The exit gate
  greps the mockup for the selected theme's selection-color hex.
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
