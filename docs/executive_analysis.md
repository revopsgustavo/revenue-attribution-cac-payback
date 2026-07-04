# Analise Executiva

## Contexto
Este projeto avalia atribuicao de receita e CAC Payback em uma operacao SaaS B2B com 3137 leads, 492 oportunidades e 137 novos clientes. A analise conecta canais, campanhas, oportunidades, clientes, receita, spend e modelos de atribuicao.

## Leitura Executiva
A empresa gerou R$ 6.629.000,00 de ARR novo com R$ 1.509.000,00 de investimento. O CAC medio ficou em R$ 11.014,60, com payback consolidado de 3.5 meses e LTV/CAC estimado em 3.44x.

## O Que Isso Significa
O crescimento existe, mas a qualidade da escala varia por canal. Volume de leads nao e suficiente para justificar budget; a decisao executiva deve combinar ARR, clientes, payback, retencao e sensibilidade de atribuicao.

## Canais Prioritarios
| channel_name | spend | customers | new_arr | cac | cac_payback_months | retained_90d |
| --- | --- | --- | --- | --- | --- | --- |
| Referral | 48000.00 | 43 | 2045280.00 | 1116.28 | 0.40 | 1.00 |
| Partner | 138000.00 | 35 | 1812200.00 | 3942.86 | 1.20 | 1.00 |
| Organic | 87000.00 | 26 | 997620.00 | 3346.15 | 1.40 | 1.00 |
| Events | 372000.00 | 11 | 965650.00 | 33818.18 | 6.20 | 1.00 |
| Paid Search | 492000.00 | 13 | 539700.00 | 37846.15 | 14.60 | 1.00 |
| Webinar | 108000.00 | 7 | 226050.00 | 15428.57 | 7.60 | 1.00 |
| Paid Social | 264000.00 | 2 | 42500.00 | 132000.00 | 99.40 | 1.00 |

## Decisoes Recomendadas
1. Usar multi-touch equal como modelo operacional e manter first/last-touch como leitura de sensibilidade.
2. Rebalancear budget incremental para canais com payback inferior a 12 meses e retencao superior.
3. Tratar Paid Social e campanhas broad como experimentos com teto de spend ate melhora comprovada de conversao.
4. Adicionar coortes de retencao e NRR ao ritual mensal de performance de marketing.
5. Revisar eventos por ARR influenciado, nao apenas pipeline ou presenca.

## Gaps Identificados
| area | metric | severity | recommended_action |
| --- | --- | --- | --- |
| channel_efficiency | cac_payback_months | critical | Reduzir budget de lead ads amplos e manter apenas retargeting com prova de produto. |
| budget_allocation | event_efficiency_vs_referral | high | Migrar parte do budget de eventos para referral e partner motions com accountability por ARR. |
| channel_efficiency | cac | high | Separar campanhas core intent de broad match e reportar CAC por subcampanha. |
| attribution_governance | last_vs_first_touch_delta | critical | Criar modelo multi-touch oficial e governar decisao de budget por mais de um modelo. |
