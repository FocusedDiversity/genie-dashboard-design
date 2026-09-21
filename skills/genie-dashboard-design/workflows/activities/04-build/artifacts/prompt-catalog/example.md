# Genie Prompt Catalog: Synaptiq Healthcare Analytics (excerpt)

**Inventory**: widget-inventory.md (v1.0) · **Test plan**: widget-test-plan.md (v1.0)

## Datasets

| Dataset | SQL | Used by |
|---|---|---|
| claims | `SELECT * FROM dev.tuva_input_layer.medical_claim` | Claims & Charges page |
| members | `SELECT * FROM dev.tuva_input_layer.eligibility` | Members page |

## Prompts by Page

### Page: Members

**W-101 — Total Members** · verified by T-101
```
Show the count of distinct person_id from dev.tuva_input_layer.eligibility
as a single number KPI titled "Total Members".
Do not filter by date: this is a lifetime total.
```

### Page: Claims & Charges

**W-201 — Total Billed** · verified by T-201
```
Show the sum of charge amounts from dev.tuva_input_layer.medical_claim
as a single number KPI titled "Total Billed".
charge_amount repeats on every claim line: take max(charge_amount) per
claim_id first, then sum those values.
Format as currency in millions with 1 decimal place.
```

**W-202 — Denial Rate** · verified by T-202
```
Show the percentage of denied claims from dev.tuva_input_layer.medical_claim
as a single number KPI titled "Denial Rate".
A claim is denied when paid_amount is null or 0.
Compute count of distinct denied claim_id divided by count of all distinct
claim_id. Format as a percentage with 1 decimal place.
```

## Fallback Views

```sql
CREATE OR REPLACE VIEW dev.tuva_input_layer.v_claim_amounts AS
SELECT claim_id, max(charge_amount) AS charge_amount, max(paid_amount) AS paid_amount
FROM dev.tuva_input_layer.medical_claim
GROUP BY claim_id;
-- If W-201/W-203 fail T-201 twice, point them here and drop the dedupe
-- sentence from their prompts.
```

## Traceability

| W-### | Prompt present | T-### | Notes |
|---|---|---|---|
| W-101 | yes | T-101 | |
| W-201 | yes | T-201 | fallback view ready |
| W-202 | yes | T-202 | |
