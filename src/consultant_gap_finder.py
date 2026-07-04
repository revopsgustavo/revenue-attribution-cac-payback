from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = PROCESSED / "consultant_gap_log.csv"


def _gap(gap_id: str, area: str, metric: str, actual: object, expected: object, severity: str, evidence: str, action: str, owner: str, follow_up: str) -> dict[str, object]:
    return {
        "gap_id": gap_id,
        "area": area,
        "metric": metric,
        "actual_value": actual,
        "expected_value": expected,
        "severity": severity,
        "evidence": evidence,
        "probable_cause": "Hipotese provavel: a combinacao de mix de canal, qualidade de demanda, regras de atribuicao e disciplina de budget precisa ser validada antes de confirmar causa raiz.",
        "missing_evidence": "Historico real de budget, criterios de MQL/SQL, origem de contratos, pesos de atribuicao, margem por segmento e retencao por coorte.",
        "validation_questions": "O desvio observado vem de qualidade de demanda, tracking incompleto, janela de atribuicao, ciclo de vendas, mix de segmento ou governanca de investimento?",
        "recommended_action": action,
        "owner": owner,
        "urgency": "immediate" if severity == "critical" else "this_week" if severity == "high" else "this_month",
        "expected_impact": "Melhorar alocacao de budget, confiabilidade de atribuicao, CAC Payback, LTV/CAC e decisao executiva de crescimento.",
        "follow_up_metric": follow_up,
        "status": "open",
    }


