# Dashboard Mockup Template

The mockup is a single `.html` file that imitates a published Databricks AI/BI
dashboard closely enough that stakeholders review the real experience, not a
sketch. See `example-appointment-analytics.html` for the canonical standard and
`example.html` for a minimal fully-offline starter.

## Required structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>[Dashboard Name] — Databricks Dashboard Mockup</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
  <style>/* all CSS inline — variables derived from workflows/resources/dashboard-theme.json
            (dark variant): --bg:#1E343F --panel:#08141A --text:#EBEBEB --accent:#D3456B;
            charts use visualizationColors in order; border-radius:12px;
            font-family:"Space Grotesk",system-ui,sans-serif */</style>
</head>
<body>
  <!-- 1. Databricks chrome: app bar (brand, search, workspace), dashboard
       title row with published pill, MOCKUP tag, Schedule/Share buttons -->
  <!-- 2. Tabs: one .tab per dashboard page; JS toggles .page sections -->
  <!-- 3. Per page: filter bar, then grid rows of .card widgets -->
  <div class="page active" id="t1">
    <div class="filters"><!-- live selects wired to re-render below --></div>
    <div class="grid g-4">
      <div class="card kpi" data-widget-id="W-101">…</div>
    </div>
    <div class="grid g-2">
      <div class="card" data-widget-id="W-105"><h3>…</h3><div class="sub">…</div>
        <div class="chart-wrap"><canvas id="c1_region"></canvas></div></div>
    </div>
  </div>
  <div class="footer">Mockup</div>
  <script>/* Chart.js charts + scenario data + filter re-render logic */</script>
</body>
</html>
```

## Invariants

- **Single file**: all CSS/JS/data inline. The only permitted external
  reference is the Chart.js CDN script; no external fonts, stylesheets,
  images, or fetches.
- **Traceable**: every widget card (or its `h3` for composite table cards)
  carries `data-widget-id="W-###"` matching the widget inventory. The Design
  exit gate greps for this.
- **Interactive where it informs**: at least the page tabs work, and the
  filters that drive design decisions re-render KPIs/charts/tables from
  pre-baked scenario data (see the appointment-type and threshold switches in
  the canonical example). Filters that are pure pass-throughs may be inert.
- **Honest**: only widget shapes AI/BI can render — counters, bar/line/donut/
  scatter/combo charts, tables. Grid proportions mirror the real layout.
- **Labeled**: a visible MOCKUP tag in the title row; the footer reads only
  "Mockup".
- **Synthetic data only**: names, MRNs, and values are fabricated. Never paste
  real patient or member rows into a mockup.
