# Theme Catalog

Four org-approved dashboard themes. Design activity picks one per dashboard
(see "Selecting a theme" below); Deploy imports the matching seed. Adding a
theme is the same shape as these four — see "Adding a theme."

Framework grounding:
[Databricks — Design beautiful dashboards with AI/BI](https://www.databricks.com/blog/design-beautiful-dashboards-aibi).
Every theme here follows its **60-30-10 rule**: 60% dominant neutral (canvas/
widget/border backgrounds), 30% supporting color (font + data visualization
palette), 10% accent (selection color, used sparingly to draw the eye). Chart
palettes are sized 5-9 colors, avoid extremely bright or extremely dark
entries, and keep red and green apart for red/green color-blindness.

## Catalog

| ID | Name | Default mode | Font | Best for | Provenance |
|---|---|---|---|---|---|
| `wanderbricks` | Wanderbricks | dark | Space Grotesk | Analysts, engineers, internal tools | Extracted from a Databricks AI/BI example dashboard |
| `clinical-slate` | Clinical Slate | light | Arial | Healthcare, clinical, conservative executive | Extracted from an org export (Synaptiq Healthcare Analytics) |
| `executive-minimal` | Executive Minimal | light | Arial | C-suite, board reporting, external-facing | Constructed from the Databricks 60-30-10 framework |
| `house-style` | House Style | light | Arial | A template to fork for your organization's own brand theme | Constructed from the Databricks 60-30-10 framework as a starting point for org-specific themes |

> `house-style` is a full catalog theme (`house-style.json` +
> `seed.house-style.lvdash.json`) and deliberately neutral — it exists to be
> copied. Beyond the standard `uiSettings` it carries the extra keys an org
> brand guide usually needs (semantic status colors, category colors, table
> styling, and a `banned` list of colors and chart types), with placeholder
> values to replace. Fork it to `<your-org>.json`, keep that file out of a
> shared repo if the palette is confidential, and record the id in
> design-decisions like any other theme.

## Swatches

| Theme | Canvas | Widget | Font | Accent | Series palette |
|---|---|---|---|---|---|
| wanderbricks (dark) | `#1E343F` | `#08141A` | `#EBEBEB` | `#D3456B` | `#15AFDD` `#2375A8` `#52A870` `#C85070` `#C89930` |
| clinical-slate (light) | `#EEF3F8` | `#FFFFFF` | `#2D3748` | `#C8956A` | `#8BA4BD` `#C8956A` `#6B8EAD` `#B8845A` `#2D3748` `#A3C4E0` `#E0B08A` `#4A6B8A` |
| executive-minimal (light) | `#F4F5F7` | `#FFFFFF` | `#1B2430` | `#B8874B` | `#2C5C8A` `#6B7A90` `#8FAFC9` `#B8874B` `#4F6D5A` |
| house-style (light) | `#F5F7FA` | `#FFFFFF` | `#2A3342` | `#3AA0D1` | `#2F7FA8` `#2E9E93` `#465063` `#D89A72` `#6E7480` `#8A7016` |

## Selecting a theme (Design activity)

Present this catalog to the stakeholder as a first Design step, before the
mockup is built:

1. Show the table above (or render three small swatch previews).
2. Ask which fits the dashboard's audience and primary use context — see
   persona fit in the catalog table. Default recommendation when the
   stakeholder has no preference: `wanderbricks` for internal/technical
   dashboards, `clinical-slate` for healthcare or executive dashboards.
3. Record the choice in `design-decisions.md` under **Theme Selection**: the
   theme id, why it fits, and any per-widget overrides.
4. Build the mockup from that theme's `uiSettings.theme` values (see the
   mapping in `workflows/resources/README.md`).

A stakeholder may also request per-widget overrides (e.g., a highlighted KPI
card with its own background) — the blog's guidance: set that widget's border
color to match its own background to reduce clutter. Record overrides in
design-decisions, not just in the mockup.

## Restyling an existing dashboard

When the cycle is a restyle (Step Zero option 5), this catalog is the whole
point of the exercise. The dashboard's current `uiSettings.theme` is mined in
Frame and recorded as the "before" state; the theme picked here is the
"after". design-decisions carries the two side by side as a property-by-
property diff, so the stakeholder approves a change rather than a description.

Two things to check that a fresh build doesn't have to: styling hard-coded
inside widgets (inline `color:` / `font-family:` in text headers, per-widget
chart color overrides) does **not** move when the theme changes, so each one
needs its own recorded decision; and a theme that declares a `banned` list —
`house-style` does — makes the Test activity's conformance checks mechanical.
See `assets/restyle-cycle.md`.

## Adding a theme

1. Style a dashboard in the Databricks theme editor (or start from one of
   these three) and download it (`.lvdash.json`).
2. Copy its `uiSettings` object into a new `themes/<id>.json` file, following
   the shape of the three above (`id`, `name`, `description`, `personaFit`,
   `defaultMode`, `provenance`, `uiSettings`).
3. Copy a `seed.<id>.lvdash.json` from an existing one, swapping in the new
   `uiSettings`.
4. Add a row to the Catalog and Swatches tables above.
5. **Font rule**: web-safe fonts (Arial, Tahoma, Verdana) need only
   `fontFamily` set. A custom/uploaded font (like Space Grotesk here) also
   needs `fontSettings.base.fontFamily` (and `fontColor`) or the workspace
   won't register it — see `wanderbricks.json` for the pattern.
6. Run the palette through a color-blindness simulator (e.g. Adobe Color) in
   both light and dark before adding it to the catalog.
