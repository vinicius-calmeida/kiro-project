# ADR-003 — Execução local em Docker; S3 versionado opcional

- **Status:** Aceita para a execução local; **o uso do S3 está pendente de confirmação**
- **Data:** 2026-10-21

## Contexto

Os documentos dos sócios definem a stack de ferramentas, mas não dizem onde ela roda. Para uma fazenda, com dados tabulares, o volume cabe em um notebook. O blueprint pede para não construir infraestrutura completa antes de validar mercado.

## Decisão

- Processar e armazenar **localmente**, em contêiner Docker com versões fixas.
- Usar, **opcionalmente**, um único bucket **S3 com versionamento e criptografia em repouso** para guardar artefatos relevantes (GeoParquet de saída, arquivo de parâmetros, EC, manifestos, backup do volume do immudb). Terraform só entra para provisionar esse bucket.
- VM na nuvem só quando houver necessidade real (território grande demais para o notebook, ou demonstração remota a cliente).

## Alternativas consideradas

- **100% local, sem S3**: zero custo e zero setup; sem backup nem compartilhamento fácil.
- **VM na nuvem**: dá acesso remoto; custo e operação (patch, backup, segurança) sem necessidade no P0.
- **Serverless (Lambda, Step Functions, Fargate)**: justificado no monitoramento recorrente (Fase 2); complexidade alta (IAM, eventos, depuração distribuída) e limite de tempo/memória do Lambda para processamento pesado.

## Consequências

- Custo praticamente zero no P0 (S3: centavos por mês para menos de 1 GB).
- Reprodutibilidade garantida pelo Docker; backup e rastreabilidade ganhos com o S3 versionado.
- Aprendizado de AWS/Terraform acontece em escala proporcional.

## Pontos em aberto

- Confirmar se o S3 entra já no P0 ou se começa sem ele.
- Avaliar créditos para startups da AWS.
