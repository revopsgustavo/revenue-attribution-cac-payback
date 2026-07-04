# Production Flow

1. Gerar dados com `python src/generate_data.py`.
2. Calcular gaps com `python src/consultant_gap_finder.py`.
3. Validar qualidade com `python src/data_quality.py`.
4. Gerar analise consultiva com `python src/ai_consultant.py`.
5. Rodar testes com `python -m pytest`.
6. Abrir dashboard com `streamlit run app/streamlit_app.py`.
