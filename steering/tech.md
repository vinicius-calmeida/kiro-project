# Stack técnica e restrições — EERA P0

As decisões abaixo foram tomadas pelos sócios e estão registradas em `docs/adr/`. Não as altere sem um novo ADR.

## Decisões vigentes

| Tema | Decisão | ADR |
|---|---|---|
| Fonte de dados | Brazil Data Cube (BDC), via STAC e WTSS | 001 |
| Formato dos dados | Tabelas GeoParquet, um pixel por linha por data; sem imagens inteiras | 002 |
| Onde roda | Local, em Docker; S3 versionado obrigatório para backup e artefatos | 003, 011 |
| Processamento | Python vetorizado (numpy/scipy), DuckDB/Polars para dados tabulares | 004 |
| Orquestração | Scripts Python + Makefile + Docker | 005 |
| Integridade | immudb (hashes) + manifesto de execução por rodada | 006 |
| Entrega | Relatório PDF primeiro; Streamlit como ferramenta interna | 007 |
| Repositório | Monorepo único, privado, com qualidade automatizada | 008 |
| Infra | Sem Kubernetes e sem serverless no P0 | 009 |
| Ciência | Parâmetros científicos em arquivo versionado, nunca no código | 010 |

## Ferramentas

- Python 3.12 ou superior; gerenciador de dependências **uv**; versões fixadas em lockfile.
- Dados: **DuckDB**, **Polars** (ou pandas onde simplificar), **pyarrow**, GeoParquet.
- Cálculo: **numpy**, **scipy**; **numba** se o solver do unmixing exigir aceleração.
- Acesso ao BDC: `pystac-client` (STAC) e cliente WTSS do BDC (confirmar o pacote e a versão na implementação).
- Integridade: SDK Python do immudb (confirmar a API na versão fixada); hash **SHA-256**.
- Configuração e validação: **pydantic** + arquivos YAML.
- Relatório: **Jinja2** + **WeasyPrint** (ou Quarto, se for mais simples) para PDF/HTML estático; gráficos com matplotlib ou plotly estático.
- Ferramenta interna: **Streamlit**, rodando em `localhost`.
- Qualidade: **pytest**, **ruff**, **pre-commit**, **GitHub Actions**.
- Contêineres: **Docker** com imagem de versões fixas.
- Infra: **Terraform** para o bucket S3 obrigatório (versionamento, criptografia em repouso, bloqueio de acesso público, acesso mínimo). Ver ADR-011.

## Restrições obrigatórias

1. **Nunca baixar imagens de satélite inteiras.** Consultar só a região de interesse, as bandas e as datas necessárias.
2. **Nenhum número científico no código.** Endmembers, bandas, índice, janela do baseline e limiares vêm do arquivo de parâmetros.
3. **Dados e segredos fora do Git.** Dados em `data/` (ignorado pelo Git); chaves e senhas em variáveis de ambiente. Nunca em steering, specs, ADRs ou testes.
4. **immudb guarda só hashes e metadados**, nunca os dados.
5. **Cada passo do pipeline é uma função pura**: recebe entradas e parâmetros, devolve saídas, sem estado escondido. Isso permite trocar o orquestrador depois sem reescrever a lógica.
6. **Determinismo**: mesma entrada + mesmos parâmetros + mesmo código = mesmo EC (mesmo hash). Fixar seeds e versões.
7. **Todo resultado carrega incerteza e limitações** e nunca usa linguagem de certificação.
8. **Não adicionar dependência, serviço ou infraestrutura fora desta lista** sem perguntar e sem registrar um ADR.

## Metas indicativas de desempenho (a confirmar)

- Fazenda de até ~1.000 ha (Sentinel-2, 10 m): pipeline completo em minutos no notebook.
- Fazenda de até ~10.000 ha: viável em notebook com memória suficiente; reavaliar se passar disso.

## Segurança e propriedade intelectual

O método e os parâmetros científicos são segredo de negócio. O repositório é privado, com acesso mínimo. Os valores reais dos parâmetros da Angela não devem aparecer em steering, specs ou prompts; usar valores fictícios nos exemplos e testes.
