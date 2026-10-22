# ADR-009 — Sem Kubernetes e sem serverless no P0

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O MDS-GS é descrito conceitualmente como serverless e orientado a eventos. O P0, porém, é um MVP de validação de mercado para uma fazenda, executado sob demanda. O blueprint determina que a empresa não construa infraestrutura científica completa antes de validar quem tem o problema.

## Decisão

Não usar **Kubernetes** nem arquitetura **serverless** (Lambda, Step Functions, EventBridge) no P0. O princípio do MDS-GS (computar perto dos dados, só a região de interesse, sem servidor ocioso) é cumprido de forma mais simples: processamento local e sob demanda.

## Consequências

- Menos operação e menos custo; foco em validar o EC-001 e o valor econômico da evidência.
- Kubernetes só faz sentido a partir da Fase 3 (Evidence Platform) ou Fase 4 (API/licenciamento), com múltiplos ECs e clientes.
- Serverless entra na Fase 2 (monitoramento recorrente), quando o pipeline precisar rodar por evento (nova imagem disponível).
- Para o aprendizado de AWS/CLF-C02, o caminho é o uso de S3 e Terraform em escala proporcional (ADR-003), sem forçar complexidade ao projeto.
