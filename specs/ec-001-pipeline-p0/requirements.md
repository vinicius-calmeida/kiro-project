# Documento de requisitos — Pipeline P0 do EC-001 (Environmental Change Detection)

## Introdução

Este documento descreve o que o sistema deve fazer para produzir, a partir de dados do BDC, o **Evidence Card EC-001** de uma fazenda piloto, com precisão de pixel, e entregá-lo como relatório rastreável e verificável. As decisões técnicas estão em `docs/adr/` e no steering (`tech.md`). Este é um **rascunho para revisão** pelos três sócios.

**Personas**

- **Analista técnico** (Vinícius): executa o pipeline, mantém o código e a infraestrutura.
- **Cientista** (Angela): fornece e revisa os parâmetros científicos e valida os resultados.
- **Responsável de produto** (Alexandre): define território, período e modelo de relatório por cliente.
- **Leitor do relatório** (cliente, ainda indefinido): recebe e usa a evidência.
- **Verificador** (terceira parte): confere a integridade e a origem da evidência.

**Convenção de escrita:** critérios de aceite no formato EARS (QUANDO … ENTÃO o sistema DEVE …).

---

## Requisito 1 — Configuração de uma execução

**História:** Como analista técnico, quero descrever cada execução por arquivos de configuração, para trocar fazenda, período, parâmetros e modelo de relatório sem alterar código.

**Critérios de aceite**

1. QUANDO uma execução é iniciada ENTÃO o sistema DEVE carregar e validar os arquivos de território, parâmetros científicos e relatório antes de qualquer acesso a dados externos.
2. QUANDO um arquivo de configuração estiver incompleto ou inconsistente (por exemplo, um endmember sem assinatura em alguma banda, ou limiares fora de ordem) ENTÃO o sistema DEVE interromper a execução e indicar o campo e o motivo.
3. O sistema DEVE atribuir a cada execução um identificador único (`run_id`) e gravar todos os artefatos em uma pasta própria.
4. O sistema NÃO DEVE conter valores científicos (endmembers, bandas, índice, janela do baseline, limiares) no código.

## Requisito 2 — Coleta de pixels no BDC

**História:** Como analista técnico, quero obter só os pixels da fazenda, nas bandas e datas necessárias, para não baixar imagens inteiras.

**Critérios de aceite**

1. QUANDO a coleta é executada ENTÃO o sistema DEVE consultar o BDC apenas para a geometria da fazenda, o período e as bandas definidos na configuração.
2. O sistema NÃO DEVE baixar nem armazenar imagens de satélite inteiras.
3. QUANDO a coleta termina ENTÃO o sistema DEVE registrar a origem dos dados: coleção, versão, identificadores dos itens consultados, parâmetros da consulta, data e hora da consulta e fatores de escala.
4. SE a consulta falhar por indisponibilidade temporária ENTÃO o sistema DEVE tentar novamente de forma limitada e, persistindo a falha, DEVE encerrar com mensagem clara sem gravar resultado parcial como completo.
5. QUANDO a mesma coleta é repetida com a mesma configuração ENTÃO o sistema DEVE produzir a mesma tabela, ou indicar que os dados de origem mudaram.
6. A chave de acesso ao BDC DEVE ser lida de variável de ambiente e nunca gravada em arquivo versionado.
7. ENQUANTO os termos de uso do BDC para finalidade comercial não forem confirmados (ADR-001), uma execução destinada a entrega comercial DEVE ser bloqueada ou marcada de forma visível como "não liberada para uso comercial"; execuções de desenvolvimento e teste permanecem liberadas.

## Requisito 3 — Armazenamento tabular

**História:** Como analista técnico, quero os dados em tabelas GeoParquet consultáveis por DuckDB, para processar com pouco custo.

**Critérios de aceite**

