# Decision Log

| ADR | Data | Decisão | Status |
|---|---|---|---|
| 001 | 2026-10-21 | BDC como fonte principal de dados | Aceita (coleção/sensor a confirmar com a Angela) |
| 002 | 2026-10-21 | Dados tabulares por pixel em GeoParquet, sem imagens inteiras | Aceita |
| 003 | 2026-10-21 | Execução local em Docker; S3 versionado opcional | Aceita (S3 a confirmar) |
| 004 | 2026-10-21 | Processamento em Python vetorizado (numpy/scipy, DuckDB/Polars) | Aceita |
| 005 | 2026-10-21 | Orquestração com scripts, Makefile e Docker | Aceita |
| 006 | 2026-10-21 | Integridade com immudb e manifesto de execução | Aceita |
| 007 | 2026-10-21 | Relatório como entrega; Streamlit como ferramenta interna | Aceita |
| 008 | 2026-10-21 | Monorepo único privado e ferramentas de qualidade | Aceita |
| 009 | 2026-10-21 | Sem Kubernetes e sem serverless no P0 | Aceita |
| 010 | 2026-10-21 | Parâmetros científicos em arquivo de configuração versionado | Aceita |
