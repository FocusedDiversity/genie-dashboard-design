# Deployment Guide: Synaptiq Healthcare Analytics (excerpt)

**Catalog**: prompt-catalog.md (v1.0) · **Test plan**: widget-test-plan.md (v1.0)
**Deployed**: 2026-07-27 by G. Fischer · **Workspace**: dbrks-ed5uat-ws01 · **Warehouse**: wh-analytics-serverless

## Prerequisites

- [x] dev.tuva_input_layer tables readable by dashboard principal
- [x] v_claim_amounts fallback view created

## Creation Steps

1. Workspace → Dashboards → Create dashboard: **Synaptiq Healthcare Analytics**
2. Datasets: `members`, `claims` per catalog
3. Pages: Members, Claims & Charges; filters: Date Range, Payer Type, State
4. Widgets pasted in inventory order; titles verified

## Verification Record

| T-### | W-### | Date | Outcome | Notes / disposition |
|---|---|---|---|---|
| T-101 | W-101 | 2026-07-27 | PASS | exact match 2,143,858 |
| T-201 | W-201 | 2026-07-27 | FAIL → PASS | Genie summed line-level charges (2.4x); re-prompted with max-per-claim sentence first; SQL now has the GROUP BY claim_id subquery |
| T-202 | W-202 | 2026-07-27 | PASS | 6.8% within tolerance |
| T-901 | — | 2026-07-27 | PASS | cascade verified incl. W-101 payer-narrowing |

- Generated-SQL inspection performed for: T-201, T-202

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Billed 2–3x expected | line-level sum, dedupe dropped | re-prompt rule-first; else point at v_claim_amounts |

## Access & Rollback

- **Sharing**: analytics-team (edit), operations-leads (view)
- **Rollback**: unpublish; previous draft retained by dashboard versioning
