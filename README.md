# Pacote de contexto e specs para o Kiro — EERA P0 (EC-001)

Rascunho preparado em 2026-10-21 a partir das decisões tomadas até agora. Tudo aqui é **para revisão** pelos três sócios antes de virar código.

## O que tem no pacote

```
.kiro/steering/product.md      contexto do produto, da tese e do escopo do P0
.kiro/steering/tech.md         stack, decisões vigentes e restrições
.kiro/steering/structure.md    estrutura do repositório e convenções
.kiro/specs/ec-001-pipeline-p0/requirements.md   14 requisitos com critérios de aceite (EARS)
.kiro/specs/ec-001-pipeline-p0/design.md         arquitetura, modelos de dados, testes, riscos
docs/adr/001 a 010             uma decisão por arquivo
docs/decision-log.md           índice das decisões
```

Não há `tasks.md` de propósito: o Kiro gera a lista de tarefas a partir do design depois que você aprovar as duas primeiras fases.

## Como usar no Kiro

1. Crie o repositório (privado) e copie estas pastas para a raiz, mantendo os caminhos.
2. Abra a pasta no Kiro. Os três arquivos de `.kiro/steering/` passam a ser contexto de toda interação. Se quiser, ajuste o modo de inclusão deles no próprio Kiro.
3. Abra a spec `ec-001-pipeline-p0`. Peça ao Kiro para **revisar** o `requirements.md` e o `design.md` (apontar lacunas, ambiguidades e contradições), sem reescrever do zero. Aprove cada fase antes de seguir.
4. Só depois de aprovar o design, peça para gerar o `tasks.md` e execute as tarefas uma a uma, começando pela configuração e pelos testes.
5. Quando as perguntas em aberto forem respondidas, atualize o ADR correspondente (ou crie um ADR novo) e depois os requisitos.

Sugestão de primeiro prompt: "Revise o requirements.md e o design.md desta spec à luz do steering e dos ADRs em docs/adr. Liste contradições, lacunas e riscos antes de qualquer alteração."

## Cuidados

- **Propriedade intelectual.** O método e os parâmetros são segredo de negócio. Não coloque os valores reais dos parâmetros da Angela em steering, specs ou prompts; use valores fictícios (como nos exemplos). Confira as configurações de privacidade e de uso de dados do Kiro para o seu plano.
- **Segredos.** Nunca coloque chaves, senhas ou tokens em steering, specs ou no chat do Kiro. Use variáveis de ambiente.
- **Rascunho.** Os requisitos e o design têm pontos em aberto que dependem da Angela (sensor, bandas, endmembers, índice, limiares, baseline, máscaras, validação) e do Alexandre (clientes, território piloto, formato do relatório). Ver o fim de `requirements.md`.
- **Confirmações técnicas.** Nomes de pacotes e APIs (cliente WTSS do BDC, SDK do immudb, WeasyPrint) devem ser confirmados nas versões fixadas na implementação.
