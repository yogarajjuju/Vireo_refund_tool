# Vireo Audio — Support Refund Reconciliation Tool

Reproducible Python/pandas CLI for Task 1.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analyze.py --data data --out output
```

## Logic
- Deduplicates `ticket_id`, preferring current `helpdesk` over `legacy_fd`.
- Converts legacy Freshdesk monetary values by `/100`; duplicate pairs validate this conversion.
- Reports monthly refunds by reason and resolving agent.
- Links refund cases to `orders.csv` using exact `order_id`, then nearest prior order for the same customer + SKU when `order_id` is absent.
- Flags refunds above matched order value for human review rather than changing them.
- Calculates refund+replacement planning cost using product unit cost + ₹340 shipping, per policy.
- Uses no LLM/API call for the financial calculation.

## Outputs
`monthly_overview.csv`, `quarterly_overview.csv`, `refunds_by_month_reason.csv`, `refunds_by_month_agent_reason.csv`, `refund_cases.csv`, `validation_report.csv`.

## Current checks
- 12,238 raw rows → 11,600 unique tickets
- 638 duplicate IDs; 638/638 normalized duplicate pairs reconcile
- 2,340 refund tickets; ₹67.10 lakh reconciled refund value
- 2,330/2,340 refund tickets (99.6%) linked to an order
- 3 linked cases have refund value above recorded order value; flagged for review
- 166 refund+replacement cases; ₹5.74 lakh refund value; ₹8.71 lakh combined refund + replacement planning cost

## Scope decisions
Raw agent totals are not treated as proof of poor performance because Returns Desk intentionally processes most refunds. The 15% refund-incidence target is a management scenario, not a forecast. Free text is retained for case review but does not determine the board total.
