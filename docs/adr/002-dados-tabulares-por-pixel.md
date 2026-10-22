# ADR-002 — Dados tabulares por pixel (sem imagens inteiras)

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O blueprint define que a plataforma não baixa imagens de satélite inteiras: consulta só a região de interesse e processa só o necessário. O one-pager define a cadeia BDC → Parquet → DuckDB. Os sócios querem gastar menos processamento do que o processamento de imagens completas exigiria.

## Decisão

Trabalhar com **tabelas** (GeoParquet) em vez de rasters: uma linha por pixel por data, com as bandas necessárias como colunas. Os dados chegam já recortados na fazenda, nas bandas e nas datas que o EC usa (a regra "nenhum dado sem função explícita" vale para colunas e datas também).

## Alternativas consideradas

- **COG/Zarr (rasters)**: natural para imagens, mas contraria a premissa tabular e exige pensar em arrays e cubos.
- **Tabelas agregadas por polígono**: muito menores, mas perdem a precisão de pixel desejada para o "onde" do EC.

## Consequências

- Parquet é o formato principal; DuckDB e Polars consultam direto.
- O volume **não** é menor por ser tabular: se todos os pixels forem usados, o tamanho é comparável ao do raster. A economia vem de recortar território, bandas, datas e de comprimir em Parquet. Estimativa indicativa (Sentinel-2, 10 bandas, ~45 datas): 1.000 ha ≈ 100 mil pixels ≈ 200 MB brutos; 10.000 ha ≈ 18 GB brutos.
- Cada tabela guarda, nos metadados do arquivo, a origem (coleção, itens, consulta, data da consulta, fatores de escala).

## Pontos em aberto

- Se o unmixing deve rodar por pixel e só depois agregar, ou se a Angela aceita agregar a assinatura antes (com restrições de não negatividade e soma 1, os resultados divergem).
- Tratamento de nuvem, sombra e água (máscaras) e como isso entra na tabela.
