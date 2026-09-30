# 3-minute screen recording

**0:00–0:20 — Start**
“Here is the Vireo refund-reconciliation tool. The client asked for monthly refunds by reason and agent, but the email thread showed a major mismatch between Finance and the helpdesk.”

**0:20–0:55 — What changed**
“I found 638 duplicate ticket IDs across current and legacy systems. The policy says legacy Freshdesk stored money in a different native unit. Dividing legacy amounts by 100 makes all 638 duplicate pairs reconcile exactly.”

**0:55–1:30 — Run the tool**
“Running `python analyze.py --data data --out output` produces the monthly overview, reason report, agent report, case-level refund file and validation report. The reconciled total is ₹67.10 lakh across 2,340 refund tickets.”

**1:30–2:05 — Order validation**
“I added the supplied orders file. 2,330 of 2,340 refund cases link to an order using exact order ID or a dated customer-plus-SKU fallback. Three refunds exceed the recorded order value; I flag them for review rather than silently changing them.”

**2:05–2:35 — Business finding**
“GW-OTHER is the largest reason at ₹29.07 lakh. I also found 166 refund-plus-replacement cases worth ₹5.74 lakh of refund value. The policy prohibits both outcomes, so this is a concrete control queue.”

**2:35–3:00 — What I discarded**
“I deliberately did not use an LLM to calculate the financial total and did not build a large dashboard. Deterministic accounting and traceability mattered more. The 15% refund-rate target and ₹16.9 lakh quarterly figure are explicitly a management scenario, not a forecast.”
