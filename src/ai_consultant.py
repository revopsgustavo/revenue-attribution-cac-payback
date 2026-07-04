from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from src import metrics
    from src.utils import format_currency_br, format_percent_br
except ModuleNotFoundError:  # pragma: no cover
    import metrics
    from utils import format_currency_br, format_percent_br

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
OUTPUT = DOCS / "ai_consultant_analysis.md"


def _severity(gaps: pd.DataFrame, severity: str) -> str:
    subset = gaps[gaps["severity"].eq(severity)] if "severity" in gaps else pd.DataFrame()
    if subset.empty:
        return "- Nenhum gap nesta severidade.\n"
    return "\n".join(f"- **{row.area} | {row.metric}**: {row.evidence} Acao recomendada: {row.recommended_action}" for row in subset.itertuples()) + "\n"


def build_analysis(gaps: pd.DataFrame, summary: dict[str, float]) -> str:
    critical = int(gaps.get("severity", pd.Series(dtype=str)).eq("critical").sum())
    high = int(gaps.get("severity", pd.Series(dtype=str)).eq("high").sum())
    return f"""# AI Consultant Analysis

## Veredito executivo
Os dados sugerem que a empresa tem tracao de receita, mas ainda nao deve escalar budget sem governar CAC Payback por canal e sensibilidade dos modelos de atribuicao. O case mostra {format_currency_br(summary['total_arr'])} de ARR novo, CAC medio de {format_currency_br(summary['cac'])}, payback consolidado de {summary['cac_payback_months']:.1f} meses e LTV/CAC de {summary['ltv_cac']:.2f}x. Foram identificados {critical} gaps criticos e {high} gaps altos.

## Leitura da operacao
O problema central nao e apenas gerar demanda; e saber qual demanda cria receita com payback saudavel. Paid Social e parte de Paid Search trazem volume, mas pressionam eficiencia. Referral, Partner e Organic mostram melhor qualidade economica, enquanto Events precisa de governanca mais dura para justificar spend por ARR e nao por presenca ou pipeline bruto.

## Principais gaps criticos
{_severity(gaps, "critical")}
## Gaps altos
{_severity(gaps, "high")}
## Gaps medios
{_severity(gaps, "medium")}

## Hipoteses que precisam de validacao
- O excesso de volume pago pode estar inflando MQL sem a mesma qualidade de conversao para cliente.
- A decisao de budget pode mudar conforme o modelo de atribuicao escolhido, especialmente entre first-touch e last-touch.
- Canais com melhor retencao e margem devem receber peso maior que canais com apenas baixo custo por lead.
- Eventos podem estar submedidos se influenciarem deals enterprise em janelas mais longas, mas isso precisa ser comprovado.

## Evidencias ausentes
- Regras oficiais de janela de atribuicao e deduplicacao de touchpoints.
- Budget planejado versus gasto real por campanha.
- Margem e churn por segmento, nao apenas por canal.
- Influencia offline de eventos e parceiros em oportunidades multi-touch.
- Politica executiva de payback maximo por fase de crescimento.

## Recomendacoes priorizadas
1. Adotar multi-touch equal como leitura operacional e manter first/last-touch como analise de sensibilidade.
2. Cortar ou testar novamente campanhas pagas com payback acima de 18 meses.
3. Rebalancear budget incremental para Referral, Partner e Organic enquanto CAC Payback consolidado estiver acima de 12 meses.
4. Adicionar retencao 90d e NRR por coorte ao ritual mensal de marketing performance.
5. Separar dashboards de volume, pipeline, ARR, payback e LTV/CAC para evitar decisao por metrica isolada.

## Perguntas para a reuniao executiva
- Qual payback maximo a empresa aceita para aquisicao neste semestre?
- Quais canais devem ser avaliados por ARR direto e quais por influencia multi-touch?
- Que budget pode ser realocado sem interromper experimentos estrategicos?
- Eventos estao gerando receita direta, influencia qualificada ou apenas pipeline caro?
- A meta de crescimento privilegia eficiencia, market share ou aprendizado de canal?
"""


def main() -> None:
    tables = metrics.load_all()
    gaps = pd.read_csv(PROCESSED / "consultant_gap_log.csv")
    DOCS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_analysis(gaps, metrics.executive_summary_metrics(tables)), encoding="utf-8")
    print(f"AI consultant analysis generated at {OUTPUT}")


if __name__ == "__main__":
    main()