1. O sistema DEVE gravar uma linha por pixel por data, com identificador estável do pixel, coordenadas do centro do pixel, data, bandas e indicadores de qualidade (máscaras de nuvem, sombra e água).
2. O sistema DEVE gravar os metadados de origem nos metadados do arquivo.
3. O sistema DEVE permitir consultar as tabelas com DuckDB sem importação prévia.
4. Os dados de `data/` NÃO DEVEM ser versionados no Git.

## Requisito 4 — Unmixing espectral

**História:** Como cientista, quero que cada pixel seja decomposto em frações dos componentes que eu defini, para derivar features subpixel.

**Critérios de aceite**

1. QUANDO o unmixing é executado ENTÃO o sistema DEVE estimar, para cada pixel e data válidos, as frações de cada endmember definido nos parâmetros, com frações não negativas e somando 1.
2. O sistema DEVE calcular e gravar, por pixel e data, uma medida de erro de reconstrução (resíduo).
3. QUANDO o pixel estiver mascarado (nuvem, sombra, água) ENTÃO o sistema DEVE marcá-lo como inválido, sem estimar frações, e contar esses casos no resultado. O limiar de contaminação que decide quando um pixel conta como mascarado DEVE vir do arquivo de parâmetros, nunca estar fixo no código.
4. QUANDO o solver recebe uma mistura sintética de frações conhecidas ENTÃO o sistema DEVE recuperar essas frações dentro de uma tolerância definida nos testes.
5. O resultado do solver DEVE concordar, em uma amostra, com uma implementação de referência (`scipy.optimize.nnls` com a restrição de soma).
6. O sistema DEVE concluir o unmixing de uma fazenda de ~1.000 ha em tempo compatível com uso interativo em um notebook (meta a confirmar na medição).

## Requisito 5 — Features e baseline

**História:** Como cientista, quero séries temporais de features e um baseline do comportamento esperado, para comparar com o período analisado.

**Critérios de aceite**

1. O sistema DEVE derivar, por pixel, as features definidas nos parâmetros (por exemplo, o índice de degradação) a partir das frações.
2. O sistema DEVE construir o baseline por pixel a partir da janela histórica definida nos parâmetros, registrando o período e a quantidade de observações usadas.
3. SE um pixel tiver observações insuficientes no baseline ENTÃO o sistema DEVE marcá-lo com confiança reduzida ou como não avaliável, e registrar o motivo.

## Requisito 6 — Detecção de mudança

**História:** Como responsável de produto, quero saber onde, quando e quanto o território mudou em relação ao esperado, para responder à pergunta do EC-001.

**Critérios de aceite**

1. O sistema DEVE identificar, por pixel, desvios relevantes em relação ao baseline, segundo os limiares dos parâmetros.
2. Para cada mudança detectada, o sistema DEVE informar: localização (pixel e geometria agregada), intervalo temporal, magnitude, trajetória (evolução no tempo) e nível de confiança.
3. O sistema DEVE descrever **o que mudou**, sem atribuir causa que os dados não sustentem.
4. O sistema DEVE informar também a ausência de mudança relevante, com a mesma estrutura, quando for o caso.

## Requisito 7 — Evidence Card

**História:** Como cientista, quero que o resultado seja encapsulado em um EC com todas as seções científicas, para que a evidência seja completa e auditável.

**Critérios de aceite**

1. O sistema DEVE gerar o EC-001 em formato estruturado (JSON) contendo as 19 seções: pergunta, hipótese, território, período, fontes de dados, método, features, baseline, detecção da mudança, localização, temporalidade, magnitude, trajetória, incerteza, nível de confiança, conclusão, evidências utilizadas, rastreabilidade e integridade.
2. O EC DEVE registrar se os parâmetros usados são **provisórios** ou **aprovados** pela Angela.
3. O EC DEVE declarar limitações e condições de validade.
4. O EC DEVE ser serializado de forma canônica (ordem fixa de campos e arredondamento declarado) para permitir hash reprodutível.
5. O texto do EC NÃO DEVE afirmar certificação nem comprovação de conformidade.
6. O EC DEVE ter identidade estável: um `ec_id` determinístico derivado de (território, período, hash dos parâmetros, versão do método) e uma `versao_ec` que incrementa a cada mudança intencional de método; ambos entram na chave de registro de integridade.
7. SE os parâmetros usados forem provisórios ENTÃO o sistema NÃO DEVE produzir um EC destinado a entrega comercial sem um aval explícito registrado (campo de aprovação de exceção); por padrão, EC com parâmetros provisórios é marcado "somente desenvolvimento/validação".

