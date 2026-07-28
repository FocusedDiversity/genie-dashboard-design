# Deployment Guide: [Dashboard Name]

**Catalog**: prompt-catalog.md ([version]) · **Test plan**: widget-test-plan.md ([version])
**Deployed**: [YYYY-MM-DD] by [name] · **Workspace**: [url/name] · **Warehouse**: [name]

## Prerequisites

- [ ] Source tables exist and are readable by the dashboard's run-as principal
- [ ] Warehouse assigned; fallback views created if the catalog defines them
- [ ] [Anything dashboard-specific: history depth, permissions, schedules]

## Creation Steps

1. Import the themed seed: workspace folder → **Import** →
   `workflows/resources/seed.lvdash.json` (from the genie-dashboard-design
   plugin) → rename the dashboard to **[name]**. This applies the canonical
   theme before any widget exists. (Fallback if import is unavailable: create
   a blank dashboard, then set every value from
   `workflows/resources/dashboard-theme.json` in the theme editor.)
2. Data tab: create each dataset from the catalog's Datasets table
3. Create pages named exactly as the inventory; add filter widgets per page
4. Per widget, in inventory order: add widget, paste the W-### prompt, confirm
   the rendered title matches
5. [Publishing, embedding, schedule steps]

## Verification Record

Run every T-### from the test plan against the live dashboard.

| T-### | W-### | Date | Outcome | Notes / disposition |
|---|---|---|---|---|
| T-101 | W-101 | [date] | PASS / FAIL / BLOCKED | [for FAIL: re-prompted → PASS; fallback view; or waiver + owner] |

- Generated-SQL inspection performed for: [T-### list — window-logic checks]

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| [doubled values] | [Genie dropped dedupe] | [inspect SQL; re-prompt with rule sentence first; fallback view] |

## Access & Rollback

- **Sharing**: [groups/users and permission levels]
- **Rollback**: [how to unpublish / restore previous dashboard version]
