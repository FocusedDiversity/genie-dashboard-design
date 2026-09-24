---
name: genie-dashboard-design
description: 'Design and build Databricks AI/BI Genie dashboards through the six HELIX activities: Frame (brief & widget inventory), Design (HTML mockup & decisions), Test (baseline SQL before prompts), Build (Genie prompt catalog), Deploy (verified rollout), Iterate (drift & feedback). Use when creating new analytics dashboards, migrating existing dashboards, or running another cycle on a deployed one.'
argument-hint: 'Describe your dashboard vision (e.g., "Members & claims dashboard for healthcare analytics")'
---

# Genie Dashboard Design — HELIX Workflow

A HELIX-methodology workflow for designing and building Databricks AI/BI Genie
dashboards. Work moves through six activities, each producing versioned
artifacts in the working repo under `dashboards/<slug>/docs/helix/`, each ending
in a gate the stakeholder approves before the next activity starts.

This skill ships with a HELIX artifact pack at [`workflows/activities/`](./workflows/activities/).
Each activity there has a `GATE.yaml` (entry/exit requirements) and artifact
folders with `template.md`, `prompt.md`, `example.md`, and `meta.yml`.
**Follow those files — they are the authority for each artifact's structure and
rules.** This document is the orchestration map.

**Every path in this skill and its artifact pack is relative to this skill's own
folder** — `workflows/…`, `assets/…`, `references/…` all resolve from here, not
from the repo you are working in.

**Artifacts you *produce* go to `dashboards/<slug>/docs/helix/…`** in the working
repo. Every dashboard owns its own HELIX record, so one repo holds many of them
side by side. Establish `<slug>` once, in Frame, before writing anything: propose
a short `snake_case` name from the dashboard's title and confirm it with the
stakeholder — don't derive it silently, because the folder name is usually
shorter than the dashboard name ("Claims Overview (Revised)" →
`claims_overview`). Reuse the existing folder when one already exists for
that dashboard. Wherever `<slug>` appears in a `meta.yml` output location or a
`GATE.yaml` path, substitute the confirmed value.

```
dashboards/<slug>/
  <Dashboard Name>.lvdash.json   the dashboard itself, when the repo holds it
  datasets/                      dataset SQL and refresh scripts
  docs/helix/
    01-frame/    dashboard-brief.md, widget-inventory.md, sources/
    02-design/   dashboard-mockup.html, design-decisions.md, <theme>.json
    03-test/     widget-test-plan.md, plus the baseline .sql files it runs
    04-build/    prompt-catalog.md
    05-deploy/   deployment-guide.md
    06-iterate/  iteration-log.md, stakeholder-inputs.md
```

`01-frame/sources/` holds copies of whatever the stakeholder supplied — PRDs,
data dictionaries, decks, source SQL — so the brief can link to them and they
outlive the conversation. `02-design/<theme>.json` is a copy of the chosen
theme, so the mockup's colors can be checked against it later. Baseline SQL long
enough to hurt the test plan's readability lives beside it as `.sql` files
rather than inline.

---

## Step Zero: Starting Point

Before anything else — before checking any gate, before Frame's interview,
before even the six activities below are relevant — ask the stakeholder which
of these best matches their situation. This is the first thing the stakeholder
sees, even in response to a one-line invocation like
`/genie-dashboard-design:genie-dashboard-design Members & claims dashboard`:

1. **Blank slate** — no existing materials; interview me from scratch to
   build requirements, design, personas, etc.
2. **Requirements document only** — a data dictionary, PRD, or similar
   written requirements, but no wireframe or mockup.
3. **Requirements document + wireframe/mockup** — both a requirements
   document and a design mockup/wireframe.
4. **Existing Tableau workbook (.twb/.twbx)** — an existing Tableau
   dashboard to convert.
5. **Existing production dashboard — restyle only** — a Databricks dashboard
   already live, to be re-themed (colors, typography, chrome) without changing
   its metrics, queries, widgets, or layout.

The answer decides what Frame's Step Zero (dashboard-brief's "Step Zero:
Existing Requirements Intake") does — it acts on the choice made here rather
than asking the open-ended version of this question again:

- **1** → skip straight to the interview; record "None provided" in Source
  Documents.
- **2** → ask for the document (file path, pasted text, or link); ingest it,
  then interview to fill what it doesn't answer.
- **3** → ask for both; ingest each. The mockup also seeds Design's layout
  and widget-inventory's candidate widgets.