## Requisito 8 — Manifesto de execução

**História:** Como verificador, quero um manifesto que ligue dados, método e resultado, para reconstruir como a evidência foi produzida.

**Critérios de aceite**

1. QUANDO uma execução termina ENTÃO o sistema DEVE gerar um manifesto contendo: `run_id`, data e hora, hash do commit do código, hash do arquivo de parâmetros, identificação e hash dos dados de entrada, versões das dependências, hashes das saídas, hash do EC e hash do relatório.
2. O sistema DEVE usar SHA-256.
3. O hash de tabelas DEVE ser calculado sobre o conteúdo lógico ordenado (e não sobre os bytes do arquivo Parquet), para ser estável entre versões de bibliotecas. A forma lógica DEVE fixar: ordem das colunas, ordenação das linhas por chave completa e determinística (todas as colunas-chave, com desempate estável), tipos declarados, e arredondamento de floats à precisão declarada nos parâmetros antes do hash.
4. A serialização canônica do EC (JSON) DEVE fixar: chaves em ordem fixa, listas internas ordenadas por critério determinístico, UTF-8 com `ensure_ascii` definido, normalização Unicode NFC, floats formatados com precisão declarada e sem `-0.0` nem notação científica, e ausência de espaços supérfluos. O SHA-256 é calculado sobre essa forma.

## Requisito 9 — Registro e verificação de integridade

**História:** Como verificador, quero registrar e conferir a integridade do EC, para detectar qualquer alteração posterior.

**Critérios de aceite**

1. QUANDO o manifesto é gerado ENTÃO o sistema DEVE registrar no immudb o hash do manifesto, do EC e do relatório, e nunca os dados.
2. QUANDO a verificação é executada para um EC ENTÃO o sistema DEVE recalcular os hashes dos artefatos, comparar com o manifesto e com o registro do immudb e informar, sem ambiguidade, se está íntegro ou se há divergência (apontando qual artefato).
3. O sistema DEVE permitir salvar o estado verificável do immudb junto da execução.
4. O volume do immudb DEVE ser persistente e DEVE ter backup no bucket S3 obrigatório (ver Requisito 13.3 e ADR-011) como parte de cada rodada ou de rotina agendada; a ausência de backup bem-sucedido DEVE ser reportada.
5. O manifesto DEVE ser um arquivo com hash bem definido, apto a receber carimbo do tempo externo no futuro (fora do P0).

## Requisito 10 — Relatório

**História:** Como leitor do relatório, quero um documento claro e fixo com a evidência, as limitações e a prova de integridade, para usar e arquivar.

**Critérios de aceite**

1. O sistema DEVE gerar um relatório (PDF e/ou HTML estático) a partir do EC e do modelo de relatório configurado.
2. O relatório DEVE conter: resposta às perguntas do EC (o quê, onde, quando, quanto, trajetória, em relação a quê, confiança, base), mapa e gráficos, método resumido, incerteza e limitações.
3. O relatório DEVE exibir o hash do EC e o identificador do registro de integridade.
4. O relatório DEVE sinalizar de forma visível quando os parâmetros forem provisórios e quando a execução estiver marcada como "não liberada para uso comercial".
5. O relatório NÃO DEVE usar linguagem de certificação ou de conformidade.

## Requisito 11 — Ferramenta interna de exploração

