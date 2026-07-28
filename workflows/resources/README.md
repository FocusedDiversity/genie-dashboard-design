# Shared Workflow Resources

Resources used by more than one activity live here (HELIX skill-resource
boundary: shared root for multi-consumer assets).

## dashboard-theme.json — canonical dashboard theme

The org-standard Databricks AI/BI theme, stored as the exact `uiSettings`
block of a `.lvdash.json` dashboard export. **This file is the palette
authority** for both mockups (Design) and deployed dashboards (Deploy).

- **Provenance**: extracted 2026-07-28 from `wanderbricks_dashboard.lvdash.json`.
- **To update**: style any dashboard in the Databricks theme editor, download
  it (`.lvdash.json`), copy its `uiSettings` object into this file AND into
  `seed.lvdash.json`, and update the mockup CSS mapping below if keys changed.

## seed.lvdash.json — themed starter dashboard

An importable dashboard definition containing one empty canvas page and the
canonical theme. Deploy starts by importing this file (workspace → import
`.lvdash.json`), so every new dashboard is born with the standard theme
instead of having it re-applied by hand.

## Theme → mockup CSS mapping

Mockups render the dark variant by default. Derive CSS variables as:

| Theme key (dark) | Value | Mockup CSS variable |
|---|---|---|
| canvasBackgroundColor.dark | #1E343F | `--bg` |
| widgetBackgroundColor.dark | #08141A | `--panel` / card background |
| widgetBorderColor.dark | #08141A | `--border` (borderless look; use a subtle lighter line for internal dividers) |
| fontColor.dark | #EBEBEB | `--text` |
| selectionColor | #D3456B | `--accent` (selection/highlight; the Design gate greps for this hex) |
| visualizationColors | #15AFDD, #2375A8, #52A870, #C85070, #C89930 | chart series palette, in order |
| widgetCornerRadius | 12 | card `border-radius: 12px` |
| widgetHeaderAlignment | LEFT | widget titles left-aligned |
| fontFamily | Space Grotesk | `font-family: "Space Grotesk", system-ui, sans-serif` — no external font loading in mockups; falls back when not installed |

Light-variant values exist in the theme file for dashboards viewed in light
mode; mockups may include them under `prefers-color-scheme: light` but the
review default is dark.

## Consumption points (the standardization)

1. **Design**: `dashboard-mockup` prompt/template require these variables;
   the 02-design exit gate greps the mockup for the selection color `D3456B`.
2. **Deploy**: `deployment-guide` creation steps start from `seed.lvdash.json`;
   the 05-deploy gate includes a manual theme-match check.
3. Widget-level color choices (e.g., semantic green/amber/red states) stay a
   Design decision — the theme governs chrome, typography, and the default
   series palette, not conditional formatting.

Note: mockup examples created before 2026-07-28 (`example-appointment-analytics.html`)
predate this theme and keep their original palette; the theme file, not the
example, is the palette authority.
