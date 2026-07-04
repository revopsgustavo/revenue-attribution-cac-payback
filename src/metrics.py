from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from src.utils import safe_divide
except ModuleNotFoundError:  # pragma: no cover
    from utils import safe_divide

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_table(name: str, base_path: Path = PROCESSED) -> pd.DataFrame:
    path = base_path / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def load_all(base_path: Path = PROCESSED) -> dict[str, pd.DataFrame]:
    names = [
        "channels",
        "campaigns",
        "marketing_spend",
        "leads",
        "opportunities",
        "customers",
        "revenue",
        "touchpoints",
        "attribution_models",
        "cohorts",
        "consultant_gap_log",
        "data_quality_report",
    ]
    return {name: load_table(name, base_path) for name in names}


def executive_summary_metrics(tables: dict[str, pd.DataFrame]) -> dict[str, float]:
    leads = tables.get("leads", pd.DataFrame())
    opportunities = tables.get("opportunities", pd.DataFrame())
    customers = tables.get("customers", pd.DataFrame())
    revenue = tables.get("revenue", pd.DataFrame())
    spend = tables.get("marketing_spend", pd.DataFrame())

    total_spend = float(spend.get("spend_amount", pd.Series(dtype=float)).sum())
    total_arr = float(revenue.get("new_arr", pd.Series(dtype=float)).sum())
    total_customers = int(customers.get("customer_id", pd.Series(dtype=object)).nunique())
    total_leads = int(leads.get("lead_id", pd.Series(dtype=object)).nunique())
    total_opportunities = int(opportunities.get("opportunity_id", pd.Series(dtype=object)).nunique())
    gross_margin = float(customers.get("gross_margin", pd.Series([0.75])).mean())
    retention = float(customers.get("retained_90d", pd.Series(dtype=float)).mean())

    return {
        "total_spend": total_spend,
        "total_arr": total_arr,
        "total_leads": total_leads,
        "total_opportunities": total_opportunities,
        "total_customers": total_customers,
        "lead_to_customer_rate": safe_divide(total_customers, total_leads),
        "opportunity_win_rate": safe_divide(total_customers, total_opportunities),
        "cac": safe_divide(total_spend, total_customers),
        "cac_payback_months": safe_divide(total_spend, (total_arr * gross_margin) / 12),
        "ltv_cac": safe_divide(total_arr * gross_margin * max(retention, 0), total_spend),
        "retention_90d": retention,
        "gross_margin": gross_margin,
    }


def channel_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    channels = tables["channels"][["channel_id", "channel_name", "channel_type"]].copy()
    leads = tables["leads"]
    opportunities = tables["opportunities"]
    customers = tables["customers"]
    revenue = tables["revenue"]
    spend = tables["marketing_spend"]

    out = channels.merge(
        spend.groupby("channel_id", as_index=False).agg(spend=("spend_amount", "sum")),
        on="channel_id",
        how="left",
    )
    out = out.merge(leads.groupby("channel_id", as_index=False).agg(leads=("lead_id", "nunique")), on="channel_id", how="left")
    out = out.merge(
        opportunities.groupby("channel_id", as_index=False).agg(
            opportunities=("opportunity_id", "nunique"),
            pipeline=("pipeline_value", "sum"),
            expected_arr=("expected_arr", "sum"),
        ),
        on="channel_id",
        how="left",
    )
    out = out.merge(
        customers.groupby("acquisition_channel_id", as_index=False).agg(
            customers=("customer_id", "nunique"),
            retained_90d=("retained_90d", "mean"),
            nrr_90d=("nrr_90d", "mean"),
        ).rename(columns={"acquisition_channel_id": "channel_id"}),
        on="channel_id",
        how="left",
    )
    out = out.merge(revenue.groupby("channel_id", as_index=False).agg(new_arr=("new_arr", "sum")), on="channel_id", how="left")
    out = out.fillna(0)
    out["lead_to_customer_rate"] = out.apply(lambda row: safe_divide(row["customers"], row["leads"]), axis=1)
    out["cac"] = out.apply(lambda row: safe_divide(row["spend"], row["customers"]), axis=1)
    out["cac_payback_months"] = out.apply(lambda row: safe_divide(row["spend"], (row["new_arr"] * 0.75) / 12), axis=1)
    out["arr_per_lead"] = out.apply(lambda row: safe_divide(row["new_arr"], row["leads"]), axis=1)
    return out.sort_values("new_arr", ascending=False)


def attribution_delta(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    attribution = tables.get("attribution_models", pd.DataFrame())
    channels = tables.get("channels", pd.DataFrame())[["channel_id", "channel_name"]]
    if attribution.empty:
        return pd.DataFrame()
    pivot = attribution.pivot_table(index="channel_id", columns="model_name", values="attributed_revenue", aggfunc="sum").reset_index()
    for column in ["first_touch", "last_touch", "multi_touch_equal"]:
        if column not in pivot:
            pivot[column] = 0.0
    pivot["last_vs_first_delta"] = pivot["last_touch"] - pivot["first_touch"]
    pivot["multi_touch_vs_first_delta"] = pivot["multi_touch_equal"] - pivot["first_touch"]
    return channels.merge(pivot, on="channel_id", how="right").sort_values("multi_touch_equal", ascending=False)
