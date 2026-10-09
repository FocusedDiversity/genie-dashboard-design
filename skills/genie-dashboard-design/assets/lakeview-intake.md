# Lakeview Dashboard Intake (.lvdash.json)

Use this when the stakeholder is starting from a dashboard that already
exists — Step Zero option 5, the restyle cycle. The dashboard file is already
in the repo, so this intake starts by *finding* it rather than asking for a
path. One bundled script does the reading; this document says what its output
means and where each part lands. `restyle-cycle.md` is the companion: this
file covers mining, that one covers what each activity is allowed to change.

The dashboard is the requirements document. Everything the brief and inventory
need — pages, widgets, titles, datasets, metric definitions, layout — is
already in the file and was already approved by whoever shipped it. Mining it
is not a shortcut around the Frame interview; it *is* the Frame interview for a
restyle, and the only open questions left are about scope and the new theme.

Don't hand-roll this with `grep` or by reading the raw JSON. A real dashboard
runs to thousands of lines, mostly per-widget encoding and number-format detail
that doesn't change what a widget is, and two shapes will bite you: a widget's
title is a bare string in some widget versions and a `{"value": …}` object in
others, and text widgets carry `multilineTextboxSpec` with no `widgetType` at
all. The script normalizes both.

## Step 1: Find the dashboard and agree its folder

The script lives in this skill's own `assets/` folder — run it by its resolved
path on disk, wherever the skill is installed, not relative to the repo you are
working in.

```
python <skill>/assets/list_dashboard_structure.py --list .
```