- **4** → ask for the `.twb`/`.twbx` path; follow
  `assets/tableau-intake.md` instead of a
  generic document read.
- **5** → follow `assets/lakeview-intake.md` to find the repo's
  `.lvdash.json` files, ask which one, and mine it into the brief and
  inventory. Then follow `assets/restyle-cycle.md`, which is the scope
  authority for all six activities in a restyle.

A stakeholder whose materials don't fit their stated choice (they picked
"blank slate" but then mention a PRD) is not a problem — ingest what's
actually offered; the choice sets expectations for the interview, it doesn't
gate what's allowed.

---

## The Spiral

| # | Activity | Artifacts produced (`dashboards/<slug>/docs/helix/…`) | Gate question |
|---|----------|-------------------------------------|---------------|
| 01 | **Frame** | `01-frame/dashboard-brief.md`, `01-frame/widget-inventory.md` | Is this the right dashboard? |
| 02 | **Design** | `02-design/dashboard-mockup.html`, `02-design/design-decisions.md` | Is this what it should look like? |
| 03 | **Test** | `03-test/widget-test-plan.md` (baselines **executed**) | Do we know what correct means? |
| 04 | **Build** | `04-build/prompt-catalog.md` | Are the prompts written to spec? |
| 05 | **Deploy** | `05-deploy/deployment-guide.md` (verification **recorded**) | Does the live dashboard pass its checks? |
| 06 | **Iterate** | `06-iterate/iteration-log.md`, `06-iterate/stakeholder-inputs.md` | What did we learn; spiral again or close? |

**Traceability spine**: every widget gets a `W-###` id in Frame. The mockup
tags it (`data-widget-id`), Test verifies it (`T-###`), Build prompts it,
Deploy records its PASS/FAIL. No orphans in either direction.

**Test before Build is the point.** Genie writes SQL nondeterministically.
The test plan's deterministic baseline SQL — written and executed *before any
prompt exists* — is the contract Genie's output must match. Skipping ahead to
prompts is the one shortcut this workflow forbids.

**Restyle cycles run all six activities.** Starting point 5 narrows what may
change, not which activities happen: the inventory is extracted as-built
instead of invented, Design's theme choice becomes the deliverable, Test proves
the numbers did not move, and Build documents the existing prompts unchanged.
`assets/restyle-cycle.md` is the scope authority; every activity note below
defers to it when the cycle is a restyle.

---

## Running an Activity

For each activity, in order:

1. **Check the entry gate** — `workflows/activities/<NN-name>/GATE.yaml`
   `entry_requirements`. If the previous activity's artifacts are missing or
   unapproved, go back.
2. **Produce each artifact** using its `prompt.md` (process & rules) and
   `template.md` (structure), writing output to the location in `meta.yml`
   (always `dashboards/<slug>/docs/helix/<NN-name>/…` in the working repo).
   Consult `example.md` for the quality bar.
3. **Self-check the exit gate** — run the automated checks (file existence,
   grep patterns) yourself; walk the manual checklist honestly.
4. **Present the gate** to the stakeholder: what was produced, the judgment
   calls, the open questions. Wait for explicit approval
   ("Proceed to <next activity>") or revise.

**Throughout every activity**: each question put to the stakeholder gets logged
when it is answered — the question and the conflict that forced it, every option
offered and which was recommended, what they chose (verbatim for gate approvals),
and what changed in the build as a result. Iterate's `stakeholder-inputs.md` is
assembled from these entries and closes the cycle; it is not reconstructable from
memory afterwards. See 06-iterate's stakeholder-inputs artifact for the format.

Activity-specific notes:

