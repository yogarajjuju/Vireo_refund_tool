# Submission Form — Final Draft

## What did you build, and what business outcome does it move?

A small reproducible Python/pandas refund-reconciliation CLI. It deduplicates migration re-imports, converts legacy Freshdesk money into rupees, produces monthly refund totals by reason and resolving agent, validates the migration conversion, and adds order-level/control checks.

Primary business scenario: reduce refund incidence from the **highest quarterly rate in the supplied data, 22.0% in Q3 2025, to 15%**. At 650 tickets/week and the observed average refund value, this models approximately **₹16.9 lakh of gross refund value avoided per quarter**, assuming average refund value stays constant.

A separate control opportunity is **166 refund+replacement cases worth ₹5.74 lakh of refund value and ₹8.71 lakh of combined cost**.

## What does one run cost, and what would a month cost?

₹0 in paid API/model calls. The runtime is local Python/pandas.

650 tickets/week × 4.33 weeks/month ≈ 2,815 tickets/month. Paid model/API calls = 0, so API/model spend = **₹0/month**.

## How do you know it works?

Sample: **12,238 raw ticket rows → 11,600 unique tickets**. There are **638 duplicate ticket IDs**, all cross-source migration pairs. After legacy `/100`, 638/638 duplicate pairs reconcile with **zero normalized mismatches**.

**2,340 refund tickets** are retained in a traceable case-level output. **2,330/2,340 (99.6%)** link to an order using exact order ID or nearest-prior customer+SKU fallback.

Three linked cases have refund value above recorded order value. They are explicitly flagged for human review rather than treated as tool errors.

## Did you change, narrow, or push back on the client's ask?

Yes. I reframed “who is giving away money” into “where is refund value coming from and where are the policy/control exceptions?” Returns Desk is intentionally responsible for most refunds, so raw agent totals are not treated as misconduct evidence.

I also resolved the Finance/helpdesk disagreement as a data-reconciliation problem before reporting financial totals.

## What is wrong with what you are handing us?

* Three refund cases exceed recorded order value and require human review.
* Ten refund cases cannot be linked to an order from the supplied order data using the defined matching rules.
* The 15% target is a scenario, not a forecast.
* Free-text interpretation is not automated into accounting decisions.
* Agent totals can still be misread without team/volume context.

## What did you deliberately leave out, and why?

I left out an LLM classifier for the financial total and a large dashboard. The requested financial report is deterministic; adding an LLM would add cost and ambiguity without improving reconciliation. I prioritized traceability and validation.

## Anything you built or found that nobody asked for?

* Refund + replacement control check.
* Order-level reconciliation and refund-above-order-value flags.
* Migration duplicate audit explaining the Finance/helpdesk discrepancy.

## What did you use AI for?

I used ChatGPT (GPT-5.6 Luna) as a coding/reasoning assistant to inspect the pack, design reconciliation logic, challenge assumptions and structure the report.

## Three-minute recording

https://drive.google.com/file/d/1AOSu5RvBm5ebhYYzOwQB5J6N5k8L1tga/view?usp=sharing

## Your Public Google Drive Link

https://drive.google.com/file/d/1AOSu5RvBm5ebhYYzOwQB5J6N5k8L1tga/view?usp=sharing

## Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. Run `python analyze.py --data data --out output`.
2. Never sum raw refund amounts across both source systems; deduplicate and normalize legacy money first.
3. Board number: **₹67.10 lakh across the 18-month reconciled dataset**.

## Honest hours spent

5

## Github Repo Link

https://github.com/yogarajjuju/Vireo_refund_tool
