#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def load_pack(d):
    d=Path(d)
    return pd.read_csv(d/"tickets.csv"), pd.read_csv(d/"agents.csv"), pd.read_csv(d/"orders.csv"), pd.read_csv(d/"products.csv")

def normalize(t):
    t=t.copy()
    t["_rank"]=t.source_system.map({"helpdesk":0,"legacy_fd":1}).fillna(9)
    t=t.sort_values(["ticket_id","_rank"]).drop_duplicates("ticket_id").copy()
    t["refund_inr_clean"]=pd.to_numeric(t.refund_amount_inr,errors="coerce")
    t.loc[t.source_system.eq("legacy_fd"),"refund_inr_clean"]/=100
    t["created_at"]=pd.to_datetime(t.created_at,errors="coerce")
    t["month"]=t.created_at.dt.to_period("M").astype(str)
    t["quarter"]=t.created_at.dt.to_period("Q").astype(str)
    return t

def audit(raw):
    dup=raw[raw.ticket_id.duplicated(False)]
    ids=int(dup.ticket_id.nunique())
    cross=int(dup.groupby("ticket_id").source_system.nunique().eq(2).sum())
    bad=0
    for _,g in dup.groupby("ticket_id"):
        vals=[]
        for _,r in g.iterrows():
            if pd.notna(r.refund_amount_inr):
                vals.append(float(r.refund_amount_inr)/100 if r.source_system=="legacy_fd" else float(r.refund_amount_inr))
        if vals and max(vals)-min(vals)>1e-9: bad+=1
    return ids,cross,bad

