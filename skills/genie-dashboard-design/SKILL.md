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

- **Frame**: interview before writing — purpose, audience, data sources (verify
  tables exist), KPI definitions (pin numerators/denominators), filters.
  Unknowns become `[NEEDS CLARIFICATION]` markers; the exit gate blocks while
  any remain.
- **Design**: the mockup is a browser-viewable HTML file imitating a published
  Databricks dashboard — dark chrome, Chart.js charts, live scenario-driven
  filters. Match `example-appointment-analytics.html`. Write
  `design-decisions.md` as you go, not after. Aggregation rules stated there
  must be SQL-translatable verbatim.
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
2. **Design**: `dashboard-mockup.html` — two tabs, Databricks chrome, working
   payer-type filter re-rendering fake-but-plausible data; decisions record the
   max-per-claim charge rule. Gate: stakeholder clicks through, approves.
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
