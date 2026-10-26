# Genie Dashboard Design — Executive Overview

## What it is

**Genie Dashboard Design** is a HELIX-based toolkit for designing, building, and maintaining
**Databricks AI/BI (Lakeview) dashboards** with **Genie**. It ships as a Claude Code plugin and as a
portable Agent Skill for GitHub Copilot in VS Code — the same `SKILL.md` folder works in both. It is
installed once and invoked in any repo with a single line:

```
/genie-dashboard-design:genie-dashboard-design Members & claims dashboard for healthcare analytics
```

From that prompt, the agent leads the stakeholder through a guided, gated process: requirements,
personas, design, test, build, deploy, and iterate. It then produces the dashboard (via Genie prompts or
the Databricks CLI) along with a complete, version-controlled documentation trail.

**Core premise:** metric rules and design decisions should be written down and *tested* before Genie is
ever asked to compute or build anything. Genie writes SQL nondeterministically, so deterministic
baseline queries become the contract its output must match.

## What it does — the HELIX spiral

Every dashboard moves through six activities. Each one writes artifacts to
`dashboards/<slug>/docs/helix/` and ends at a **gate the stakeholder must explicitly approve**.

| # | Activity | Key artifacts | Gate question |
|---|---|---|---|
| 01 | **Frame** | Dashboard brief (purpose, personas, KPIs, sources), **widget inventory** | Is this the right dashboard? |
| 02 | **Design** | Theme selection, **browser-viewable HTML mockup**, design-decisions doc | Is this what it should look like? |
| 03 | **Test** | Widget test plan with baseline SQL that has **already been run** | Do we know what "correct" means? |
| 04 | **Build** | Prompt catalog — one Genie prompt per widget | Are the prompts written to spec? |
| 05 | **Deploy** | Deployment guide with recorded **PASS/FAIL** per widget | Does the live dashboard pass? |
| 06 | **Iterate** | Iteration log (feedback, drift checks), stakeholder-inputs record | Spiral again, or close? |

**Traceability spine:** Frame gives every widget a stable `W-###` id. The mockup tags the widget with
it, Test writes a `T-###` check for it, Build writes its Genie prompt, and Deploy records its result.
Nothing enters the pipeline without a `W-###`, and nothing ships without a `T-###` that traces back to
one.

### Five starting points (Step Zero)

1. **Blank slate.** The agent interviews the stakeholder from scratch.
2. **Requirements document.** A PRD or data dictionary is ingested; the interview fills the gaps.
3. **Requirements + wireframe/mockup.** The mockup also seeds the layout and candidate widgets.
4. **Tableau conversion (`.twb`/`.twbx`).** The workbook is mined for worksheets, fields,
   calculations, and layout.
5. **Restyle an existing production dashboard.** The theme changes; the metrics, SQL, and layout are
   held fixed and proven unchanged.

## Value proposition

**1. Artifacts and documentation as a byproduct.** Every cycle produces a full,
version-controlled record as plain Markdown, HTML, and SQL files. Each one is generated against
a template, a set of generation rules, and a quality-bar example. Nobody has to write documentation
after the fact; it comes out of doing the work. One repo can hold many dashboards side by side,
each with its own HELIX folder.

**2. Widget inventory.** This is a single source of truth for what the dashboard contains: each widget's
id, type, metric, grain, persona, and source. It drives the mockup, the tests, and the prompts, so
nothing gets orphaned or added without a requirement behind it. For conversions and restyles,
it's an as-built census mined from the existing asset.

**3. Design doc and HTML mockup before any build.** Stakeholders can open an interactive,
Databricks-styled mockup in a browser, with Chart.js charts and working filters, and approve the look
before any compute is spent. The design-decisions doc records themes, overrides, aggregation and dedup
rules, data grain, and assumptions in SQL-translatable language. Four themes ship with the tool:
*Wanderbricks*, *Clinical Slate*, *Executive Minimal*, and *House Style*. Each comes with a
seed `.lvdash.json`.

