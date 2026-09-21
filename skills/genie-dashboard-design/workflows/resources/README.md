# Shared Workflow Resources

Resources used by more than one activity live here (HELIX skill-resource
boundary: shared root for multi-consumer assets).

## themes/ — theme catalog

Multiple org-approved dashboard themes, not one fixed theme. Design activity
asks the stakeholder to pick one as its first step (before the mockup is
built); Build/Deploy use whichever theme was recorded in `design-decisions.md`.
See [themes/README.md](themes/README.md) for the full catalog, swatches,
selection process, and how to add a theme.

Each theme is a pair:

- `themes/<id>.json` — metadata (name, persona fit, provenance) + the exact
  `uiSettings` block of a `.lvdash.json` export. **This is the palette
  authority** for that theme, consumed by both mockups (Design) and deployed
  dashboards (Deploy).
- `themes/seed.<id>.lvdash.json` — an importable dashboard definition (one
  empty canvas page + that theme) so a new dashboard is born themed instead
  of being themed by hand afterward.

## Theme → mockup CSS mapping

Applies to whichever theme was selected; substitute that theme's values.
Mockups render the theme's `defaultMode` variant by default, with the other
mode reachable via `prefers-color-scheme`.

| Theme key | Mockup CSS variable |
|---|---|
| canvasBackgroundColor | `--bg` |
| widgetBackgroundColor | `--panel` / card background |
| widgetBorderColor | `--border` (if it equals widgetBackgroundColor, use a subtle lighter internal divider instead of a visible card border) |
| fontColor | `--text` |
| selectionColor | `--accent` (selection/highlight; the Design gate greps the mockup for this hex) |
| visualizationColors | chart series palette, in order |
| widgetCornerRadius | card `border-radius` (omit → use 8px default) |
| widgetHeaderAlignment | widget title alignment |
| fontFamily | `font-family: "<value>", system-ui, sans-serif` — no external font loading in mockups; falls back when not installed locally |

## Consumption points (the standardization)

1. **Design**: stakeholder selects a theme from `themes/README.md` as Design
   step one; the choice and rationale are recorded in `design-decisions.md`
   under "Theme Selection." The `dashboard-mockup` prompt/template derive
   their CSS from that theme; the 02-design exit gate greps the mockup for
   the selected theme's selection-color hex.
2. **Deploy**: `deployment-guide` creation steps import
   `themes/seed.<id>.lvdash.json` for the selected theme; the 05-deploy gate
   spot-checks the live dashboard against that theme's JSON.
3. Widget-level color choices (e.g., semantic green/amber/red states) stay a
   Design decision — the theme governs chrome, typography, and the default
   series palette, not conditional formatting.

Note: `dashboard-mockup/example-appointment-analytics.html` predates the
theme catalog and keeps its original bespoke palette (it remains the
layout/interactivity reference); `dashboard-mockup/example.html` demonstrates
the `wanderbricks` theme concretely. Neither example is itself a palette
authority — the files in `themes/` are.
