# Generating a Deployment Guide

Write `dashboards/<slug>/docs/helix/05-deploy/deployment-guide.md` from
`template.md` as you deploy — it is a record of what happened, not a plan of
what should.

## Process

1. Fill prerequisites and creation steps from the prompt-catalog before
   touching the workspace; execute them in order.
2. After all widgets exist, run every T-### against the live dashboard the
   same day (re-run baselines first if source data moves daily).
3. Record each outcome. For FAIL: re-prompt once with the rule sentence moved
   to the front; if it fails again, switch to the catalog's fallback view.
   Both dispositions get noted. Anything else needs a waiver with an owner.
4. Inspect Genie's generated SQL for every window-logic check (dedupe,
   baselines-vs-current) — a matching number can still hide wrong SQL that
   diverges when data shifts.
5. Record sharing, run-as principal, and the rollback path.

## Rules

- No "will verify later" — the Deploy exit gate greps for recorded outcomes.
- The verification table is evidence: dates, outcomes, dispositions. Keep it
  honest; Iterate reads it.

## Restyle cycles

If the brief's Source Documents table lists a Lakeview dashboard export,
deployment is a theme swap on a copy — see `assets/restyle-cycle.md`. The
process above still applies; these constraints are added:

1. Work on the side-by-side copy in `dashboards/<slug>/`, never the live file.
   Record the original `uiSettings.theme` block (from the brief's Restyle
   Scope) as the rollback before changing anything.
2. Apply the target theme block from the prompt-catalog verbatim. Don't
   hand-tune hex values during deployment — a value worth changing is a
   Design decision, and it goes back a gate.
3. Re-run every invariance baseline against the restyled dashboard and compare
   to the pre-restyle results recorded in Test. **Any difference blocks the
   gate.** A restyle that moves a number has changed something it was not
   allowed to change; find it rather than widening the tolerance.
4. Walk the T-8xx conformance checks against the rendered dashboard, in the
   theme's primary mode.
5. Confirm permissions, sharing, run-as principal, schedules, and alerts all
   carried over to the copy — none of them live in the `.lvdash.json`, so they
   are the usual thing a side-by-side swap silently drops.