def attach_orders(r,o):
    r=r.copy(); o=o.copy(); o.order_date=pd.to_datetime(o.order_date,errors="coerce")
    r["matched_order_id"]=pd.NA; r["matched_order_value_inr"]=pd.NA; r["order_match_method"]="unmatched"
    exact=o.drop_duplicates("order_id").set_index("order_id")
    m=r.order_id.notna() & r.order_id.isin(exact.index)
    r.loc[m,"matched_order_id"]=r.loc[m,"order_id"]
    r.loc[m,"matched_order_value_inr"]=r.loc[m,"order_id"].map(exact.order_value_inr)
    r.loc[m,"order_match_method"]="order_id"
    fb=r.loc[~m,["ticket_id","customer_id","product_sku","created_at"]].merge(o,left_on=["customer_id","product_sku"],right_on=["customer_id","sku"],how="left")
    fb["days_gap"]=(fb.created_at.dt.normalize()-fb.order_date).dt.days
    fb=fb[fb.days_gap>=0].sort_values(["ticket_id","days_gap"]).drop_duplicates("ticket_id")
    if len(fb):
        lk=fb.set_index("ticket_id")
        mm=r.ticket_id.isin(lk.index)
        r.loc[mm,"matched_order_id"]=r.loc[mm,"ticket_id"].map(lk.order_id)
        r.loc[mm,"matched_order_value_inr"]=r.loc[mm,"ticket_id"].map(lk.order_value_inr)
        r.loc[mm,"order_match_method"]="customer_sku_nearest_prior"
    r["refund_gt_matched_order_value"]=r.matched_order_value_inr.notna() & (r.refund_inr_clean>pd.to_numeric(r.matched_order_value_inr,errors="coerce")+0.01)
    return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data",default="data"); ap.add_argument("--out",default="output")
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    raw,agents,orders,products=load_pack(a.data); t=normalize(raw); r=t[t.refund_inr_clean.notna()].copy()
    r["dual_refund_replacement"]=r.replacement_issued.eq("Y"); r=attach_orders(r,orders)
    r=r.merge(products[["sku","unit_cost_inr"]],left_on="product_sku",right_on="sku",how="left")
    r["replacement_cost_inr"]=r.unit_cost_inr+340; r["dual_total_cost_inr"]=r.refund_inr_clean+r.replacement_cost_inr
    monthly=r.groupby(["month","refund_reason_code"],dropna=False).refund_inr_clean.agg(refund_tickets="size",refund_inr="sum").reset_index()
    agent=r.groupby(["month","agent_id","refund_reason_code"],dropna=False).refund_inr_clean.agg(refund_tickets="size",refund_inr="sum").reset_index().merge(agents[["agent_id","name","team","tier"]].drop_duplicates("agent_id"),on="agent_id",how="left")
    overview=t.groupby("month").agg(tickets=("ticket_id","size"),refund_tickets=("refund_inr_clean",lambda s:s.notna().sum()),refund_inr=("refund_inr_clean","sum")).reset_index(); overview["refund_rate"]=overview.refund_tickets/overview.tickets
    q=t.groupby("quarter").agg(tickets=("ticket_id","size"),refund_tickets=("refund_inr_clean",lambda s:s.notna().sum()),refund_inr=("refund_inr_clean","sum")).reset_index(); q["refund_rate"]=q.refund_tickets/q.tickets
    ids,cross,bad=audit(raw); linked=r.matched_order_id.notna().sum(); dual=r.dual_refund_replacement.sum(); above=r.refund_gt_matched_order_value.sum()
    pd.DataFrame([
      ["raw_export_rows",len(raw),"Rows received"],["unique_ticket_ids",len(t),"Deduplicated ticket IDs"],["duplicate_ticket_ids",ids,"Duplicate IDs"],["cross_source_duplicate_ids",cross,"Duplicates in both source systems"],["normalized_duplicate_mismatches",bad,"Should be zero after legacy /100"],["refund_tickets",len(r),"Unique refund tickets"],["refund_total_inr",r.refund_inr_clean.sum(),"Reconciled refund value"],["order_linked_refund_tickets",linked,"Exact order ID or nearest prior customer+SKU"],["order_link_rate",linked/len(r),"Linked / refund tickets"],["refunds_above_matched_order_value",int(above),"Review flags, not assumed errors"],["dual_refund_replacement_tickets",int(dual),"Policy-risk cases"],["dual_refund_value_inr",r.loc[r.dual_refund_replacement,"refund_inr_clean"].sum(),"Refund value in policy-risk cases"],["dual_combined_cost_inr",r.loc[r.dual_refund_replacement,"dual_total_cost_inr"].sum(),"Refund + replacement planning cost"]],columns=["metric","value","meaning"]).to_csv(out/"validation_report.csv",index=False)
    monthly.to_csv(out/"refunds_by_month_reason.csv",index=False); agent.to_csv(out/"refunds_by_month_agent_reason.csv",index=False); overview.to_csv(out/"monthly_overview.csv",index=False); q.to_csv(out/"quarterly_overview.csv",index=False)
    r[["ticket_id","created_at","agent_id","refund_inr_clean","refund_reason_code","replacement_issued","dual_refund_replacement","matched_order_id","order_match_method","matched_order_value_inr","refund_gt_matched_order_value","customer_message","agent_notes","source_system"]].to_csv(out/"refund_cases.csv",index=False)
    q3=q[q.quarter.eq("2025Q3")].iloc[0]; avg=r.refund_inr_clean.mean(); savings=(q3.refund_rate-.15)*650*13*avg
    print(f"Raw rows: {len(raw):,}; unique tickets: {len(t):,}; duplicate IDs: {ids:,}; normalized mismatches: {bad}")
    print(f"Refund total: Rs {r.refund_inr_clean.sum():,.0f}; refund tickets: {len(r):,}")
    print(f"Order-linked: {linked:,}/{len(r):,} ({linked/len(r):.1%}); above order value: {int(above)}")
    print(f"Refund+replacement: {int(dual)}; refund value Rs {r.loc[r.dual_refund_replacement,'refund_inr_clean'].sum():,.0f}; combined cost Rs {r.loc[r.dual_refund_replacement,'dual_total_cost_inr'].sum():,.0f}")
    print(f"Q3 2025 rate: {q3.refund_rate:.1%}; modeled 15% target savings: Rs {savings:,.0f}/quarter")
if __name__=="__main__": main()
