# ADR-005 — Orquestração com scripts e Makefile

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O pipeline tem cerca de seis passos (coletar, gravar em Parquet, unmixing, features e baseline, detecção de mudança, montar o EC), executados sob demanda para uma fazenda. A questão é quem dispara e controla a execução.

## Decisão

Usar **scripts Python (CLI) + Makefile + Docker**. Cada passo é uma função pura exposta como subcomando; o Makefile encadeia os passos. Cada execução gera um **manifesto de execução**.

## Alternativas consideradas

- **Prefect ou Dagster**: retries, interface e agendamento; passa do ponto para seis passos manuais. O Dagster casa bem com a linhagem dado → feature → EC e é candidato na Fase 2.
- **AWS Step Functions / Airflow gerenciado**: só compensam com monitoramento recorrente; o Airflow gerenciado tem custo mensal relevante.

## Consequências

- Zero dependências extras e custo zero.
- Sem interface, retries automáticos nem agendamento nativo (cron ou GitHub Actions podem cobrir o necessário).
- Migrar para Prefect/Dagster depois é barato porque a lógica científica não depende do orquestrador.
