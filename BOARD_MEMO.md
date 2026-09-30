# Refund Review — Key Findings and Actions

**To:** Arjun Mehta
**Subject:** Refund reconciliation and actions to reduce refund leakage

## Executive summary

The refund data does not support the concern that quarterly refunds are “well over a crore.” After removing duplicate ticket records and normalizing the legacy/current helpdesk data, the analysis identifies **2,340 refund tickets totaling ₹67.1 lakh** across the supplied January 2025–June 2026 data.

The **highest quarterly refund rate was 22.0% in Q3 2025**. Using that quarter as the benchmark, reducing the refund rate from approximately **22% to 15%** would represent a modeled gross refund-value opportunity of approximately **₹16.9 lakh per quarter**, based on the observed refund volume and average refund amount. This is an opportunity estimate, not guaranteed savings.

## What is driving refunds

The largest reason code is **GW-OTHER**, representing **991 refund tickets and ₹29.1 lakh**, or approximately **43.3% of total refund value**. This concentration suggests that improving reason-code discipline and reviewing the underlying cases classified as GW-OTHER could provide a focused starting point for reducing avoidable refunds.

Other material categories are RETURN-QC-OK (**₹11.8 lakh**) and DUP-PAYMENT (**₹8.8 lakh**).

## Control issue identified

The analysis found **166 tickets where a refund and replacement were both recorded**, involving **₹5.74 lakh of refund value**. The supplied support policy states that customers should not receive both a refund and replacement for the same order and that such cases should be escalated.

This should be treated as a control-review queue rather than automatically assuming every case represents recoverable loss.

## Recommended actions

1. **Review GW-OTHER cases** and identify the most common underlying reasons currently being grouped into this code.
2. **Review the 166 refund-plus-replacement cases** and determine which represent genuine policy exceptions versus process/control failures.
3. **Add a refund/replacement control check** before completing either transaction.
4. **Track the refund rate monthly**, alongside refund value and reason, with a target of moving from the approximately 22% benchmark toward 15%.
5. **Reconcile legacy/current helpdesk records before financial reporting** so migration duplicates do not inflate the reported total.

The analysis provides a repeatable monthly view by reason and agent/team, while preserving the policy context that Returns Desk intentionally processes a large share of refunds and Tier 2 agents should not be compared directly with Tier 1 agents on refund volume.
