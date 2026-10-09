# Maintaining an Iteration Log

Create `dashboards/<slug>/docs/helix/06-iterate/iteration-log.md` from
`template.md` at release; append to it for the life of the dashboard.

## Rules

- Feedback is recorded when received, dated, with its source. Paraphrase later
  if needed; capture verbatim first.
- Drift checks re-run the actual T-### SQL from the test plan — the baselines
  were written to be re-run; use them. A drifted check is either a data issue
  (escalate to the source owner) or Genie SQL that silently changed
  (re-verify the widget) — name which.
- Where the dashboard raises alerts, review noise: thresholds that fired
  daily get tuned or defended in writing.
- Every accepted change request enters the parking lot with enough scope to
  Frame from; the next cycle starts at Frame, not at prompt-editing.
- Close the loop explicitly: a cycle ends "next cycle scoped" or "closed",
  never by silence.
