# ADR-007 — Entrega: relatório primeiro, Streamlit como ferramenta interna

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O one-pager pede "dashboard/relatório demonstrável" sem fechar o formato. O produto inicial é uma *Environmental Evidence Assessment*: serviço especializado que entrega análise, EC, relatório, rastreabilidade, integridade e limitações. Os clientes-alvo ainda não estão definidos e podem ser mais de um.

## Decisão

- A entrega principal é um **relatório** (PDF e/ou HTML estático) gerado a partir do EC, com o **hash impresso e registrado no immudb**.
- O **Streamlit** é mantido como ferramenta interna (exploração dos resultados por Vinícius, Angela e Alexandre, e demonstrações projetadas), rodando em `localhost`. Não é descartado como possível entrega futura.
- O pipeline é **orientado a configuração**: o modelo de relatório é um arquivo de configuração por cliente.

## Alternativas consideradas

- **Só dashboard**: bom para exploração, ruim como artefato formal e auditável (a tela muda com os filtros); exige hospedagem e autenticação.
- **Os dois como entrega**: custo maior sem validação de demanda.

## Consequências

- Artefato fixo, arquivável e com hash; sem superfície de ataque nem custo de hospedagem.
- Um dashboard para cliente fica para a Fase 2 (monitoramento recorrente), se a demanda justificar.
- A escolha final do formato por cliente depende do cliente-alvo (decisão do Alexandre).
