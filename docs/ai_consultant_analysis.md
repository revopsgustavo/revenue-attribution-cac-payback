# AI Consultant Analysis

## Veredito executivo
Os dados sugerem que a empresa tem tracao de receita, mas ainda nao deve escalar budget sem governar CAC Payback por canal e sensibilidade dos modelos de atribuicao. O case mostra R$ 6.629.000,00 de ARR novo, CAC medio de R$ 11.014,60, payback consolidado de 3.5 meses e LTV/CAC de 3.44x. Foram identificados 2 gaps criticos e 2 gaps altos.

## Leitura da operacao
O problema central nao e apenas gerar demanda; e saber qual demanda cria receita com payback saudavel. Paid Social e parte de Paid Search trazem volume, mas pressionam eficiencia. Referral, Partner e Organic mostram melhor qualidade economica, enquanto Events precisa de governanca mais dura para justificar spend por ARR e nao por presenca ou pipeline bruto.

## Principais gaps criticos
- **channel_efficiency | cac_payback_months**: Paid Social concentra volume de leads, mas apresenta payback acima do limite executivo. Acao recomendada: Reduzir budget de lead ads amplos e manter apenas retargeting com prova de produto.
- **attribution_governance | last_vs_first_touch_delta**: A leitura de receita por canal muda de forma relevante entre first-touch e last-touch. Acao recomendada: Criar modelo multi-touch oficial e governar decisao de budget por mais de um modelo.

## Gaps altos
- **budget_allocation | event_efficiency_vs_referral**: Events recebe investimento materialmente maior, mas converte menos que Referral. Acao recomendada: Migrar parte do budget de eventos para referral e partner motions com accountability por ARR.
- **channel_efficiency | cac**: Paid Search gera captura de demanda, mas CAC fica muito acima de canais orgânicos e referral. Acao recomendada: Separar campanhas core intent de broad match e reportar CAC por subcampanha.

## Gaps medios
- Nenhum gap nesta severidade.


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