- **Frame**: act on the starting point already chosen in Step Zero above (see
  dashboard-brief's "Step Zero: Existing Requirements Intake" for the
  mechanics of ingesting whatever was supplied — files, pasted text, links,
  or a Tableau workbook via
  `assets/tableau-intake.md`). Ingest anything
  supplied first; use the interview to fill gaps and verify claims, not
  repeat what the docs already establish. Log every source doc in
  the brief's Source Documents table — its content keeps surfacing downstream
  (widget-inventory mines mockups or Tableau worksheets for candidate
  widgets, design-decisions reconciles style docs or a workbook's color
  palette against the theme catalog, prompt-catalog reuses a data
  dictionary's terms verbatim). Then
  interview before writing — purpose, audience, data sources (verify
  tables exist), KPI definitions (pin numerators/denominators), filters. VERY IMPORTANT: Ask the the stakeholder to define things like how dashbaord is to be used, with specifics, by who (Personas), and what actionss will be taken base don the dashbaord. This information should inform the design.  Personas and Use become very improtant to account for by tabs, and widgets. Unknowns become `[NEEDS CLARIFICATION]` markers; the exit gate blocks while
  any remain.
- **Design**: **first, select a theme** — present the catalog in
  `workflows/resources/themes/README.md` (Wanderbricks, Clinical Slate,
  Executive Minimal — each with a stated persona fit) and get the
  stakeholder's pick before building anything; record it, the reason, mode,
  and any per-widget overrides in `design-decisions.md`'s Theme Selection
  section. Then the mockup: a browser-viewable HTML file imitating a
  published Databricks dashboard, styled from the selected theme's exact
  colors/font/corner-radius (not assumed dark, not assumed Wanderbricks) —
  Chart.js charts, live scenario-driven filters. Match
  `example-appointment-analytics.html` for layout and interactivity. Write
  `design-decisions.md` as you go, not after. Aggregation rules stated there
  must be SQL-translatable verbatim. Verify with the user data grains for data
  sets, and ensure that the mockup reflects the correct grain and
  deduplication rules. If any assumptions are made, they should be documented
  in the decisions artifact.
- **Test**: write baseline SQL per widget, **run it**, record results and
  dates. Choose exact/tolerance/invariant rules deliberately. Add
  dashboard-level checks (filter cascade, counter/table agreement,
  empty-slice).
- **Build**: one prompt per widget, style per
  `assets/prompt-style-guide.md`, dedupe/null/
  grain language copied verbatim from design-decisions. Pre-write fallback
  views for window-logic widgets.
- **Deploy**: execute the creation steps, then run every T-### against the
  live dashboard and record outcomes. FAIL → re-prompt rule-first once →
  fallback view → waiver. Inspect generated SQL for window-logic checks even
  when the number matches.
- **Iterate**: append-only log — dated feedback, periodic baseline re-runs
  (drift), alert-noise review. Cycle ends "next cycle scoped" (returns to
  Frame) or "closed", never by silence. **Then, as the final step of the whole
  cycle**, write `stakeholder-inputs.md`: every question the cycle put to the
  stakeholder, grouped by activity and numbered continuously, with the options
  offered, what they chose, what it changed — and a closing section on what to
  profile or decide up front so the next cycle doesn't have to ask again.
  Overridden recommendations and their reasoning matter most here; they are
  how a standing preference gets discovered.

The optional HELIX **Discover** activity (validating whether the dashboard is
worth building) precedes Frame when the opportunity itself is in question; use
the HELIX methodology repo's Discover artifacts if needed.

---

## Example Cycle (condensed)

> "Create a healthcare dashboard for members and claims on Tuva input layer tables."

1. **Frame**: brief + inventory (W-101 Total Members … W-203 Monthly Billed vs
   Paid), payer/date/state filters. Gate: stakeholder approves scope.
2. **Design**: stakeholder picks `clinical-slate` (healthcare audience) from
   the theme catalog; `dashboard-mockup.html` — two tabs, themed chrome,
   working payer-type filter re-rendering fake-but-plausible data; decisions
   record the theme choice and the max-per-claim charge rule. Gate:
   stakeholder clicks through, approves.
3. **Test**: T-101/T-201/T-202 baseline SQL run on the warehouse; results
   recorded (2.14M members, $412M billed, 6.8% denial). Gate: correct is now
   defined.
4. **Build**: prompt per widget, each ending with its rule sentence; fallback
   view `v_claim_amounts` pre-written.
5. **Deploy**: T-201 FAILs (Genie summed claim lines, 2.4x) → re-prompt
   rule-first → PASS; all outcomes recorded. Gate: live dashboard verified.
6. **Iterate**: analyst feedback on the denial definition → subtitle fix +
   parking-lot item → next cycle scoped.

---

## Key Principles

1. **Artifacts are the memory.** Decisions live in
   `dashboards/<slug>/docs/helix/`, not in chat history or meeting recall. If
   it mattered, it's written.
2. **Clarity first.** Exact table paths, explicit aggregation, named null
   handling — in briefs, decisions, tests, and prompts alike.
3. **No double-counting.** Grain and dedupe rules are stated once in Design
   and copied verbatim everywhere they apply.
4. **Verify, then trust.** A matching number with uninspected SQL is a bug
   waiting for a data shift.
5. **The spiral, not the line.** Change requests re-enter at Frame. Editing a
   deployed prompt without updating its test is how dashboards rot.
