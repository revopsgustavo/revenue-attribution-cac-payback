# Revenue Attribution and CAC Payback for B2B SaaS RevOps

Case analitico completo para diagnosticar atribuicao de receita, eficiencia de canais, CAC Payback e alocacao de budget em uma operacao SaaS B2B. O projeto foi estruturado para vitrine GitHub, com dados sinteticos reprodutiveis, dashboard Streamlit, testes automatizados, SQLite e uma camada de consultoria de gaps orientada a decisao executiva.

## Executive Summary
- ARR novo analisado: R$ 6.629.000,00
- Investimento de marketing: R$ 1.509.000,00
- Novos clientes: 137
- CAC medio: R$ 11.014,60
- CAC Payback consolidado: 3.5 meses
- LTV/CAC estimado: 3.44x
- Retencao 90d: 100,0%

## Problema de Negocio
Marketing e RevOps frequentemente tomam decisoes com base em CPL, MQL ou pipeline bruto. Este case mostra como a decisao muda quando a analise passa a considerar ARR, clientes conquistados, margem, retencao, CAC Payback e diferencas entre modelos de atribuicao.

## Principais Insights
- Referral lidera em ARR novo, mas a decisao de escala depende de payback e retencao.
- Paid Social apresenta o maior payback e deve ser tratado como experimento controlado, nao como canal de escala automatica.
- A leitura por first-touch, last-touch e multi-touch muda a distribuicao de credito por canal, exigindo governanca de atribuicao.
- Canais como Referral, Partner e Organic sustentam melhor eficiencia economica e devem orientar realocacao incremental de budget.

## Estrutura
- `src/revenue_attribution_pipeline.py`: geracao deterministica dos dados e SQLite.
- `src/metrics.py`: metricas executivas, eficiencia por canal e variancia de atribuicao.
- `src/consultant_gap_finder.py`: gaps consultivos com evidencia, perguntas e acoes recomendadas.
- `src/ai_consultant.py`: analise executiva rule-based em markdown.
- `app/streamlit_app.py`: dashboard executivo em Streamlit.
- `tests/`: testes de dados, metricas, gaps e import do dashboard.

## Como Rodar
```bash
python src/generate_data.py
python src/consultant_gap_finder.py
python src/data_quality.py
python src/ai_consultant.py
python -m pytest
streamlit run app/streamlit_app.py
```

## Artefatos
- Dados CSV: `data/processed/`
- Banco SQLite: `data/database/revenue_attribution_case.sqlite`
- Analise executiva: `docs/executive_analysis.md`
- Consultoria IA: `docs/ai_consultant_analysis.md`
- Dicionario de metricas: `docs/metrics_dictionary.md`

## Dashboard Preview
O dashboard Streamlit fica em `app/streamlit_app.py`. Screenshots devem ser adicionados em `docs/screenshots/` antes da divulgação pública.

## Data Disclaimer
Todos os dados são sintéticos. O projeto não usa APIs externas nem dados reais. As análises são rule-based e devem ser tratadas como hipóteses para validação, não como causa raiz confirmada.

## Consulting Use Case
Este case pode ser usado como base para diagnóstico RevOps em SaaS B2B, apoiando liderança com evidências, hipóteses, perguntas de validação, responsáveis e métricas de acompanhamento.

## Contact
LinkedIn: https://www.linkedin.com/in/gustavo-worliczek-lazzarotto/  
E-mail: gustavo.lazzaro77o@gmail.com

