from __future__ import annotations

from pathlib import Path

try:
    from src import metrics
    from src.utils import format_currency_br, format_percent_br
except ModuleNotFoundError:  # pragma: no cover
    import metrics
    from utils import format_currency_br, format_percent_br

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    tables = metrics.load_all()
    summary = metrics.executive_summary_metrics(tables)
    memo = f"""# Executive Memo

## Problem
Os dados sugerem que decisões de budget não devem depender apenas de volume de leads, CPL ou pipeline bruto.

## Evidence
- ARR novo: {format_currency_br(summary['total_arr'])}.
- Investimento de marketing: {format_currency_br(summary['total_spend'])}.
- CAC médio: {format_currency_br(summary['cac'])}.
- CAC Payback: {summary['cac_payback_months']:.1f} meses.
- LTV/CAC: {summary['ltv_cac']:.2f}x.
- Retenção 90d: {format_percent_br(summary['retention_90d'])}.

## Business Risk
Há indícios de que atribuição pode ser lida como verdade absoluta. Isso pode gerar realocação de budget sem considerar payback, retenção, margem e sensibilidade do modelo.

## Recommended Decision
Governar budget com múltiplos modelos de atribuição, CAC Payback, retenção e eficiência econômica por canal.

## Owner
Head de Marketing Ops, RevOps, Demand Gen, Finance/FP&A e CRO.

## Follow-up Metric
CAC Payback, LTV/CAC, ARR por canal, retention_by_channel e attribution_delta.

## What Is Missing
Janelas reais de influência, custos completos, vendas assistidas, margem por produto e validação de Finance/FP&A.

## Final Recommendation
A evidência disponível aponta para tratar atribuição como leitura direcional para governança de budget, não como causalidade absoluta.
"""
    executive = f"""# Análise Executiva

## Veredito executivo
Os dados sugerem tração de receita, mas a decisão de escala precisa considerar CAC Payback, retenção e sensibilidade de atribuição por canal.

## Resumo de métricas
- ARR novo: {format_currency_br(summary['total_arr'])}.
- Investimento de marketing: {format_currency_br(summary['total_spend'])}.
- Clientes: {summary['total_customers']}.
- CAC médio: {format_currency_br(summary['cac'])}.
- CAC Payback: {summary['cac_payback_months']:.1f} meses.
- LTV/CAC: {summary['ltv_cac']:.2f}x.

## Recomendação
Atribuição deve apoiar decisão executiva como hipótese de alocação, com validação por payback, retenção, margem e contexto comercial.
"""
    dictionary = """# Metrics Dictionary

| Métrica | Definição | Decisão suportada | Limitação |
|---|---|---|---|
| CAC | Investimento / novos clientes | Avaliar eficiência de aquisição | Não inclui todos os custos reais |
| CAC Payback | Meses para recuperar CAC com margem | Decidir escala ou ajuste de budget | Depende de margem sintética |
| LTV/CAC | Receita ajustada por margem e retenção / spend | Comparar eficiência econômica | Simplificação de LTV |
| Attribution delta | Diferença entre modelos de atribuição | Governar sensibilidade de canal | Não prova causalidade |
| Retention 90d | Clientes retidos em 90 dias | Qualificar qualidade da aquisição | Janela curta e sintética |
"""
    (DOCS / "executive_memo.md").write_text(memo, encoding="utf-8")
    (DOCS / "executive_analysis.md").write_text(executive, encoding="utf-8")
    (DOCS / "metrics_dictionary.md").write_text(dictionary, encoding="utf-8")
    print("Revenue attribution reports generated.")


if __name__ == "__main__":
    main()
