# Dashboard Brief: [Dashboard Name]

**Stakeholder**: [name, role]
**Date**: [YYYY-MM-DD]
**Status**: Draft | Approved

## Source Documents

| Document | Type | What it provided |
|---|---|---|
| [name/link, or "None provided"] | data dictionary \| PRD \| mockup \| wireframe \| design doc \| Tableau workbook \| Lakeview dashboard export \| none | [e.g., "field names & grain for claims table", "target KPIs & audience", "3 worksheets mined for chart type/aggregation", "6 pages / 28 widgets mined as-built"] |

## Summary

[1–2 paragraphs: what business question this dashboard answers, for whom, and
what decision or action it enables. Write this last.]

## Problem & Audience

- **Problem**: [What is invisible, slow, or error-prone today without this dashboard?]
- **Audience**: [Roles who use it and how often — e.g., "analysts daily, VP weekly"]
- **Primary workflow**: [The glance-then-dig path: what users check first, what they drill into]

## Data Sources

| Table (full path) | Grain | Role | Known quality issues |
|---|---|---|---|
| [catalog.schema.table] | [one row per …] | [facts / dimension / snapshot] | [nulls, duplicates, lag] |

- **Join keys**: [e.g., person_id joins eligibility to patient]
- **Refresh cadence**: [nightly at HH:MM, etc.]

## KPIs & Metrics

For every metric, name the aggregation. For every rate, name numerator and denominator.

| Metric | Definition | Aggregation | Unit | Target |
|---|---|---|---|---|
| [name] | [e.g., Denial rate = claims with paid_amount 0 or null / all claims] | [distinct count / sum / max-per-id] | [percent, count, currency] | [value or n/a] |

## Filters & Drill-downs

| Filter | Field | Cardinality | Default | Applies to |
|---|---|---|---|---|
| [name] | [field] | [~N values] | [All / value] | [all pages / page X] |

- **Drill-down paths**: [which summaries lead to which detail views]

## Constraints & Assumptions

- [Grain rules — e.g., "grain pinned to 'overall' until regional data lands"]
- [Double-counting risks per table and the rule that prevents each]
- [Anything assumed about data conventions — flag with [NEEDS CLARIFICATION] until confirmed]

## Success Criteria

- [Observable, checkable post-release — e.g., "analysts stop running manual query X",
  "values match source dashboard Y within 1%"]

## Restyle Scope

[Restyle cycles only (Step Zero option 5) — delete this section otherwise.]

- **Dashboard**: [path to the .lvdash.json being restyled]
- **Current theme**: [the as-is `uiSettings.theme` values, or "Lakeview default"]
- **Reason for restyle**: [brand alignment, accessibility, consolidation, …]
- **In scope**: [theme, palette, typography, widget chrome — narrow this if the
  stakeholder narrowed it]
- **Out of scope**: metrics, SQL, datasets, widget set, grid layout, filters.
  [Name anything the stakeholder asked for that falls outside — it becomes a
  parking-lot item for a later cycle, not part of this one.]
- **Invariance requirement**: every widget returns the same values after the
  restyle as before. [Name any accepted exception and why.]
