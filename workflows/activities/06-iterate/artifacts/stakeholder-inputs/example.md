# Stakeholder Inputs — Synaptiq Healthcare Analytics

A record of every input the stakeholder supplied during the 2026-09-16 HELIX cycle that
produced the Synaptiq Healthcare Analytics dashboard, and what to prepare before running
the next one.

**Totals**: 15 questions across 7 prompts, 4 gate approvals, 1 opening brief.
**Result**: 34 widgets, 3 pages, 42/42 verification checks passing on first deploy.

---

## 1. Opening brief (volunteered, not asked)

| Input | Value |
|---|---|
| Goal | Design and build a Databricks AI/BI dashboard for a Healthcare Analytics audience |
| Environment | DEV — `adb-<workspace-id>.<n>.azuredatabricks.net` |
| Requirements document | `Synaptiq Healthcare Analytics - Dashboard Requirements Document.docx` (BRD v1.1) |
| Source DDL | `Healthcare_Analytics_Tables.txt` |

Two further constraints came from saved preferences rather than this conversation:
requirements documents do not pre-supply a widget inventory (HELIX derives W-IDs itself),
and they are written in prospective BRD voice rather than as an audit report.

---

## 2. Setup — 2 questions

| # | Activity | Question | Options offered | Chosen |
|---|---|---|---|---|
| 1 | Step Zero | Which best matches your starting materials? | Requirements doc only *(rec)* · Doc + wireframe/mockup · Blank slate · Existing Tableau workbook | **Requirements doc only** |
| 2 | Frame | Confirm the Databricks profile | `gfischer` *(rec)* · Create a different profile | **gfischer** |

Question 2 exists because the Databricks skill forbids auto-selecting a profile even when
only one is configured.

---

## 3. Frame, round 1 — 4 questions

Every one of these arose from a conflict between the BRD and live profiling. None were
answerable from the document alone.

| # | Question | Options offered | Chosen |
|---|---|---|---|
| 3 | Active Members returns 40 of 5,040 (0.8%) — eligibility and claims data disagree | Keep rule, add caveat *(rec)* · Redefine as activity-based · Drop the KPI this release | **Redefine as activity-based** |
| 4 | `payer_type` holds one value for all 5,040 members, so the payer-mix chart is a single bar | Swap for Employer Group *(rec)* · Keep as single-value placeholder · Swap for enrollment-duration band · Drop it | **Swap for Employer Group** |
| 5 | "Employer Groups" is ambiguous — `group_id` gives 3,838, `group_name` gives 4 | `group_name` → 4 *(rec)* · `group_id` → 3,838 · Show both | **`group_name` — 4** |
| 6 | The BRD restricts the State filter on a premise that is factually wrong | Full coverage, all 3 pages *(rec)* · Members page only, but complete · Keep the doc's partial scope | **Full coverage, all 3 pages** |

**Effect on the build**: replaced the Active Members KPI with Members with Activity,
replaced Enrollment by Payer Type with Members by Employer Group, fixed the Employer
Groups KPI from 3,838 to 4, and extended the State filter to all 34 widgets.

---

## 4. Frame, round 2 — 4 questions

| # | Question | Options offered | Chosen |
|---|---|---|---|
| 7 | Activity window for the new KPI — asked after correcting an estimate of mine that turned out wrong (trailing-12mo is 947, not ~4,992) | Ever active — 4,992 *(rec)* · Trailing 12 months — 947 · Both as separate tiles | **Ever active — 4,992** |
| 8 | Calendar 2025 contains no data, so every trend spans a 17-month hole | Add a date-range filter, default to populated window *(rec)* · Show the full range honestly · Restrict trends to 2024 only | **Add a date-range filter** |
| 9 | Denial Rate — the BRD's type-averaged method vs a single line-weighted rate | Line-weighted — 14.66% *(rec)* · Type-averaged — 14.73% · Line-weighted headline plus by-type breakdown | **Line-weighted — 14.66%** |
| 10 | Depth for ranked "Top N" widgets, given narrow code sets (19–25 distinct values) | Top 10 *(rec)* · Top 15 · Show all values | **Top 10** |

**Effect on the build**: introduced a dashboard-level Date Range filter the BRD never
specified, settled the denial-rate denominator, and fixed Top-10 across six widgets.

