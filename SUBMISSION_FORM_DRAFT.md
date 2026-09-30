# Vireo — 3-Minute Screen Recording Script

## Before recording

Open two windows side-by-side:

* **Terminal:** `~/Downloads/vireo_refund_tool_final`
* **VS Code/Text editor:** project folder

Start with the terminal visible.

---

## 0:00–0:20 — Introduce the project

### Show

Open `README.md` briefly.

### Say

> “Here is my Vireo refund-reconciliation tool. The goal was to reconcile the refund data and provide monthly refund reporting by reason and agent, while investigating the mismatch between Finance and the helpdesk.”

---

## 0:20–0:45 — Explain the data problem

### Show

Open the terminal and run:

```bash
python analyze.py --data data --out output
```

### Say

> “The data contains records from both the current and legacy helpdesk systems. I found 638 duplicate ticket IDs across the source systems. The policy states that legacy monetary values use a different unit, so the tool normalizes those values before reconciliation. All 638 duplicate pairs reconcile with zero normalized mismatches.”

---

## 0:45–1:10 — Show the main result

### Show

Run:

```bash
column -s, -t < output/quarterly_overview.csv
```

### Say

> “The reconciled dataset contains 11,600 unique tickets from 12,238 raw rows. There are 2,340 refund tickets totaling approximately 67.1 lakh rupees. The highest quarterly refund rate in the supplied data is 22.0% in Q3 2025.”

---

## 1:10–1:35 — Show the refund drivers

### Show

Run:

```bash
column -s, -t < output/refunds_by_month_reason.csv | head -20
```

### Say

> “The largest refund reason is GW-OTHER, with about 29.1 lakh rupees, representing approximately 43.3% of total refund value. RETURN-QC-OK and DUP-PAYMENT are the next major categories. This gives the business a focused area to investigate rather than simply looking at individual agent totals.”

---

## 1:35–2:00 — Show order validation

### Show

Run:

```bash
column -s, -t < output/validation_report.csv
```

### Say

> “The tool also validates refunds against the supplied order data. 2,330 of the 2,340 refund cases link to an order, giving a 99.6% match rate. Three linked cases have refund values above their recorded order value, so I flag them for human review instead of silently changing the data.”

---

## 2:00–2:25 — Show the policy control finding

### Show

Run:

```bash
python - <<'PY'
import pandas as pd

df = pd.read_csv("output/refund_cases.csv")
x = df[df["replacement_issued"].eq("Y")]

print("Refund + replacement cases:", len(x))
print("Refund value:", x["refund_inr_clean"].sum())
PY
```

### Say

> “I also added a control check for refunds and replacements. There are 166 cases where both outcomes were recorded, involving 5.74 lakh rupees of refund value. The policy says a customer should not receive both a refund and replacement for the same order, so these cases form a concrete review queue.”

---

## 2:25–2:45 — Show the business recommendation

### Show

Open:

```text
BOARD_MEMO.md
```

### Say

> “The recommended actions are to review GW-OTHER cases, investigate the 166 refund-plus-replacement cases, add a refund-replacement control check, and track the refund rate monthly. A reduction from the approximately 22% quarterly benchmark toward 15% represents a modeled gross opportunity of about 16.9 lakh rupees per quarter.”

---

## 2:45–3:00 — Show what was deliberately left out

### Show

Open:

```text
SUBMISSION_FORM_DRAFT.md
```

or `README.md`.

### Say

> “I deliberately kept the financial calculation deterministic instead of using an LLM for accounting decisions, and I did not build a large dashboard. The priority was reproducibility, traceability and validation. The 15% target and 16.9 lakh figure are a management scenario, not a forecast. The project can be reproduced from the README on a clean machine.”

---

# Recording checklist

Before starting:

* [ ] Terminal is in `vireo_refund_tool_final`
* [ ] Virtual environment is available
* [ ] `python analyze.py --data data --out output` works
* [ ] `BOARD_MEMO.md` is saved
* [ ] `SUBMISSION_FORM_DRAFT.md` is saved
* [ ] No personal information is visible on screen
* [ ] Recording is under 3 minutes
* [ ] Voice is clear

## Important

Do not spend time scrolling through the entire CSV files.

Show the **commands → outputs → business conclusion**. The reviewer needs to see that the tool works and that you understand why the findings matter.
