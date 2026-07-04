from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import metrics
from src.utils import format_currency_br, format_integer_br, format_percent_br, select_existing

DOCS = ROOT / "docs"

st.set_page_config(page_title="Revenue Attribution and CAC Payback", layout="wide")


@st.cache_data
def load_tables() -> dict[str, pd.DataFrame]:
    return metrics.load_all()


def markdown_doc(file_name: str) -> None:
    path = DOCS / file_name
    st.markdown(path.read_text(encoding="utf-8") if path.exists() else "Documento ainda nao gerado.")


def metric_card(column, label: str, value: str, help_text: str) -> None:
    column.metric(label, value, help=help_text)


def overview(tables: dict[str, pd.DataFrame]) -> None:
    st.title("Revenue Attribution and CAC Payback")
    st.caption("Case RevOps SaaS B2B: atribuicao de receita, eficiencia de canais e decisao de CAC Payback.")
    summary = metrics.executive_summary_metrics(tables)
    cols = st.columns(4)
    metric_card(cols[0], "ARR novo", format_currency_br(summary["total_arr"]), "Receita anual recorrente gerada pelos clientes adquiridos.")
    metric_card(cols[1], "CAC medio", format_currency_br(summary["cac"]), "Investimento de marketing dividido por novos clientes.")
    metric_card(cols[2], "Payback CAC", f"{summary['cac_payback_months']:.1f} meses", "Tempo estimado para recuperar o CAC com margem bruta.")
    metric_card(cols[3], "LTV/CAC", f"{summary['ltv_cac']:.2f}x", "Retorno unitario aproximado considerando margem e retencao.")

    st.subheader("Eficiencia por canal")
    channel = metrics.channel_summary(tables)
    st.dataframe(
        select_existing(
            channel,
            [
                "channel_name",
                "channel_type",
                "spend",
                "leads",
                "opportunities",
                "customers",
                "new_arr",
                "cac",
                "cac_payback_months",
                "retained_90d",
            ],
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.plotly_chart(px.bar(channel, x="channel_name", y="new_arr", color="channel_type", title="ARR novo por canal"), use_container_width=True)


def attribution(tables: dict[str, pd.DataFrame]) -> None:
    st.header("Attribution Models")
    delta = metrics.attribution_delta(tables)
    st.dataframe(delta, use_container_width=True, hide_index=True)
    if not delta.empty:
        melted = delta.melt(
            id_vars=["channel_name"],
            value_vars=["first_touch", "last_touch", "multi_touch_equal"],
            var_name="model",
            value_name="attributed_revenue",
        )
        st.plotly_chart(px.bar(melted, x="channel_name", y="attributed_revenue", color="model", barmode="group"), use_container_width=True)


def gaps(tables: dict[str, pd.DataFrame]) -> None:
    st.header("Consultant Gap Review")
    gap_log = tables.get("consultant_gap_log", pd.DataFrame())
    st.dataframe(gap_log, use_container_width=True, hide_index=True)
    markdown_doc("ai_consultant_analysis.md")


def data_quality(tables: dict[str, pd.DataFrame]) -> None:
    st.header("Data Quality")
    dq = tables.get("data_quality_report", pd.DataFrame())
    failures = int((dq["status"] == "fail").sum()) if "status" in dq else 0
    st.metric("Falhas de qualidade", format_integer_br(failures))
    st.dataframe(dq, use_container_width=True, hide_index=True)


def docs() -> None:
    st.header("Executive Narrative")
    doc = st.radio("Documento", ["executive_analysis.md", "metrics_dictionary.md", "final_handoff_report.md"], horizontal=True)
    markdown_doc(doc)


def main() -> None:
    tables = load_tables()
    page = st.sidebar.radio("Navegacao", ["Visao executiva", "Attribution", "Gaps", "Data quality", "Docs"])
    if page == "Visao executiva":
        overview(tables)
    elif page == "Attribution":
        attribution(tables)
    elif page == "Gaps":
        gaps(tables)
    elif page == "Data quality":
        data_quality(tables)
    else:
        docs()


if __name__ == "__main__":
    main()
