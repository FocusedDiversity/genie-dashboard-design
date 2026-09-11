---
name: genie-dashboard-design
description: 'Design and build Databricks AI/BI Genie dashboards through the six HELIX activities: Frame (brief & widget inventory), Design (HTML mockup & decisions), Test (baseline SQL before prompts), Build (Genie prompt catalog), Deploy (verified rollout), Iterate (drift & feedback). Use when creating new analytics dashboards, migrating existing dashboards, or running another cycle on a deployed one.'
argument-hint: 'Describe your dashboard vision (e.g., "Members & claims dashboard for healthcare analytics")'
---

# Genie Dashboard Design — HELIX Workflow

A HELIX-methodology workflow for designing and building Databricks AI/BI Genie
dashboards. Work moves through six activities, each producing versioned
artifacts in the working repo under `docs/helix/`, each ending in a gate the
stakeholder approves before the next activity starts.

This skill ships with a HELIX artifact pack at `workflows/activities/` in the
plugin root (`${CLAUDE_PLUGIN_ROOT}`). Each activity there has a `GATE.yaml`
(entry/exit requirements) and artifact folders with `template.md`, `prompt.md`,
`example.md`, and `meta.yml`. **Follow those files — they are the authority for
each artifact's structure and rules.** This document is the orchestration map.

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
  `skills/genie-dashboard-design/assets/tableau-intake.md` instead of a
  generic document read.

A stakeholder whose materials don't fit their stated choice (they picked
"blank slate" but then mention a PRD) is not a problem — ingest what's
actually offered; the choice sets expectations for the interview, it doesn't
gate what's allowed.

---

## The Spiral

| # | Activity | Artifacts produced (`docs/helix/…`) | Gate question |
|---|----------|-------------------------------------|---------------|
| 01 | **Frame** | `01-frame/dashboard-brief.md`, `01-frame/widget-inventory.md` | Is this the right dashboard? |
| 02 | **Design** | `02-design/dashboard-mockup.html`, `02-design/design-decisions.md` | Is this what it should look like? |
| 03 | **Test** | `03-test/widget-test-plan.md` (baselines **executed**) | Do we know what correct means? |
| 04 | **Build** | `04-build/prompt-catalog.md` | Are the prompts written to spec? |
| 05 | **Deploy** | `05-deploy/deployment-guide.md` (verification **recorded**) | Does the live dashboard pass its checks? |
| 06 | **Iterate** | `06-iterate/iteration-log.md` | What did we learn; spiral again or close? |

**Traceability spine**: every widget gets a `W-###` id in Frame. The mockup
tags it (`data-widget-id`), Test verifies it (`T-###`), Build prompts it,
Deploy records its PASS/FAIL. No orphans in either direction.

**Test before Build is the point.** Genie writes SQL nondeterministically.
The test plan's deterministic baseline SQL — written and executed *before any
prompt exists* — is the contract Genie's output must match. Skipping ahead to
prompts is the one shortcut this workflow forbids.

---

## Running an Activity

For each activity, in order:

1. **Check the entry gate** — `workflows/activities/<NN-name>/GATE.yaml`
   `entry_requirements`. If the previous activity's artifacts are missing or
   unapproved, go back.
2. **Produce each artifact** using its `prompt.md` (process & rules) and
   `template.md` (structure), writing output to the location in `meta.yml`
   (always `docs/helix/<NN-name>/…` in the working repo). Consult `example.md`
   for the quality bar.
3. **Self-check the exit gate** — run the automated checks (file existence,
   grep patterns) yourself; walk the manual checklist honestly.
4. **Present the gate** to the stakeholder: what was produced, the judgment
   calls, the open questions. Wait for explicit approval
   ("Proceed to <next activity>") or revise.

Activity-specific notes:

- **Frame**: act on the starting point already chosen in Step Zero above (see
  dashboard-brief's "Step Zero: Existing Requirements Intake" for the
  mechanics of ingesting whatever was supplied — files, pasted text, links,
  or a Tableau workbook via
  `skills/genie-dashboard-design/assets/tableau-intake.md`). Ingest anything
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
  `skills/genie-dashboard-design/assets/prompt-style-guide.md`, dedupe/null/
  grain language copied verbatim from design-decisions. Pre-write fallback
  views for window-logic widgets.
- **Deploy**: execute the creation steps, then run every T-### against the
  live dashboard and record outcomes. FAIL → re-prompt rule-first once →
  fallback view → waiver. Inspect generated SQL for window-logic checks even
  when the number matches.
- **Iterate**: append-only log — dated feedback, periodic baseline re-runs
  (drift), alert-noise review. Cycle ends "next cycle scoped" (returns to
  Frame) or "closed", never by silence.

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

1. **Artifacts are the memory.** Decisions live in `docs/helix/`, not in chat
   history or meeting recall. If it mattered, it's written.
2. **Clarity first.** Exact table paths, explicit aggregation, named null
   handling — in briefs, decisions, tests, and prompts alike.
3. **No double-counting.** Grain and dedupe rules are stated once in Design
   and copied verbatim everywhere they apply.
4. **Verify, then trust.** A matching number with uninspected SQL is a bug
   waiting for a data shift.
5. **The spiral, not the line.** Change requests re-enter at Frame. Editing a
   deployed prompt without updating its test is how dashboards rot.
