# ADR-008 — Monorepo único e ferramentas de qualidade

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

O blueprint pede memória institucional e rastreabilidade (Decision Log, versionamento) e separação entre propriedade, autoria e acesso (parceria com a Angela). Também exige proteger o método como segredo de negócio.

## Decisão

- **Um único repositório privado** no GitHub, contendo código, configuração, testes e documentação. Dados e segredos ficam fora do Git.
- Parâmetros científicos em pasta própria (`configs/parametros_cientificos/`), para que uma futura separação em repositório próprio seja barata, se a conversa jurídica sobre propriedade intelectual exigir.
- Ferramentas: **uv** (dependências), **pytest**, **ruff**, **pre-commit**, **GitHub Actions** (testes e lint a cada push), **Docker**.
- Três tipos de teste obrigatórios: mistura sintética do unmixing, golden de reprodutibilidade (hash do EC de um mini conjunto fixo) e validação do arquivo de parâmetros.

## Alternativas consideradas

- **Repositórios separados** (motor, parâmetros, infra): permite dar acesso à Angela só ao repositório de parâmetros e alinha à separação de autoria/acesso; mas exige fixar versões entre repositórios e complica o manifesto.

## Consequências

- Um commit descreve código, parâmetros e configuração juntos; é esse hash que vai no manifesto.
- A autoria de cada arquivo fica no histórico do Git.
- Controle de acesso por pasta é limitado; rever junto com o jurídico.