This lists every `.lvdash.json` in the working repo with its page, widget, and
dataset counts, skipping vendored skill copies and bundled theme seeds (which
are starter templates, not anyone's dashboard). A repo commonly holds dozens.

**Ask the stakeholder which one.** Present the list — name and size — and wait.
Never guess from the invocation text: names repeat, and `_Old`, `_FIX`, and
`(WIP)` variants of the same dashboard sit side by side in the same folder.

Then agree the folder. Artifacts go to `dashboards/<slug>/docs/helix/…`:

- If the dashboard already lives in a `dashboards/<slug>/` folder of its own,
  that is the slug. Reuse it; don't make a second one.
- If it sits loose in `dashboards/`, propose a short `snake_case` slug from its
  title and **confirm it** before writing anything. The folder name is usually
  shorter than the dashboard name — "Claims Overview (Revised)" →
  `claims_overview`. Create `dashboards/<slug>/` and copy the
  `.lvdash.json` into it; leave the original where it is, so the restyle is a
  side-by-side working copy rather than an edit to the live file.

Record the chosen file in the brief's Source Documents table as type
`Lakeview dashboard export`.

## Step 2: Read the structure

```
python <skill>/assets/list_dashboard_structure.py "<path>.lvdash.json"
python <skill>/assets/list_dashboard_structure.py "<path>.lvdash.json" --sql
python <skill>/assets/list_dashboard_structure.py "<path>.lvdash.json" --page Overview
```

Start without `--sql` for the shape of the thing; add it when you need the
dataset queries (Build and Test both do). `--page` narrows widget output to one
page once you're mining page by page.

| Script output | Where it lands |
|---|---|
| `pages[].displayName` + order | `widget-inventory` Pages table, in dashboard order; the mockup's tab structure — **treat exactly like a supplied mockup**, because it is one |
| widget `[name]` | `widget-inventory` Source Widget column. This is the stable id the `W-###` binds to, and the only thing Deploy can use to map a check back to a real widget |
| widget type | `widget-inventory` Type. `filter-*` types are the dashboard's filter architecture, not chart widgets — they belong in the brief's Filters section |
| widget title | `widget-inventory` Widget name, verbatim. Build reuses these exactly; a restyle must not rename anything |
| widget `dataset` + `fields` | `widget-inventory` Metric & aggregation and Source; `MEASURE(x)` fields point at a dataset column, so resolve them against the Datasets section below |
| widget `position` | Mockup layout: `y` gives row order, `x` and `width` give placement across the 12-column grid |
| `datasets[].columns` | The brief's KPIs & Metrics table — `description` is the human definition, `expression` is the aggregation already stated in SQL. Copy both rather than re-deriving them |
| `datasets[].queryLines` (`--sql`) | The brief's Data Sources table (mine the `FROM`/`JOIN` targets for full three-part paths); Build's reverse-engineered prompt catalog; Test's invariance baselines |
| `uiSettings.theme` | The brief's Restyle Scope "current theme", and the *before* column of design-decisions' before/after palette table. Absent means the dashboard is on the Lakeview default — say so explicitly rather than leaving it blank |

## Step 3: Mine as-built, don't invent

Every widget in the file gets an inventory row, including the ones you would
not have designed. A restyle inherits the dashboard as it is; a widget you
think is redundant is a parking-lot item for a later cycle, not something to
drop from the inventory. The inventory's job here is to be a complete,
verifiable census of what exists.

- **Text widgets** (type `text`) are the section headers and definition blocks.
  They carry no data but they do carry visual structure and inline styling —
  font, size, color, usually as raw HTML. They are the widgets a restyle is
  most likely to actually change, so inventory them and note the styling they
  hard-code; that styling is exactly what a theme change has to reconcile.
- **Filter widgets** (`filter-multi-select`, `filter-date-range-picker`,
  `filter-single-select`) define the filter architecture. Record which page
  they sit on and which dataset fields they drive.
- **Pages that are entirely filters or text** (a "Global Filters" page, a
  "Definitions" page) are still pages. List them.
- If a widget's title is empty, name it by what it shows and flag the gap —
  don't silently invent a title, because Build will be told to reuse titles
  verbatim and an invented one is a rename.

## Step 4: Record the "before" state

The current `uiSettings.theme` block is the baseline the restyle is measured
against, and it is the one thing that will be overwritten. Copy it verbatim
into the brief's Restyle Scope section before any theme work begins. Without
it there is nothing to roll back to and nothing to diff the new theme against.

Note any styling that is hard-coded in widgets rather than set by the theme —
inline `color:` and `font-family:` in text widgets, per-widget color overrides
in chart encodings. These do not move when the theme changes, so they are the
usual source of a half-restyled dashboard, and every one of them needs a
decision recorded in design-decisions.

## What doesn't transfer

- **Cross-filter wiring and widget interactions** — the file records which
  fields a filter targets, but the intent behind a filter's scope is not in
  there. Note what you observe; confirm intent with the stakeholder rather
  than inferring it.
- **Permissions, sharing, subscriptions, and alerts** — not in the file at
  all. Out of scope for a restyle, but flag them in Deploy so the side-by-side
  copy doesn't quietly ship without them.
- **Whether the numbers are right** — mining tells you what the dashboard
  computes, not whether it is correct. A restyle does not relitigate that; it
  proves the numbers didn't *change*. That's Test's job.

## Worked mini-example

Stakeholder picks option 5. `--list .` reports 35 candidates; they choose
`dashboards/Claims Overview (Revised).lvdash.json` (8 pages, 67 widgets, 7
datasets). It sits loose in `dashboards/`, so you propose the slug
`claims_overview`, confirm it, create `dashboards/claims_overview/`, and copy
the file in.

The structure run shows page 2 "Overview" holding `[b1] text` (an HTML header
hard-coding `font-size:32px; font-family:Calibri; color:#0B7FC4`), then
`[w101] counter` titled "Clean Claim Rate" reading `measure(clean_rate)`
from `ds_scope`, at `x0 y2 3x2`. The Datasets section resolves that measure:
`clean_rate - SUM(clean)/SUM(submitted)
[try_divide(sum(clean), sum(submitted))]`.

That single widget becomes inventory row `W-101` with Source Widget `w101`,
type counter, metric "Clean Claim Rate = try_divide(sum(clean),
sum(submitted))" — a definition copied, not derived. `b1` becomes a row too,
flagged as hard-coding brand color `#0B7FC4` outside the theme, which
design-decisions will have to reconcile when the new theme's accent differs.

The theme block reports `fontFamily: Arial` with a `#0B7FC4` selection color
and a six-entry `visualizationColors` palette — that is the "before" state,
copied into the brief's Restyle Scope before anything else happens.
