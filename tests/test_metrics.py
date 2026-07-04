from __future__ import annotations

from src import metrics


def test_revenue_attribution_metrics_do_not_error_and_stay_in_range():
    tables = metrics.load_all()
    summary = metrics.executive_summary_metrics(tables)
    assert summary["total_arr"] > 0
    assert summary["total_spend"] > 0
    assert summary["total_customers"] > 0
    assert 0 <= summary["lead_to_customer_rate"] <= 1
    assert 0 <= summary["opportunity_win_rate"] <= 1
    assert summary["cac"] > 0
    assert summary["cac_payback_months"] > 0
    assert summary["ltv_cac"] > 0


def test_channel_summary_has_unit_economics_by_channel():
    channel = metrics.channel_summary(metrics.load_all())
    assert len(channel) >= 5
    for column in ["channel_name", "spend", "new_arr", "customers", "cac", "cac_payback_months"]:
        assert column in channel.columns
    assert channel["new_arr"].sum() > 0
