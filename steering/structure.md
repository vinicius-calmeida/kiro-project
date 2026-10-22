# Estrutura do repositório e convenções

Monorepo único, privado. Idioma da documentação: português. Identificadores de código: inglês ou português, mas **consistente** (preferência: nomes de domínio em português já definidos no glossário, ex.: `baseline`, `ec`; verbos e termos técnicos em inglês).

## Árvore

```
eera/
├── .kiro/
│   ├── steering/            product.md, tech.md, structure.md
│   └── specs/               uma pasta por feature (requirements, design, tasks)
├── src/eera/
│   ├── coleta/              acesso ao BDC (STAC/WTSS) e gravação em GeoParquet
│   ├── unmixing/            solver FCLS e cálculo de frações
│   ├── features/            índices, séries temporais, métricas
│   ├── baseline/            comportamento esperado por pixel
│   ├── deteccao/            detecção de mudança (onde, quando, magnitude, trajetória)
│   ├── ec/                  montagem e serialização do Evidence Card
│   ├── integridade/         manifesto, hashes, cliente immudb, verificação
│   ├── relatorio/           geração do PDF/HTML a partir do EC
│   ├── config/              modelos pydantic dos arquivos de configuração
│   └── cli.py               ponto de entrada (um subcomando por passo)
├── configs/
│   ├── territorio/          fazenda, geometria, período
│   ├── parametros_cientificos/   endmembers, bandas, índice, baseline, limiares (da Angela)
│   └── relatorio/           modelos de relatório por cliente
├── tests/
│   ├── unit/                misturas sintéticas, funções puras
│   ├── golden/              mini conjunto fixo e hash esperado do EC
│   └── config/              validação dos arquivos de parâmetros
├── docs/
│   ├── adr/                 NNN-titulo-curto.md
│   ├── decision-log.md
│   └── ec-001-especificacao.md
├── infra/                   Terraform do bucket S3 (somente se usado)
├── data/                    ignorado pelo Git (brutos, intermediários, saídas)
├── Makefile
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Convenções

- **Um módulo por etapa do pipeline**; módulos não importam uns aos outros fora da ordem do fluxo (coleta → unmixing → features → baseline → deteccao → ec → relatorio). `integridade` é transversal e só lê artefatos.
- **Funções puras** nas etapas; entrada e saída por arquivo (Parquet/JSON) ou por tabela Arrow, nunca por estado global.
- **Configuração por arquivo**, validada com pydantic antes de qualquer execução. Falha rápida com mensagem clara.
- **Cada execução** tem um `run_id` e grava seus artefatos em `data/runs/<run_id>/` junto com o manifesto.
- **ADRs**: `docs/adr/NNN-titulo-curto.md`, com status, contexto, decisão, alternativas e consequências. Uma decisão nova ou mudança de decisão gera um ADR novo.
- **Commits** pequenos e descritivos; branch principal protegida quando o plano do GitHub permitir; testes e lint rodam em cada push.
- **Testes**: três tipos obrigatórios (mistura sintética, golden de reprodutibilidade, validação de parâmetros). Toda função científica nova entra com teste.
- **Nomes de arquivos de dados**: `<territorio>_<colecao>_<inicio>_<fim>.parquet`, em minúsculas, sem acentos.
- **Segredos**: `.env` local fora do Git; `.env.example` versionado sem valores.