**História:** Como analista, cientista ou responsável de produto, quero explorar os resultados em uma tela local, para inspecionar pixels, séries e detecções.

**Critérios de aceite**

1. O sistema DEVE oferecer uma interface Streamlit local que leia os resultados de uma execução e mostre mapa de frações/mudanças, série temporal de um pixel e o baseline.
2. A interface DEVE rodar apenas localmente, sem exigir hospedagem.
3. Este requisito é de prioridade menor que os requisitos 1 a 10.

## Requisito 12 — Reprodutibilidade

**História:** Como verificador, quero repetir a execução e obter o mesmo resultado, para confiar na evidência.

**Critérios de aceite**

1. QUANDO o pipeline é executado duas vezes com os mesmos dados, parâmetros e versão do código ENTÃO o sistema DEVE produzir o mesmo EC canônico e, portanto, o mesmo hash.
2. O ambiente DEVE ser fixado por imagem Docker e lockfile de dependências; seeds e o número de threads de cálculo (BLAS/OpenMP, por exemplo `OMP_NUM_THREADS=1`) DEVEM ser fixados para eliminar não determinismo numérico, e o teste golden DEVE rodar sob essa mesma configuração.
3. Um teste golden, com um mini conjunto fixo de dados, DEVE falhar se o hash do EC mudar sem mudança intencional de método.

## Requisito 13 — Segurança e propriedade intelectual

**História:** Como responsável de produto, quero proteger o método e os dados, para preservar o ativo da empresa.

**Critérios de aceite**

1. O repositório DEVE ser privado e não conter dados, chaves nem senhas. DEVE existir um `.env.example` versionado sem valores e `data/` DEVE estar no `.gitignore`.
2. Os valores reais dos parâmetros científicos NÃO DEVEM aparecer em steering, specs, ADRs, testes ou exemplos; esses usam valores fictícios.
3. A integração contínua DEVE falhar se detectar segredos ou arquivos de `data/` adicionados ao Git (verificação automática de segredos/dados).
4. O sistema DEVE usar um bucket S3 (obrigatório no P0, ADR-011) com versionamento, criptografia em repouso, bloqueio de acesso público e política de acesso mínimo, provisionado por Terraform, guardando apenas artefatos definidos (saídas, parâmetros, EC, manifestos, backup do immudb) e nunca dados brutos nem segredos.
5. A credencial de acesso ao S3/AWS DEVE ser lida de variável de ambiente e nunca gravada em arquivo versionado.

## Requisito 14 — Qualidade e governança

**História:** Como analista técnico, quero testes e registros de decisão automáticos, para manter o projeto confiável e rastreável.

**Critérios de aceite**

1. O repositório DEVE ter testes de: mistura sintética do unmixing, golden de reprodutibilidade e validação dos arquivos de parâmetros.
2. A integração contínua DEVE executar testes e lint a cada push.
3. Toda decisão arquitetural nova ou alterada DEVE gerar um ADR em `docs/adr/` e uma linha no `docs/decision-log.md`.

---

## Pontos em aberto (dependem de terceiros)

**Para a Angela**

1. Qual sensor/coleção do BDC e quais bandas os parâmetros assumem?
2. Quais endmembers e como são escolhidos para uma fazenda específica?
3. O unmixing roda por pixel ou aceita agregar antes?
4. Qual índice de degradação e quais limiares definem cada nível?
5. Quantos anos de histórico o baseline exige?
6. Como tratar nuvem, sombra e água?
7. Como validar o resultado (dados de campo, imagens de alta resolução)?

**Para o Alexandre**

1. Quais clientes são mais prováveis e que formato de relatório cada um esperaria?
2. Qual é o território piloto (qual fazenda, qual área em hectares)?

**Para a equipe**

1. ~~O S3 entra já no P0 ou começa sem ele?~~ **Resolvido:** o S3 versionado entra no P0 como obrigatório (ADR-011).
