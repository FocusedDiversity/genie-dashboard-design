# Tableau Workbook Intake (.twb / .twbx)

Use this when the brief's Source Documents table lists a Tableau workbook —
either a bare `.twb` or a `.twbx` that packages its own `.hyper` extract.
Two bundled scripts do the actual reading; this document says what their
output means and how it maps into HELIX artifacts. The "What doesn't
transfer" section below is the honest list of what still needs a human.

Don't hand-roll structural extraction with `grep` on the raw XML — attribute
order and quoting on tags like `<dashboard>`/`<zone>`/`<connection>` varies
between workbooks (sometimes `name` is the first attribute, sometimes the
third), so a `grep '<dashboard name='` that comes up empty does not mean the
workbook has no dashboards. `grep` is fine for a quick spot-check of one
known field or worksheet name; for enumeration, use the script below.

## Step 1: Read the workbook's structure

```
python skills/genie-dashboard-design/assets/list_workbook_structure.py "<path-to-workbook>.twb-or-.twbx"
```

This works directly on either a `.twb` or a `.twbx` — no manual unzip
needed for this step (it reads the zip in place). Add `--worksheet "<name>"`
to limit output to one worksheet once you know which one you're mining. It
reports:

| Output key | What it is | Maps to |
|---|---|---|
| `dashboards[].name`, `.worksheet_zones` | each dashboard and the worksheet zones placed on it | `widget-inventory` page grouping and row order; mockup tab structure — treat exactly like a supplied image mockup |
| `worksheets[].mark_classes` | the mark type Tableau rendered | chart type — see mapping table below |
| `worksheets[].rows_shelf` / `.cols_shelf` / `.encodings` | which fields drive the view, on which shelf | `widget-inventory`'s Metric & aggregation and Filters cells |
| `worksheets[].datasource_dependencies` | the fields **that specific worksheet** uses, with human-readable captions and formulas | the scoped view to mine one widget from — a worksheet's own dependency list, not the workbook-wide field list |
| `datasources[].source_connection` | the original connection (`excel-direct`, `snowflake`, `databricks`, a live table, …) | `dashboard-brief` Data Sources — what this data was *before* Tableau packaged it |
| `datasources[].packaged_extract` | present only if this datasource ships its own `.hyper` file, with its real relative path | if present, go to Step 2 before trusting any schema claim; if absent, this is a live connection — verify against the warehouse instead, same as any other claimed source |
| `calculated_fields_flagged` | calculated fields classified `lod` or `table_calc`, deduplicated, with every worksheet that references each one | see "Calculated fields" below — most calculated fields in a real workbook are **not** in this list and need no clarification |

A workbook commonly declares far more `<calculation>` elements than any
worksheet actually uses (parked experiments, superseded versions); the
`datasource_dependencies` scoping — and the tool's `calculated_fields_summary`
(`total_referenced` vs. `flagged_lod_or_table_calc`) — is what keeps this
tractable. A workbook with 500+ calculated fields total might have only
a few dozen actually in use, and only a handful of those flagged.

## Step 2: Read the packaged extract (if a datasource has one)

A `.hyper` file is Tableau's own binary format — not readable with Grep/Read.
First unzip the `.twbx` (PowerShell `Expand-Archive`, bash `unzip`) into the
scratchpad directory to get the extract onto disk, using the path Step 1
reported in `packaged_extract.dbname` — **do not assume it lives under
`Data/Extracts/`**; that is the common case, but real workbooks also ship it
under `Data/TableauTemp/` or elsewhere, and this attribute is the actual
source of truth. Then:

```
python skills/genie-dashboard-design/assets/read_hyper_schema.py "<unzipped-path>/<packaged_extract.dbname>"
```

This requires the `tableauhyperapi` package (`pip install tableauhyperapi`);
if it isn't installed, install it first — it's a small, official Tableau
package, not a build dependency of anything else. If installing it isn't
possible in this environment, don't silently skip the extract: tell the
stakeholder the packaged data couldn't be inspected and fall back to the
`.twb`'s declared schema, flagged as unverified rather than confirmed.

