# Generating a Deployment Guide

Write `docs/helix/05-deploy/deployment-guide.md` from `template.md` as you
deploy — it is a record of what happened, not a plan of what should.

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
