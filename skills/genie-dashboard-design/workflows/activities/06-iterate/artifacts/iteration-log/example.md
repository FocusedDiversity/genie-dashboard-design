# Iteration Log: Synaptiq Healthcare Analytics (excerpt)

**Deployed**: 2026-07-27 · **Owner**: G. Fischer

## Change Log

| Date | Change | Widgets | Driver |
|---|---|---|---|
| 2026-07-27 | v1.0 released | all | initial cycle |
| 2026-08-04 | Denial Rate subtitle now states the unpaid-only definition | W-202 | analyst confusion (2026-08-03 feedback) |

## Usage & Feedback

| Date | Source | Feedback | Disposition |
|---|---|---|---|
| 2026-08-03 | #analytics-help | "Does denial include partial payments?" | fixed — subtitle clarifies unpaid-only |
| 2026-08-10 | ops weekly | "Want denial rate split by payer type" | parking lot |

## Drift Checks

| Date | Checks re-run | Result | Action |
|---|---|---|---|
| 2026-08-11 | T-101, T-201, T-202 | all PASS | none |

## Parking Lot

- W-202 variant: denial rate grouped by payer_type (bar) — requested by ops
- New widget: claims aging distribution — needs Frame-level definition of "aging"

## Next Cycle

Scoped: both parking-lot items enter Frame week of 2026-09-01.
