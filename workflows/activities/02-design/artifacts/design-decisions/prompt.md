# Generating Design Decisions

Write `docs/helix/02-design/design-decisions.md` from `template.md` while (not
after) building the mockup — every judgment call made in the mockup gets its
line here the moment it is made.

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
