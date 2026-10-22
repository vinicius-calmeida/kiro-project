# ADR-004 — Processamento em Python vetorizado

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O núcleo computacional é o unmixing espectral: estimar, para cada pixel e data, as frações dos componentes (endmembers) a partir da assinatura espectral observada. O modelo é linear; com as restrições usuais (frações não negativas e soma igual a 1) o problema é de mínimos quadrados com restrições (FCLS), resolvido por pixel. Em escala de fazenda são alguns milhões de linhas pixel×data.

## Decisão

Implementar o pipeline em **Python vetorizado** sobre tabelas: numpy/scipy para o cálculo, DuckDB e Polars para consulta e transformação. O solver do unmixing é implementação própria, vetorizada (ou acelerada com numba), validada contra `scipy.optimize.nnls` em uma amostra.

## Alternativas consideradas

- **xarray + Dask**: adequado a cubos de dados e a clusters; contraria a premissa tabular e adiciona complexidade desnecessária para uma fazenda.
- **Unmixing dentro do GEE**: descartado pela ADR-001.
- **Bibliotecas dedicadas de unmixing**: algumas são pouco mantidas; implementar o solver dá controle total, o que ajuda a auditabilidade.

## Consequências

- Simplicidade e facilidade de depuração: tabela entra, tabela sai.
- Escala até dezenas de milhares de hectares em um notebook; se o escopo crescer muito, a lógica científica está isolada em módulo e pode migrar.
- **Validação em duas camadas**: (1) o código é correto, provado com misturas sintéticas de frações conhecidas; (2) os endmembers representam a fazenda, julgamento da Angela. O EC registra as duas.

## Pontos em aberto

- Escolha do algoritmo do solver (laço com NNLS acelerado, ou método vetorizado em lote) a decidir na implementação, com medição de desempenho.
