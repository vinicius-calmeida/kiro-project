# ADR-011 — S3 versionado obrigatório no P0

- **Status:** Aceita
- **Data:** 2026-10-22
- **Supersede parcialmente:** ADR-003 (que deixava o S3 opcional)
- **Decisores:** Vinícius (engenharia), com concordância dos sócios

## Contexto

O ADR-003 deixou o uso do S3 como **opcional** ("S3 a confirmar"). Essa opcionalidade criou um buraco de governança: o ADR-006 declara o backup do volume do immudb como **obrigatório** ("backup obrigatório (S3, se usado)"), mas o único meio de backup descrito — o próprio S3 — era opcional. Resultado: um requisito obrigatório (preservar o histórico de integridade) dependia de um meio opcional.

Perder o volume do immudb é perder a cadeia de integridade de todas as execuções anteriores; isso é incompatível com os princípios de rastreabilidade e auditabilidade do blueprint. Além disso, o S3 versionado dá uma segunda cópia, imutável por versionamento, dos artefatos citáveis de cada execução (EC, manifesto, parâmetros, saídas), reforçando a reprodutibilidade.

## Decisão

- O **S3 versionado passa a ser obrigatório no P0**, não mais opcional.
- Um único bucket, provisionado por **Terraform**, com: versionamento habilitado, criptografia em repouso, bloqueio de acesso público e política de acesso mínimo.
- Conteúdo do bucket (apenas artefatos definidos): GeoParquet de saída, arquivo de parâmetros científicos, EC, manifestos e **backup do volume do immudb**.
- O backup do immudb para o S3 é parte do procedimento de cada rodada (ou de uma rotina agendada), não um passo manual esquecível.
- Os **dados brutos e segredos continuam fora do S3 versionado controlado pelo cliente/empresa** na forma definida: segredos em variáveis de ambiente; dados brutos locais em `data/` (o S3 guarda apenas os artefatos listados, não os brutos, salvo se explicitamente desejado como cache).

## Alternativas consideradas

- **Manter o S3 opcional (ADR-003)**: menor custo/setup, mas deixa o backup do immudb sem garantia — rejeitada por criar a contradição descrita.
- **Backup local (segundo volume / disco externo)**: zero dependência de nuvem, mas sem imutabilidade por versionamento e sem cópia fora do host; frágil para a finalidade de integridade.
- **Object Lock (WORM) no S3**: reforça a imutabilidade além do versionamento. Fica como evolução futura (quando um cliente exigir verificação por terceiro, junto da âncora externa do ADR-006); não é exigido agora para não aumentar a complexidade operacional.

## Consequências

- Custo deixa de ser zero, mas permanece desprezível no P0 (menos de 1 GB; centavos/mês, como estimado no ADR-003).
- O backup do immudb passa a ter um destino garantido; o ADR-006 fica satisfeito sem ressalva.
- O Terraform entra no P0 para provisionar o bucket (aprendizado de AWS/IaC em escala proporcional, como previsto no ADR-003/009).
- A credencial de acesso à AWS entra na lista de segredos geridos por variável de ambiente, nunca versionados.
- O ponto em aberto "o S3 entra já no P0?" fica **resolvido**: entra.

## Pontos em aberto

- Avaliar créditos para startups da AWS (herdado do ADR-003).
- Momento de adotar Object Lock e âncora externa (ligado ao ADR-006), provavelmente com o primeiro cliente que exigir verificação por terceiro.