The script prints one entry per table: real column names/types, row count,
and a small sample. Use this to confirm — or correct — what the workbook's
`datasource_dependencies` claim about that same data source, exactly as
DESCRIBE/LIMIT 1 confirms a live table (there is no live table behind an
extract-only datasource, so this read *is* the verification). A mismatch
(a field the workbook references that the extract doesn't have, a grain that
doesn't match the row count) is a `[NEEDS CLARIFICATION]`, not a silent pick
of one over the other.

## Mark class → HELIX chart type

| Tableau mark class | Typical shape | Chart type |
|---|---|---|
| Bar | one dimension, one measure | bar |
| Line | date/continuous field on one shelf | line |
| Area | like Line, with a filled region | area |
| Circle | two measures (rows × columns) | scatter |
| Square | dimension × dimension grid with a color measure | heatmap |
| Pie | part-of-whole | donut |
| GanttBar | a start field + a duration/end field per row | timeline — no standard HELIX equivalent; note as a design decision for what replaces it |
| Shape / Polygon | custom icon markers or filled map regions | usually a map or a highly custom visual — no standard HELIX equivalent; note as a design decision, don't force it into bar/scatter |
| Automatic, single measure on `text`, no `cols_shelf` (or rows filtered to one value via a parameter) | one value on display | KPI / counter |
| Automatic, dimensions on both `rows_shelf` and `cols_shelf`, multiple fields on `text` | a grid of values | table |

`Automatic` needs the shelf/encoding check — the mark class alone doesn't
say whether it's a single-value tile or a crosstab; Tableau picks "Automatic"
for both.

## Step 3: Mine before inventing

Same rule as any other supplied source doc: read every worksheet used on a
dashboard before writing a single widget-inventory row from scratch. One
worksheet placed on a dashboard is normally one candidate widget — a
worksheet that only feeds a legend, a title card, or an unused tab is noted,
not counted. Reconcile against the brief's approved KPIs rather than
carrying every worksheet over silently: a worksheet with no corresponding
KPI gets flagged in Open Questions, same as a stale row from an old mockup.

## Calculated fields

Only `calculated_fields_flagged` entries need attention — everything else
(`total_referenced` minus that list) is SQL-translatable directly from its
formula. Within the flagged list, the right treatment differs by kind:

- **`lod`** (`{FIXED ...}`, `{INCLUDE ...}`, `{EXCLUDE ...}`) — the scoping is
  inherently ambiguous outside Tableau. Flag
  `[NEEDS CLARIFICATION: Tableau LOD expression — confirm scope]` and resolve
  the actual meaning with the stakeholder; Test then writes a baseline from
  that confirmed meaning, never a literal translation of the formula text.
- **`table_calc`** that is a pure interaction helper — typically boolean,
  comparing `LOOKUP(...)` of a field against a parameter to drive
  highlighting or "which row is selected" logic, not a displayed value. This
  doesn't need a SQL translation at all; note the *intent* (e.g., "the
  selected agent's row is highlighted") as a filter-flow requirement in
  `design-decisions.md` and rebuild it as ordinary dashboard filter/selection
  behavior in Design.
- **`table_calc`** that computes an actual displayed metric — a
  period-over-period delta, a running total, a rank — needs a real SQL
  window-function baseline (`LAG`/`LEAD`, `RANK`/`DENSE_RANK`, a self-join).
  The business meaning is usually clear from the field's caption (e.g., a
  month-over-month change), so this is a translation-and-verify task for
  Test, not necessarily an open stakeholder question — but it still gets a
  baseline query and a recorded result before Build, like any other metric.

Every flagged entry lists every worksheet that references it — write the
clarification or baseline **once per calculated field**, not once per widget;
several widgets commonly share the same underlying calculation (a KPI tile,
its trend sparkline, and its category-rank chart are often three worksheets
built on one calc).

## What doesn't transfer

- **Dashboard actions and parameters** (filter/highlight/URL actions,
  parameter controls) are Tableau-specific interactivity. Note the *intent*
  (e.g., "clicking a region bar filters the detail table") as a filter-flow
  requirement in `design-decisions.md`; it gets rebuilt as a normal Genie
  dashboard filter, not assumed to carry over as-is.
- **Row-level security, Tableau Server permissions, subscriptions/alerts** are
  out of scope for artifact derivation — flag for the stakeholder if they
  matter to this dashboard's rollout.

## Worked mini-example

A supplied `claims_overview.twbx` has one dashboard ("Claims Overview") with
three worksheets: a Bar mark on `payer_type` with `SUM([Charge Amount])`, a
Line mark on `month(claim_date)` with `SUM([Paid Amount])`, and an
`Automatic`-mark worksheet with a single `text` encoding and no `cols_shelf`
showing `COUNTD([Claim ID])`. `list_workbook_structure.py` reports this
datasource's `source_connection` as a live `databricks` class with no
`packaged_extract` — a live connection, so Step 2 is skipped and the table
gets verified against the warehouse instead. One calculated field,
`[Denial Rate]`, is classified `lod`.

This mines into: three widget-inventory rows (bar → "Billed by Payer Type",
line → "Monthly Paid Trend", KPI → "Total Claims") with aggregation already
decided (sum, sum, distinct count), one Data Sources row for
`prod.claims.medical_claim` (still DESCRIBE'd to confirm — it's a live
connection), and one `[NEEDS CLARIFICATION: Denial Rate is a Tableau LOD
expression — confirm scope]` marker that Test resolves with a verified
baseline query before Build ever sees it.

If `claims_overview.twbx` had instead packaged its own extract, the
datasource entry would carry a `packaged_extract.dbname` value (commonly,
but not always, under `Data/Extracts/`) — Step 2's script would run against
that file before the Data Sources row is written, and its reported columns,
types, and row count become that row's grain and "known quality issues"
entries directly, instead of "still DESCRIBE'd to confirm" (there is no live
table to DESCRIBE).
