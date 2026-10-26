# Iteration Cycle (Step Zero option 6)

This governs a cycle run against a dashboard that **already has a HELIX record**
(`dashboards/<slug>/docs/helix/`) from an earlier cycle. It covers additions,
fixes, rebinds, new pages, or new definitions. All six activities still run. What
changes is that every activity starts from the record instead of from
scratch, and must prove that what it did not touch did not move.

`restyle-cycle.md` still governs any part of the request that is a restyle.
`lakeview-intake.md` is not re-run: the record already holds the mined
dashboard.

## Before Frame: read the record

Read these before asking anything. They are the stakeholder's earlier answers,
and asking them again costs a round-trip each:

| Read | Use it for |
|---|---|
| `06-iterate/iteration-log.md`: the last cycle's **Next Cycle** note and **Parking Lot** | Candidate scope. Items the request resolves get marked resolved at Iterate |
| `06-iterate/stakeholder-inputs.md`: **standing preferences**, **overridden recommendations**, **"What to prepare before the next cycle"** | Apply them without asking. Record each as *inherited, not asked* in this cycle's opening brief |
| `01-frame/dashboard-brief.md`: personas, actions, constraints | Inherited unchanged unless the request changes them |
| `02-design/design-decisions.md`: theme, aggregation rules, header / color rules | Inherited. Reuse rule text verbatim in new prompts and tests |
| `05-deploy/deployment-guide.md`: the **current release file and SHA** | The base this cycle builds from, and the rollback |

Then confirm the release file in the repo is what is live. If the last commit
message or the stakeholder mentions a live-only edit, ask before building on
the file: a change made only in the workspace is lost on re-import.

## Conventions

- **Cycle number**: N = the last cycle in the iteration log + 1. Tag every new
  section "Cycle N" or "(CN)".
- **Questions**: logged per cycle as **CN Q1, Q2, …**, numbered from 1 in each cycle and cited as "Q##" inside that cycle's sections.
- **Append, never rewrite**: each artifact gains a `## Cycle N …` section.
  - Earlier cycles' text stays as the record of what was true then. When something is superseded, say so in the new section ("supersedes the C2 W-118 entry") rather than editing the old one.
  - Header lines (Date, Status, Mockup) are the only lines updated in place.
- **Widget IDs are permanent**: new widgets continue the page's W-### series
  (a new page takes the next hundred: W-6xx). Retired widgets are struck
  through, never reused.
- **Inventory**: add a "Cycle N changes" table (ID, Source Widget, change,
  driver Q##) rather than editing the census rows.
- **Release files**: build from the last release file, with a script that
  always rebuilds from a frozen copy of that release so it can run any number
  of times.
  - Edit only the file the stakeholder named; a bundle-path original stays untouched unless they say otherwise.
  - If the stakeholder wants a side-by-side comparison in the workspace, keep the previous release as `<Dashboard Name>_old.lvdash.json` and edit the copy.

## Per activity

**01 Frame**:
- Step Zero has been answered (option 6); don't re-ask the open question.
- Append "Cycle N Scope" to the brief:
  - the request quoted verbatim
  - a table mapping each requested item to W-### ids, source, and data readiness
  - an explicit **out of scope** list
- Ask only what the record and the request leave open. Profile any new source (row counts in the target environment, date coverage) before asking, so Blocked / Live is known at Frame.
- If part of the request crosses a restyle fence, record it as a **named exception**.

**02 Design**:
- The theme and every earlier decision are inherited; the mockup is the previous cycle's mockup plus this cycle's changes, driven by real profiled values where possible.
- Save the previous mockup as `dashboard-mockup-c{N-1}-before.html` and link it from the new one ("Compare: before").
- Write only the changed decisions under "Cycle N Decisions".

**03 Test** needs two families of checks, both required:
- **Change checks**: baseline SQL for every changed or new widget, executed before Build, plus cross-tab identity checks where a metric name appears on more than one page.
- **Regression checks**: a structural diff of the build against the previous release. Pages, widget set, positions, every untouched widget's spec and queries, and every untouched dataset must be byte-identical. Only the listed changes may differ.

Write the regression rule before Build; run it after.

**04 Build**:
- Prompts for new or changed widgets only. Everything else is "unchanged (CN−1 entries)" in the traceability table.
- Verify the built measure expressions against the Test baselines (expand them from the file and run them) as well as the structural diff.

**05 Deploy**:
- Expected values are same-day: re-run the baselines on the check day if the windows move.
- The stakeholder usually imports. Compare against the previous release still live in the workspace.
- Live feedback becomes "Deploy fix round K" sections, not a new cycle, unless the stakeholder chooses otherwise.
- A **new** request arriving at Deploy is a sequencing question: fold it into this cycle, or close this one and run it as N+1. Ask; don't assume.

**06 Iterate**:
- Append "Cycle N" to the iteration log: change log, feedback, drift, and a **parking-lot status table** that marks what this cycle resolved, partly resolved, or made worse, then lists new items.
- Append a "Cycle N" stakeholder-inputs record: the totals, every CN Q with the options offered, verbatim gates, overridden recommendations, standing preferences confirmed or newly found, and what to prepare before cycle N+1.
- Update the header line listing each cycle's status.

## Lessons carried from earlier iterations

- **Metric-view sources** cannot be joined, even with a one-row cross join. Put window bounds inline.
- **Window-function columns** inside a dataset ignore dashboard field filters. Per-entity "best outcome" logic belongs in distinct-count measures.
- **Databricks SQL string literals** escape quotes with `\'`; `''` concatenates adjacent literals.
- **Viewer-facing text** (definitions, notes, titles) carries no internal widget ids, work-item numbers, or planning-document names. Keep traceability in a non-exported field.
- **Metric names on several tabs**: when the same name appears on more than one tab, run a cross-tab consistency check under one population before assuming they agree. Compare on rank or code fields, not label text.
