# Genie Prompt Catalog: [Dashboard Name]

**Inventory**: widget-inventory.md ([version]) · **Test plan**: widget-test-plan.md ([version])

## Datasets

| Dataset | SQL | Used by |
|---|---|---|
| [name] | `SELECT ... FROM catalog.schema.table WHERE ...` | [pages/widgets; note filter-scoping reasons for extra datasets] |

## Prompts by Page

### Page: [Page Name]

**W-### — [Widget Title]** · verified by T-###
```
Show [visualization] of [metric] from [catalog.schema.table]
[where clause] [grouping] titled "[exact inventory title]".
[dedupe/null/grain language from design-decisions, verbatim]
[formatting: currency, percent, decimals, sort]
```

## Fallback Views

For widgets where Genie's generated SQL fails its T-### check twice, point the
widget at a view instead and simplify the prompt:

```sql
CREATE OR REPLACE VIEW [catalog.schema.v_name] AS
-- deterministic SQL from the test plan baseline
```

## Traceability

| W-### | Prompt present | T-### | Notes |
|---|---|---|---|
| W-101 | yes | T-101 | |