**4. Correctness by construction.** Baseline SQL is written and **executed** before any prompt exists.
Deploy re-runs every `T-###` against the live dashboard. A FAIL follows a defined escalation path:
re-prompt once with the rule stated first, then fall back to a pre-written view, then record a waiver.
Iterate re-runs the baselines to catch drift.

**5. Lower risk and rework.** Explicit metric definitions (numerators, denominators, null handling),
no-double-counting rules, and `[NEEDS CLARIFICATION]` markers that block gates mean that ambiguity
gets resolved up front, not discovered in production.

**6. Institutional memory.** `stakeholder-inputs.md` logs every question asked, the options offered,
the recommendation, the decision, and what it changed. It ends with guidance on what to decide up front
next time, so later cycles start faster.

## A fast development lifecycle

The process is gated, but it's built for speed:

- **One-line start, guided flow.** There's no blank page and no process to learn. The agent drives,
  asks targeted questions, and proposes defaults.
- **Reuse over re-entry.** Supplied PRDs, data dictionaries, mockups, and Tableau workbooks are mined
  automatically. Their terms and definitions are reused verbatim in the brief, the design, and the
  Genie prompts.
- **Cheap feedback first.** Design problems surface in an HTML mockup in minutes, not in a deployed
  dashboard after days.
- **Fewer Genie retries.** Prompts carry exact table paths, joins, grain, and dedup language, and they
  are validated against known-good baselines. That cuts the prompt-and-pray loop.
- **Shortcuts for migrations.** The Tableau conversion and restyle paths reuse existing structure
  instead of rebuilding it.
- **Repeatable cycles.** Iterate either scopes the next cycle (back to Frame with everything already
  documented) or closes the dashboard explicitly.

## What's in the box

| Component | Purpose |
|---|---|
| **`SKILL.md`** | The orchestration map. Covers Step Zero, the six activities, gate handling, and stakeholder-question logging. Works in Claude Code and VS Code Copilot. |
| **HELIX artifact pack** (`workflows/activities/`) | Six `GATE.yaml` files (entry/exit criteria with automated and manual checks) and nine artifact types. Each artifact has `template.md`, `prompt.md`, `example.md`, and `meta.yml`. |
| **Theme catalog** (`workflows/resources/themes/`) | Four palette definitions plus themed seed dashboards. |
| **Intake and scope guides** (`assets/`) | `tableau-intake.md`, `lakeview-intake.md`, `restyle-cycle.md`, and `prompt-style-guide.md`, which sets the rules for Build's Genie prompts. |
| **`list_dashboard_structure.py`** | Finds `.lvdash.json` files in a repo and summarizes their pages, widgets (stable ids, types, titles, datasets, fields, grid position), datasets and calculated columns (with optional SQL), and the current theme. Used for restyles and as-built inventories. Standard library only. |
| **`list_workbook_structure.py`** | Parses a Tableau `.twb`/`.twbx`: dashboards and their zones, worksheets (marks, shelves, encodings, fields), live and extract connections, and calculated fields. Calculated fields are classified as simple, LOD, or table-calc, so only the hard ones get flagged. Standard library only. |
| **`read_hyper_schema.py`** | Reads a packaged `.hyper` extract's real tables, columns, types, row counts, and sample rows. This checks the actual grain instead of trusting the workbook XML. Requires `tableauhyperapi`. |
| **Install scripts** (`scripts/install-skill.ps1` / `.sh`) | Install the skill into a user profile or vendor it into a team repo (`.github/skills/` or `.claude/skills/`). |

**Prerequisites:** a Databricks workspace, the Databricks CLI with a profile (always confirmed, never
auto-selected), a SQL warehouse, and Unity Catalog tables. Python 3 is needed only for the Tableau and
restyle paths.

## Roadmap

- **Pattern matching to existing dashboards.** New dashboards inherit the design patterns of the
  existing set before falling back to best practices.
- **Enhance-dashboard mode.** Add a new tab to an existing dashboard, matching its style and bringing in
  new datasets.

---
*Apache 2.0 · © 2026 Synaptiq · All example data is synthetic (Tuva Project data model).*
