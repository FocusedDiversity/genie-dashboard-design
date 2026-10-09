# Widget Inventory: [Dashboard Name]

**Brief**: [link to dashboard-brief.md]
**Date**: [YYYY-MM-DD]

## Pages

| # | Page | Purpose (1 sentence) |
|---|---|---|
| 1 | [name] | [what users do here] |

## Inventory

One row per widget. Ids are permanent: retire with strikethrough, never reuse.

| ID | Page | Row | Widget | Type | Metric & aggregation | Source (full path) | Filters | Unit | Target | Source Widget |
|---|---|---|---|---|---|---|---|---|---|---|
| W-101 | [page] | 1 | [title as it will appear] | counter \| bar \| line \| donut \| table | [e.g., distinct person_id where active] | [catalog.schema.table] | [all / list / none] | [unit] | [value or –] | [widget `name` from the .lvdash.json, or –] |

ID convention: W-1xx page 1, W-2xx page 2, W-3xx page 3; gaps are fine.
Source Widget is filled only when the inventory was extracted from an existing
dashboard; it is the binding Deploy uses to find the real widget.

## Global Filters

| Filter | Field | Cardinality | Default | Exempt widgets (why) |
|---|---|---|---|---|
| [name] | [field] | [~N] | [All] | [W-### — reason, or none] |

## Open Questions

- [Anything blocking Design — mark [NEEDS CLARIFICATION] to hold the gate]
