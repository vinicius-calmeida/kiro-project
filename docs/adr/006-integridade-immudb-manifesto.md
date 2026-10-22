# ADR-006 — Integridade com immudb e manifesto de execução

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O blueprint exige demonstrar a cadeia dado → versão → processamento → Evidence Card → relatório → registro de integridade, guardando hashes e não os dados. O one-pager lista o immudb como entregável. A empresa não certifica conformidade; a integridade serve à rastreabilidade e à auditabilidade.

## Decisão

- Usar o **immudb** (Docker, volume persistente) como camada de integridade.
- Cada execução produz um **manifesto**: hash do commit do código, hash do arquivo de parâmetros, identificação e hash dos dados de entrada, versões das dependências, hashes das saídas, hash do EC e hash do relatório.
- O **hash do manifesto** (e os hashes do EC e do relatório) são registrados no immudb. Os dados nunca vão para o immudb.
- Verificação: dado um EC, recalcular os hashes dos artefatos e conferir com o registro e com a prova de inclusão do immudb.

## Alternativas consideradas

- **Manifesto + Git + S3 com Object Lock**: mais simples e sem serviço extra; a verificação é código próprio. Fica como plano B.
- **Âncora externa** (carimbo do tempo ICP-Brasil, possivelmente com peso jurídico; confirmar com o jurídico): complemento futuro, não alternativa.

## Consequências

- Atende o entregável do one-pager e o princípio de rastreabilidade.
- Um immudb operado pela própria empresa prova que o registro não foi alterado depois, mas **não prova a terceiros** que não foi recriado do zero. Para responder "quem pode verificar?" será necessária âncora externa. O desenho deve permitir isso: o manifesto é um arquivo com hash bem definido, passível de carimbo.
- Perder o volume do immudb é perder o histórico: backup obrigatório (S3, se usado).

## Pontos em aberto

- Quando introduzir a âncora externa (provavelmente com o primeiro cliente que exigir verificação por terceiro).
- Determinismo do hash de arquivos Parquet entre versões de bibliotecas (ver o design: hash do conteúdo lógico).
