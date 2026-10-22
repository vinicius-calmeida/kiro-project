# ADR-001 — Fonte de dados: Brazil Data Cube (BDC)

- **Status:** Aceita
- **Data:** 2026-10-21
- **Decisores:** Vinícius (engenharia), com validação pendente da Angela sobre a coleção

## Contexto

O P0 precisa de séries temporais de reflectância por pixel para uma fazenda. As fontes consideradas foram o BDC (INPE) e o Google Earth Engine (GEE). A Angela já trabalhou no INPE e conhece o BDC. O blueprint exige rastreabilidade, reprodutibilidade e proteção do método (trade secret).

## Decisão

Usar o **BDC como fonte principal**, acessado por STAC (leitura de janelas) e WTSS (séries temporais por coordenada). O GEE fica como ferramenta de prototipagem eventual, nunca como parte do pipeline de produção.

## Alternativas consideradas

- **GEE**: catálogo enorme e computação no servidor; porém o uso comercial exige licença paga, a computação roda em infraestrutura de terceiros (caixa-preta, difícil de reproduzir e de auditar) e o método ficaria exposto a esse ambiente.
- **BDC** (escolhida): gratuito, cubos versionados e citáveis, dados em formato aberto; exige que a leitura e o cálculo sejam feitos pela equipe.

## Consequências

- Reprodutibilidade melhor: dá para citar a coleção, a versão e os itens exatos usados.
- O método permanece na infraestrutura da empresa.
- A equipe implementa a leitura e o unmixing; a disponibilidade e o desempenho do BDC podem variar.
- É preciso cadastro e chave de acesso ao serviço STAC do BDC (guardar como variável de ambiente).

## Pontos em aberto

- Qual **coleção/sensor** (Sentinel-2, Landsat etc.) e quais **bandas** os parâmetros da Angela assumem. Há trade-off entre resolução (10 m no Sentinel-2) e profundidade histórica para o baseline (décadas no Landsat, porém a 30 m).
- Confirmar termos de uso do BDC para finalidade comercial.