---

## 5. Frame, structure — 1 question

| # | Question | Options offered | Chosen |
|---|---|---|---|
| 11 | Pages 2 and 3 exceed the 12-widget inventory limit (13 and 14) | Split into 5 pages *(rec)* · Keep 3 pages, accept the overage · Keep 3 pages, trim to 12 each · Split into 4 pages | **Keep 3 pages, trim to 12 each** |

**The only question where the recommendation was overridden — correctly.** The BRD's
three-page structure is a stakeholder commitment with named page owners (Health Plan
Operations owns Members, Finance owns Claims & Charges, Population Health owns Clinical
Conditions), so re-cutting the pages would have changed who owns what. Three secondary
widgets were deferred instead: Avg Billed by Claim Type, Encounter Volume by Day of Week,
and HbA1c Value Distribution.

This is now a standing preference: when a widget-count heuristic collides with a page
structure the BRD promised, trim widgets rather than split pages.

---

## 6. Design — 1 question

| # | Question | Options offered | Chosen |
|---|---|---|---|
| 12 | Dashboard theme | Clinical Slate *(rec)* · Executive Minimal · Wanderbricks | **Clinical Slate** |

Presented with rendered swatch previews. Clinical Slate was recommended because BRD §12.2
specifies a "navy/tan palette, Arial typography" and that theme's own provenance is an
export of a Synaptiq Healthcare Analytics dashboard — an exact match rather than an
approximation, needing no per-widget overrides.

---

## 7. Deploy — 3 questions

| # | Question | Options offered | Chosen |
|---|---|---|---|
| 13 | Build method | Deploy with verified SQL *(rec)* · Themed seed, stakeholder pastes Genie prompts · Hybrid | **Deploy with verified SQL** |
| 14 | SQL warehouse | `dev-default-serverless` *(rec)* · `Serverless Starter Warehouse` | **dev-default-serverless** |
| 15 | Create the 5 fallback views now? | Only if needed *(rec)* · Create all 5 · Create only `v_claim_line_enriched` | **Only if needed** |

All three were asked together because deploying writes to a shared workspace, and that
warranted explicit authorisation before any object was created. No fallback views were
ultimately needed.

---

## 8. Gate approvals — 4 free-text

| Gate | Response | What it released |
|---|---|---|
| Frame | `Approved` | Design |
| Design | `Proceed to TEST` | Test |
| Test | `Proceed to Build` | Build |
| Build | `Proceed to Deploy` | Deploy |

The Deploy gate and the Iterate activity were still open when this record was written.

---

## 9. What to prepare before the next cycle

Ten of the fifteen questions existed only because live profiling contradicted the
requirements document. Most of that round-tripping is avoidable.

**Profile the data before writing the BRD.** Every conflict below was discoverable with a
single query, and each one changed the dashboard:

- Cardinality of every column intended as a filter or breakdown. A dimension with one
  distinct value is not a breakdown; a filter documented as "~50 states" that holds 15 is
  a wrong spec.
- Distinct-value counts for any column named in a KPI. `group_id` versus `group_name`
  differed by three orders of magnitude and the BRD named neither.
- Date coverage per fact table, at month grain. The 17-month hole in 2025 reshaped every
  trend widget and forced a filter the BRD never contemplated.
- Row counts against stated grain, and the actual double-counting test rather than an
  assumed one. The BRD's highest-priority risk turned out to be a misdiagnosis.

**Decide these in advance — they will be asked every time:**

1. Numerator and denominator for every rate, stated explicitly.
2. Which exact column backs each KPI, not just the business term.
3. Top-N depth for ranked widgets.
4. Filter coverage per page, including which widgets are deliberately exempt and why.
5. Page structure and who owns each page.
6. Theme, against the catalog in `workflows/resources/themes/README.md`.
7. Target environment, warehouse, and whether deployment may write to the catalog.

**Supply the complete DDL.** `lab_result` was named throughout the BRD but absent from the
DDL file; its schema had to be recovered from the live catalog, and both HbA1c widgets
depend on it.

**Expect to be asked about anything the document leaves as an open question.** The BRD
carried seven. Four were closed by evidence during Frame, three were scoped as dev-build
decisions with production promotion recorded as the prerequisite. None could simply be
inherited.
