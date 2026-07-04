from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def test_main_revenue_attribution_files_exist():
    for name in [
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
    ]:
        assert (PROCESSED / f"{name}.csv").exists()


def test_required_columns_and_primary_ids_not_null():
    required = {
        "channels": ["channel_id", "channel_name"],
        "campaigns": ["campaign_id", "channel_id"],
        "leads": ["lead_id", "channel_id", "campaign_id"],
        "opportunities": ["opportunity_id", "lead_id", "channel_id", "pipeline_value"],
        "customers": ["customer_id", "lead_id", "opportunity_id", "acquisition_channel_id", "arr"],
        "revenue": ["revenue_id", "customer_id", "new_arr"],
    }
    for table, columns in required.items():
        df = pd.read_csv(PROCESSED / f"{table}.csv")
        for column in columns:
            assert column in df.columns
            if column.endswith("_id"):
                assert df[column].notna().all()
