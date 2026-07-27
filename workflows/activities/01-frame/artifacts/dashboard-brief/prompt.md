# Generating a Dashboard Brief

Interview the stakeholder, then write `docs/helix/01-frame/dashboard-brief.md`
from `template.md`.

## Gather (ask, don't assume)

1. **Purpose**: what business problem, what decision does it enable
2. **Audience**: roles, frequency, glance vs. dig usage
3. **Data sources**: full `catalog.schema.table` paths, join keys, refresh cadence
4. **KPIs**: the metrics that matter, targets if any
5. **Filters**: what users slice by, sensible defaults
6. **References**: existing dashboards to match or replace, style constraints

## Verify before writing

- Confirm each named table exists (DESCRIBE or a LIMIT 1 query) and note its grain.
- For each rate/percentage metric, pin down numerator and denominator with the
  stakeholder — do not accept "% denied" without the rule for the denominator.
- For each source table, identify the double-counting risk (claim lines vs claims,
  reruns, multiple grains) and record the prevention rule.

## Rules

- State WHAT is measured, never HOW Genie will be prompted — prompt wording is
  the prompt-catalog's authority in Build.
- Unknowns get `[NEEDS CLARIFICATION: question]` inline. The Frame exit gate
  blocks while any marker remains.
- Metric definitions must be executable by a stranger: "distinct person_id per
  payer_type", not "member count".
