# Widget Inventory: Synaptiq Healthcare Analytics

**Brief**: [dashboard-brief.md](../dashboard-brief/example.md)
**Date**: 2026-07-27

## Pages

| # | Page | Purpose |
|---|---|---|
| 1 | Members | Enrollment volume, mix, and geography at a glance |
| 2 | Claims & Charges | Spend and denial monitoring with monthly trend |

## Inventory

| ID | Page | Row | Widget | Type | Metric & aggregation | Source (full path) | Filters | Unit | Target |
|---|---|---|---|---|---|---|---|---|---|
| W-101 | Members | 1 | Total Members | counter | distinct person_id | dev.tuva_input_layer.eligibility | all | count | – |
| W-102 | Members | 1 | Active Members | counter | distinct person_id where enrollment_end_date >= today or = 9999-12-31 | dev.tuva_input_layer.eligibility | all | count | – |
| W-103 | Members | 2 | Enrollment by Payer Type | donut | distinct person_id per payer_type | dev.tuva_input_layer.eligibility | all | count | – |
| W-104 | Members | 2 | Members by Age Band | bar | distinct person_id per age band (0-17, 18-34, 35-49, 50-64, 65+) from birth_date join on person_id | dev.tuva_input_layer.eligibility + patient | all | count | – |
| W-201 | Claims & Charges | 1 | Total Billed | counter | sum of max(charge_amount) per claim_id | dev.tuva_input_layer.medical_claim | all | currency $M | – |
| W-202 | Claims & Charges | 1 | Denial Rate | counter | distinct claim_id with paid_amount 0 or null / all distinct claim_id | dev.tuva_input_layer.medical_claim | all | percent | < 8% |
| W-203 | Claims & Charges | 2 | Monthly Billed vs Paid | line | sum of max(charge_amount) and max(paid_amount) per claim_id, by month | dev.tuva_input_layer.medical_claim | all | currency $M | – |

## Global Filters

| Filter | Field | Cardinality | Default | Exempt widgets (why) |
|---|---|---|---|---|
| Date Range | service/enrollment dates | continuous | last 12 months | W-101 (lifetime total by definition) |
| Payer Type | payer_type | 3 | All | none |
| State | state | ~50 | All | none |

## Open Questions

- none