def find_gaps() -> pd.DataFrame:
    channels = pd.read_csv(PROCESSED / "channels.csv")
    leads = pd.read_csv(PROCESSED / "leads.csv")
    opportunities = pd.read_csv(PROCESSED / "opportunities.csv")
    customers = pd.read_csv(PROCESSED / "customers.csv")
    revenue = pd.read_csv(PROCESSED / "revenue.csv")
    spend = pd.read_csv(PROCESSED / "marketing_spend.csv")
    attribution = pd.read_csv(PROCESSED / "attribution_models.csv")

    channel = channels[["channel_id", "channel_name", "channel_type"]].merge(
        spend.groupby("channel_id", as_index=False).agg(spend=("spend_amount", "sum")),
        on="channel_id",
        how="left",
    )
    channel = channel.merge(leads.groupby("channel_id", as_index=False).agg(leads=("lead_id", "nunique"), icp_rate=("is_icp", "mean")), on="channel_id", how="left")
    channel = channel.merge(opportunities.groupby("channel_id", as_index=False).agg(opportunities=("opportunity_id", "nunique")), on="channel_id", how="left")
    channel = channel.merge(
        customers.groupby("acquisition_channel_id", as_index=False).agg(customers=("customer_id", "nunique"), retention_90d=("retained_90d", "mean")).rename(columns={"acquisition_channel_id": "channel_id"}),
        on="channel_id",
        how="left",
    )
    channel = channel.merge(revenue.groupby("channel_id", as_index=False).agg(new_arr=("new_arr", "sum")), on="channel_id", how="left").fillna(0)
    channel["cac"] = channel["spend"] / channel["customers"].replace(0, pd.NA)
    channel["payback"] = channel["spend"] / ((channel["new_arr"] * 0.75) / 12).replace(0, pd.NA)
    channel["lead_to_customer"] = channel["customers"] / channel["leads"].replace(0, pd.NA)

    gaps: list[dict[str, object]] = []
    paid_social = channel.loc[channel["channel_name"].eq("Paid Social")].iloc[0]
    events = channel.loc[channel["channel_name"].eq("Events")].iloc[0]
    referral = channel.loc[channel["channel_name"].eq("Referral")].iloc[0]
    paid_search = channel.loc[channel["channel_name"].eq("Paid Search")].iloc[0]

    if paid_social["payback"] > 18:
        gaps.append(_gap("gap_paid_social_payback", "channel_efficiency", "cac_payback_months", round(float(paid_social["payback"]), 1), "<= 12", "critical", "Paid Social concentra volume de leads, mas apresenta payback acima do limite executivo.", "Reduzir budget de lead ads amplos e manter apenas retargeting com prova de produto.", "Marketing Ops", "cac_payback_months"))
    if events["spend"] > referral["spend"] * 4 and events["lead_to_customer"] < referral["lead_to_customer"]:
        gaps.append(_gap("gap_events_budget_efficiency", "budget_allocation", "event_efficiency_vs_referral", round(float(events["lead_to_customer"]), 3), f">= {referral['lead_to_customer']:.3f}", "high", "Events recebe investimento materialmente maior, mas converte menos que Referral.", "Migrar parte do budget de eventos para referral e partner motions com accountability por ARR.", "Head of Marketing", "arr_per_spend"))
    if paid_search["cac"] > referral["cac"] * 2:
        gaps.append(_gap("gap_paid_search_cac", "channel_efficiency", "cac", round(float(paid_search["cac"]), 2), f"<= {referral['cac'] * 1.5:.2f}", "high", "Paid Search gera captura de demanda, mas CAC fica muito acima de canais orgânicos e referral.", "Separar campanhas core intent de broad match e reportar CAC por subcampanha.", "Demand Generation", "cac_by_campaign"))

    attr = attribution.pivot_table(index="channel_id", columns="model_name", values="attributed_revenue", aggfunc="sum").reset_index()
    attr["delta_last_first"] = attr.get("last_touch", 0) - attr.get("first_touch", 0)
    shifted = attr.merge(channels[["channel_id", "channel_name"]], on="channel_id")
    shifted = shifted.loc[shifted["delta_last_first"].abs().gt(100000)]
    if not shifted.empty:
        gaps.append(_gap("gap_attribution_model_sensitivity", "attribution_governance", "last_vs_first_touch_delta", round(float(shifted["delta_last_first"].abs().max()), 2), "<= 100000", "critical", "A leitura de receita por canal muda de forma relevante entre first-touch e last-touch.", "Criar modelo multi-touch oficial e governar decisao de budget por mais de um modelo.", "RevOps Analytics", "model_variance"))

    low_retention = channel.loc[channel["retention_90d"].lt(0.82)]
    if not low_retention.empty:
        gaps.append(_gap("gap_low_retention_channels", "cohort_quality", "retention_90d", round(float(low_retention["retention_90d"].min()), 3), ">= 0.82", "high", "Alguns canais trazem clientes com retencao de 90 dias abaixo do minimo esperado.", "Adicionar retencao e NRR por coorte na decisao de investimento de aquisicao.", "Revenue Operations", "retention_90d_by_channel"))

    if int(leads["is_icp"].mean() * 100) < 85:
        gaps.append(_gap("gap_icp_quality", "lead_quality", "icp_rate", round(float(leads["is_icp"].mean()), 3), ">= 0.85", "medium", "A base inclui volume relevante de leads fora de ICP.", "Revisar criterios de segmentacao e score minimo antes de MQL.", "Marketing Ops", "icp_rate"))

    overall_payback = float(channel["spend"].sum() / ((channel["new_arr"].sum() * 0.75) / 12))
    if overall_payback > 12:
        gaps.append(_gap("gap_company_payback", "unit_economics", "company_cac_payback_months", round(overall_payback, 1), "<= 12", "critical", "O payback consolidado esta acima do limite de crescimento eficiente.", "Rebalancear investimento para canais com payback inferior a 12 meses antes de escalar spend.", "CRO", "company_cac_payback_months"))

    return pd.DataFrame(gaps)


def main() -> None:
    gaps = find_gaps()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    gaps.to_csv(OUTPUT, index=False)
    print(f"Consultant gap log generated at {OUTPUT} with {len(gaps)} gaps")


if __name__ == "__main__":
    main()
