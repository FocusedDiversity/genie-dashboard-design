# Widget Test Plan: Synaptiq Healthcare Analytics

**Inventory**: widget-inventory.md (v1.0) · **Decisions**: design-decisions.md (v1.0)
**Baselines executed**: 2026-07-27 on wh-analytics-serverless

## Strategy

- Counts: exact match. Rates: within ±0.1 percentage points (rounding drift).
- Synthetic data is static, so baselines are stable; on live data, re-run
  baselines the same day as Deploy verification.

## Baseline Checks

### T-101 — verifies W-101 Total Members

**Rule**: exact match

```sql
SELECT count(DISTINCT person_id) AS total_members
FROM dev.tuva_input_layer.eligibility;
```

**Baseline result** (2026-07-27): 2,143,858
**Covers design rule**: Member = person

### T-201 — verifies W-201 Total Billed

**Rule**: exact match

```sql
SELECT sum(max_charge) AS total_billed
FROM (
  SELECT claim_id, max(charge_amount) AS max_charge
  FROM dev.tuva_input_layer.medical_claim
  GROUP BY claim_id
);
```

**Baseline result** (2026-07-27): $412,384,022
**Covers design rule**: Charge-once-per-claim

### T-202 — verifies W-202 Denial Rate

**Rule**: within ±0.1pp

```sql
SELECT round(
  count(DISTINCT CASE WHEN paid_amount IS NULL OR paid_amount = 0
                      THEN claim_id END) * 100.0
  / count(DISTINCT claim_id), 1) AS denial_rate_pct
FROM dev.tuva_input_layer.medical_claim;
```

**Baseline result** (2026-07-27): 6.8%
**Covers design rule**: Denied means unpaid

## Dashboard-Level Checks

### T-901 — Filter cascade
Set Payer Type = medicaid: W-102–W-104, W-201–W-203 narrow; W-101 unchanged
(date-exempt only — payer filter DOES apply; verify it narrows).

### T-902 — Counter/table agreement
W-201 equals the sum of the monthly billed series in W-203 over the same window.

### T-903 — Empty-slice behavior
State = "AK" AND Payer = medicare on synthetic data returns empty widgets, no errors.

## Out of Scope

- Pixel layout and chart styling: authority is the approved mockup.
- Query performance: synthetic volume is unrepresentative; profile on production data.
