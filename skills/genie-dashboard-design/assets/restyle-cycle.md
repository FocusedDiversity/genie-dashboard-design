# Restyle Cycle (Step Zero option 5)

The scope authority for a cycle run against a dashboard that is already live,
where the only thing allowed to change is how it looks. `lakeview-intake.md`
covers mining the dashboard; this covers what each activity does with it.

All six activities still run. A restyle narrows what may change, not which
gates you pass. The traceability spine is unchanged: `W-###` in Frame, tagged
in the mockup, `T-###` in Test, carried through Build, PASS/FAIL in Deploy.

## The fence

**In scope** — the dashboard's `uiSettings.theme` block and anything that
fights it:

- canvas, widget, and border colors; font family and font color
- the selection/accent color and the `visualizationColors` series palette
- widget chrome: corner radius, header alignment, borders
- styling hard-coded inside widgets that contradicts the new theme — inline
  `color:` / `font-family:` in text widgets, per-widget color overrides in
  chart encodings

**Out of scope** — everything that decides what a number *is*:

- metrics, aggregations, dataset SQL, dataset columns
- the set of widgets, their titles, their types
- grid layout and widget positions, page structure and page order
- filters and their wiring

A restyle that renames a widget, moves it, or changes what it computes is not
a restyle. When the stakeholder asks for one of those — and they will, because
looking closely at a dashboard surfaces everything else wrong with it — record
it in the brief's Restyle Scope as out of scope and in Iterate's parking lot
for the next cycle. Don't fold it in. The whole value of this cycle is that
Test can prove nothing but appearance changed, and that proof dies the moment
one metric moves with it.

The one exception worth naming: a widget type change forced purely by the
theme (a chart the new palette makes unreadable) is a design decision, not a
scope break — but it needs the stakeholder's explicit approval at the Design
gate, recorded in design-decisions with the reason.

## Per activity

**01 Frame** — the inventory is an as-built census, not a proposal. Every
widget in the file gets a row with its `name` in the Source Widget column and
its title copied verbatim. The brief records the dashboard as it is plus a
**Restyle Scope** section: the file being restyled, the current theme, the
reason for the restyle, what's in and out, and the invariance requirement. No
new KPIs are invented; no existing one is re-litigated.

**02 Design** — theme selection is the deliverable, not a preliminary. The
mockup reproduces the production layout exactly — same pages, same widgets,
same grid positions — rendered in the proposed theme, so the stakeholder is
comparing appearance and only appearance. design-decisions carries a
before/after palette table and a decision for every piece of hard-coded
styling the intake found. Layout rationale is inherited, not rewritten.

**03 Test** — two families of checks, and both are required:

- **Invariance** (`T-1xx`): baseline SQL for each P0 widget, executed against
  the dashboard *as it is today*, results recorded. After the restyle the same
  queries run again and must match exactly. This is the proof that a cosmetic
  change stayed cosmetic.
- **Conformance** (`T-8xx`): the resolved colors and fonts match the selected
  theme's hex values; contrast ratios pass; no color or chart type on the
  theme's `banned` list appears; every hard-coded style the intake flagged is
  either reconciled or explicitly waived.

**04 Build** — no new prompts exist, so the catalog documents the existing
ones. Reverse-engineer each widget's entry from its dataset query and mark it
`unchanged (restyle)`. The catalog also carries the target `uiSettings.theme`
block — in a restyle that block *is* the build output. A widget whose prompt
you cannot reconstruct is flagged, not skipped; the gate's "no widget skipped"
rule holds here exactly as it does in a new build.

**05 Deploy** — work on a side-by-side copy, never the live file. Apply the
theme, re-run every invariance baseline against the restyled dashboard, and
record PASS/FAIL per `T-###` the same as any deployment. A single invariance
FAIL blocks the gate: it means the restyle changed a number, which is the one
outcome this cycle exists to prevent. Record the rollback (the original theme
block from Frame) before publishing, and confirm permissions, sharing, and
schedules carried over to the copy.

**06 Iterate** — unchanged. Log the theme rollout as the cycle's change, carry
the out-of-scope requests into the parking lot with the reason they were
deferred, and note whether the theme should become the house default for other
dashboards in the repo.
