# Generating a Stakeholder Inputs Record

Write `dashboards/<slug>/docs/helix/06-iterate/stakeholder-inputs.md` from
`template.md` as the **final step of the cycle**, after the iteration log.
`example.md` is the quality bar — match its level of specificity, not its length.

## Capture as you go, assemble at the end

Entries are logged **when the question is answered**, not reconstructed from memory at
the end — the same discipline the iteration log applies to feedback. For every
question put to the stakeholder in any activity, record four things while they are
still exact:

1. **The question as asked**, including the conflict or ambiguity that forced it —
   "the BRD says ~50 states, the column holds 15" is the reason the question exists
   and is more useful than the question alone.
2. **Every option offered**, marking which was recommended.
3. **What they chose** — verbatim where it was free text.
4. **What changed in the build as a result**: W-### widgets added, replaced, or
   retired, filters extended, a definition settled. "Nothing changed" is a valid
   answer and worth recording.

Only the synthesis — totals, result, and "what to prepare before the next cycle" — is
written at the end, once the whole cycle is visible.

## Rules

- Number questions continuously across the whole cycle, not per activity. The count is
  the point: it shows the stakeholder how much was asked of them, and where.
- Group by activity and round (Setup, Frame round 1, Frame round 2, Design, Deploy) so
  a reader can see where the cost fell.
- Inputs the stakeholder volunteered without being asked belong in the opening brief,
  separate from questions. So do constraints inherited from saved preferences or a
  prior cycle — flag those as not-asked, or the next cycle will assume they were
  agreed here.
- **Record every overridden recommendation and the reasoning behind it.** A
  stakeholder who rejects a recommendation is stating a constraint the workflow did
  not know about; that reasoning is the most reusable content in this document, and
  frequently becomes a standing preference worth naming as such.
- Gate approvals are quoted verbatim — "Approved", "Proceed to TEST" — since they are
  the authorization trail, not a summary of sentiment.
- The final section is written *for the stakeholder*, not for the archive: which
  questions existed only because the supplied documents disagreed with live data, and
  what profiling or up-front decisions would have prevented them. Name the specific
  query that would have caught each conflict — "cardinality of every filter column",
  not "profile the data better".
- A blank-slate cycle still gets this record. Its opening brief is thin and its
  question count is high; that contrast is exactly what the next cycle needs to see.
