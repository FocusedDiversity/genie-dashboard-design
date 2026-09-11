# Generating Design Decisions

Write `docs/helix/02-design/design-decisions.md` from `template.md` while (not
after) building the mockup — every judgment call made in the mockup gets its
line here the moment it is made.

## Step Zero: Theme Selection

Before any mockup work starts, present the catalog in
`workflows/resources/themes/README.md` to the stakeholder — the table of
theme id, persona fit, and default mode is enough; show swatches if useful.
Ask which fits this dashboard's audience. If they have no preference,
recommend by persona fit (default: `wanderbricks` for internal/technical
dashboards, `clinical-slate` for healthcare/executive) and confirm before
proceeding. Record the choice, rationale, mode, and any per-widget overrides
in the Theme Selection section immediately — the mockup is built from this
theme's `uiSettings.theme`, so an unrecorded or wrong theme choice means
rebuilding the mockup.

If the brief's Source Documents table lists an existing mockup, wireframe,
brand/style doc, or Tableau workbook (its `<style>`/`<color-palette>`
elements — see `skills/genie-dashboard-design/assets/tableau-intake.md`),
present it alongside the catalog: does one catalog theme already match its
colors/fonts/corner-radius, or does the pick need per-widget overrides to get
closer? Note the source doc, the reconciliation, and any gaps that remain
unmatched in the Theme Selection section — don't silently pick a catalog
theme that ignores supplied styling.

## Rules

- Aggregation rules are the load-bearing section: state each one so Test can
  translate it to a baseline query without asking questions. "Avoid double
  counting" is not a rule; "sum max(charge_amount) per claim_id" is.
- Attribute every rule to the W-### widgets it governs.
- Record what was rejected and why — the next cycle re-litigates anything
  undocumented.
- Filter exemptions are decisions, not omissions: name the widget and reason
  (e.g., "W-101 lifetime total is date-filter-exempt by definition").
- Keep claims scoped: this artifact records design authority; prompt wording
  belongs to Build, verification belongs to Test.
