# Tableau Workbook Intake (.twb / .twbx)

Use this when the brief's Source Documents table lists a Tableau workbook —
either a bare `.twb` or a `.twbx` that packages its own `.hyper` extract.
Both are handled: the `.twb` XML gives layout, worksheets, fields, and
formatting; a packaged `.hyper` extract (when present) gets queried directly
for its real schema and row counts. Nothing beyond the file/shell tools this
workflow already uses, plus one small bundled script for the extract. The
"What doesn't transfer" section below is the honest list of what still needs
a human.

## Step 1: Unpack

- `.twbx` is a zip. Unzip it into the scratchpad directory (PowerShell
  `Expand-Archive`, bash `unzip`) — you get a `.twb` file (plain XML) plus,
  sometimes, `Data/Extracts/*.hyper` and any embedded images.
- A bare `.twb` is already the XML — no unpacking needed, and it never
  packages an extract (that's what makes a `.twbx` a `.twbx`).
- If unpacking produced a `.hyper` file, continue to Step 2 before reading
  the XML. If not — a live-connection workbook, or a bare `.twb` — skip to
  Step 3; the real tables get verified against the warehouse in Frame/Test
  like any other claimed source instead.

## Step 2: Read the packaged extract (if present)

A `.hyper` file is Tableau's own binary format — not readable with
Grep/Read. Query it directly with the bundled script:

```
python skills/genie-dashboard-design/assets/read_hyper_schema.py "<path>/Data/Extracts/<name>.hyper"
```

This requires the `tableauhyperapi` package (`pip install tableauhyperapi`);
if it isn't installed, install it first — it's a small, official Tableau
package, not a build dependency of anything else. If installing it isn't
possible in this environment, don't silently skip the extract: tell the
stakeholder the packaged data couldn't be inspected and fall back to the
`.twb` XML's declared schema, flagging it as unverified rather than
confirmed.

The script prints one entry per table: real column names/types, row count,
and a small sample. Use this to confirm — or correct — what the `.twb` XML's
`<relation>`/`<column>` elements claim about that same data source, exactly
as DESCRIBE/LIMIT 1 confirms a live table. A mismatch (a column the XML
references that the extract doesn't have, a grain that doesn't match the row
count) is a `[NEEDS CLARIFICATION]`, not a silent pick of one over the other.

## Step 3: Read the XML for these elements

Attribute names shift a little across Tableau versions (2018.x–2024.x+) —
if a `grep` below comes up empty, search for the worksheet or field name
directly rather than assuming the workbook has nothing to offer.

| Element | What it tells you | Maps to |
|---|---|---|
| `<datasource>` … `<connection class="databricks\|snowflake\|hyper\|...">` | live connection vs. packaged extract | `dashboard-brief` Data Sources — `class="hyper"` means Step 2's extract read is the source of truth for schema/grain; any live class means the warehouse table is |
| `<relation type="table" table="[schema].[tbl]">` | table/schema referenced | `dashboard-brief` Data Sources, `widget-inventory` Source column (still verify with DESCRIBE — this is a claim, not confirmation) |
| `<relation type="text">SELECT ...</relation>` (custom SQL data source) | literal SQL text | a **draft** baseline for `widget-test-plan` — must still be run against the warehouse, never copied in as an already-verified result |
| `<column caption="Denial Rate" name="[Calculation_12345]" role="measure">` with a nested `<calculation class="tableau" formula="...">` | a calculated field, in Tableau's own formula language | flag `[NEEDS CLARIFICATION: Tableau calculated field — verify SQL equivalent]`; see "What doesn't transfer" below |
| `<dashboard name="Overview"><zones>...<zone name="..." x="" y="" w="" h="">` (nested zone tree) | tab name + widget grid position/size per worksheet | `widget-inventory` page grouping and row order; mockup layout — treat exactly like a supplied image mockup |
| `<worksheet name="..."><pane><mark class="Bar\|Line\|Circle\|...">` | mark type Tableau rendered | chart type — see mapping table below |
| `<encodings>` and `<column-instance column="[Field]" derivation="Sum\|CountD\|Avg\|..." role="dimension\|measure">` | which fields drive the view, and their aggregation | `widget-inventory`'s Metric & aggregation and Filters cells — this is normally the hardest thing to extract from an interview; here it's stated |
| `<style>` rules, `<color-palette name="..."><color>#4E79A7</color>...` | fonts, custom colors | `design-decisions.md` Theme Selection reconciliation — treat exactly like a supplied brand/style doc (match, override, or gap; never silently ignored) |

## Mark class → HELIX chart type

| Tableau mark class | Typical encoding shape | Chart type |
|---|---|---|
| Bar | one dimension, one measure | bar |
| Line | date/continuous field on one shelf | line |
| Circle | two measures (rows × columns) | scatter |
| Square | dimension × dimension grid with a color measure | heatmap |
| Pie | part-of-whole | donut |
| Text, large single value, no axes | single measure | KPI / counter |
| Text, dimension × dimension grid (crosstab) | multiple dimensions, no marks | table |

## Step 4: Mine before inventing

Same rule as any other supplied source doc: read every worksheet used on a
dashboard before writing a single widget-inventory row from scratch. One
worksheet placed on a dashboard is normally one candidate widget — a
worksheet that only feeds a legend, a title card, or an unused tab is noted,
not counted. Reconcile against the brief's approved KPIs rather than
carrying every worksheet over silently: a worksheet with no corresponding
KPI gets flagged in Open Questions, same as a stale row from an old mockup.

## What doesn't transfer

- **LOD expressions and table calculations** (`{FIXED ...}`, `{INCLUDE ...}`,
  `RUNNING_SUM`, `WINDOW_AVG`, etc.) are Tableau's own computation model —
  there is no mechanical translation to SQL. Every one becomes a
  `[NEEDS CLARIFICATION]` item in Frame, and a from-scratch baseline query in
  Test that the stakeholder confirms means the same thing the Tableau
  calculation did — not a port of the formula text.
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
Line mark on `month(claim_date)` with `SUM([Paid Amount])`, and a Text mark
showing `COUNTD([Claim ID])`. Its data source connects live to
`prod.claims.medical_claim`. One calculated field, `[Denial Rate]`, uses an
LOD expression.

This mines into: three widget-inventory rows (bar → "Billed by Payer Type",
line → "Monthly Paid Trend", KPI → "Total Claims") with aggregation already
decided (sum, sum, distinct count), one Data Sources row for
`prod.claims.medical_claim` (still DESCRIBE'd to confirm), and one
`[NEEDS CLARIFICATION: Denial Rate is a Tableau LOD expression — confirm
numerator/denominator]` marker that Test resolves with a verified baseline
query before Build ever sees it.

If `claims_overview.twbx` had instead packaged its own extract (connection
class `hyper`, no live warehouse table behind it), Step 2's script would run
against `Data/Extracts/Claims.hyper` before the Data Sources row is written —
its reported columns, types, and row count become that row's grain and
"known quality issues" entries directly, instead of "still DESCRIBE'd to
confirm" (there is no live table to DESCRIBE).
