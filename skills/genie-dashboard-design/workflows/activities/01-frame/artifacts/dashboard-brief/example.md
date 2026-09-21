# Dashboard Brief: Synaptiq Healthcare Analytics

**Stakeholder**: Analytics Lead
**Date**: 2026-07-27
**Status**: Approved

## Summary

Three-page dashboard giving analysts a single view of members, claims, and
clinical conditions from the Tuva Input Layer synthetic dataset. Replaces ad-hoc
notebook queries with governed, filterable views; enables month-over-month
utilization review without SQL.

## Problem & Audience

- **Problem**: Enrollment and claims questions each require a hand-written query;
  answers differ by author because aggregation rules are not standardized.
- **Audience**: Data analysts daily; operations leads weekly.
- **Primary workflow**: Glance at member/claims KPIs, then drill into payer mix,
  monthly trend, and top diagnoses.

## Data Sources

| Table (full path) | Grain | Role | Known quality issues |
|---|---|---|---|
| dev.tuva_input_layer.eligibility | one row per member-enrollment span | facts | open-ended spans use 9999-12-31 |
| dev.tuva_input_layer.patient | one row per person_id | dimension | none known |
| dev.tuva_input_layer.medical_claim | one row per claim line | facts | charge repeats per line — max per claim_id |

- **Join keys**: person_id (eligibility ↔ patient; claims ↔ patient)
- **Refresh cadence**: static synthetic data

## KPIs & Metrics

| Metric | Definition | Aggregation | Unit | Target |
|---|---|---|---|---|
| Total Members | all persons ever enrolled | distinct person_id | count | n/a |
| Active Members | enrollment_end_date >= today or 9999-12-31 | distinct person_id | count | n/a |
| Total Billed | charge per claim counted once | sum of max(charge_amount) per claim_id | currency | n/a |
| Denial Rate | claims with paid_amount 0 or null / all claims | distinct claim_id ratio | percent | < 8% |

## Filters & Drill-downs

| Filter | Field | Cardinality | Default | Applies to |
|---|---|---|---|---|
| Date Range | claim/enrollment dates | continuous | last 12 months | all pages |
| Payer Type | payer_type | 3 | All | all pages |
| State | state | ~50 | All | all pages |

- **Drill-down paths**: claims KPIs → monthly billed-vs-paid trend → top diagnoses table

## Constraints & Assumptions

- Charge amounts repeat on every claim line; all charge aggregations take max per claim_id first.
- Synthetic data — no PHI constraints; production swap requires a compliance pass.

## Success Criteria

- Analysts answer payer-mix and denial-rate questions without writing SQL.
- Billed/paid totals match the finance reconciliation notebook within 1%.
