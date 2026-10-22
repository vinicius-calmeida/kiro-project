# Visão do produto — EERA

## O que é o projeto

Startup em estruturação que produz e comercializa **evidências ambientais** para perguntas relevantes de mercados regulados. A arquitetura de referência se chama **EERA (Environmental Evidence Reference Architecture)**.

Pergunta orientadora da empresa:

> Que pergunta relevante de um mercado regulado precisa ser respondida por uma evidência ambiental que hoje é difícil de produzir, verificar ou auditar?

A empresa transforma observações ambientais em evidências científicas **estruturadas, rastreáveis, reproduzíveis e verificáveis**. Ela **não** é: empresa de sensoriamento remoto, de ESG, de dashboards, consultoria ambiental tradicional, certificadora ou auditora regulatória.

## Unidade de produto: Evidence Card (EC)

O EC é a menor unidade reutilizável de conhecimento científico aplicado capaz de responder uma pergunta específica. Ele encapsula pergunta, dados, método, resultados, validação, incerteza e rastreabilidade.

Cadeia de produção da evidência: dado → informação → feature → inferência → evidência → Evidence Card → resposta → produto.

Regra de ouro: um dado não é automaticamente uma evidência; uma feature não é automaticamente uma conclusão; e um modelo não substitui a demonstração da validade da inferência.

## Escopo do P0 (primeiro MVP)

**EC-001 — Environmental Change Detection.** Pergunta operacional:

> O território analisado apresentou uma mudança ambiental relevante em relação ao seu comportamento histórico esperado e, em caso positivo, onde, quando, com qual magnitude, trajetória e nível de confiança essa mudança ocorreu?

O EC-001 responde **o que mudou**, sem atribuir causa que os dados ainda não sustentem.

Estrutura mínima da resposta: o quê, onde, quando, quanto, qual trajetória, em relação a quê (baseline), com qual confiança, com base em quê (dados, método, features).

Premissas do P0:

- Território piloto: **uma fazenda**.
- Precisão desejada: **pixel**.
- Domínio científico inicial: dinâmica vegetal/biomassa e solo/degradação, via desmistura espectral (unmixing).
- Clientes-alvo ainda **indefinidos** (podem ser vários). O sistema deve ser orientado a configuração: território, período, parâmetros científicos e modelo de relatório são entradas; a lógica não conhece o cliente.
- Primeiro produto comercial: uma *Environmental Evidence Assessment* (serviço especializado com EC, relatório, rastreabilidade, integridade, limitações e nível de confiança). Não é SaaS.

Fora do P0: SCADA, historiadores industriais, IoT, drones, edge computing, integrações corporativas, plataforma completa, múltiplos setores, grande catálogo de ECs, IA genérica.

## Mercados considerados (contexto, não implementar agora)

Green Finance / Mercado de Capitais (primeiro ambiente de validação comercial) e Saneamento (perdas de água). A tecnologia do P0 não deve assumir nenhum dos dois.

## Regras de linguagem e de produto

- Nunca afirmar que a empresa "certifica" ou "comprova conformidade". Posicionamento correto: produzir a evidência ambiental necessária para subsidiar avaliação, divulgação, estruturação e acompanhamento, deixando explícitas as condições de validade e as limitações científicas.
- Todo resultado carrega incerteza, nível de confiança e limitações.
- Nenhum dado entra no P0 sem função explícita na resposta do EC.
- Não construir o que ainda não se sabe se alguém compra: pergunta → evidência → cliente → pagamento; só depois automação, escala e plataforma.

## Equipe

- **Angela**: ciência, sensoriamento remoto, parâmetros do unmixing, baseline, validação. Pouco disponível no dia a dia; é a dona dos parâmetros científicos.
- **Alexandre**: mercado, produto, cliente, governança e comercial.
- **Vinícius**: engenharia e infraestrutura.

## Glossário mínimo

- **Feature**: variável derivada dos dados (índice, fração subpixel, métrica temporal, tendência, anomalia).
- **Unmixing espectral**: estima a contribuição de componentes (endmembers) dentro de um pixel.
- **Endmember**: assinatura espectral de um componente puro (vegetação, solo, sombra etc.).
- **Baseline**: comportamento ambiental esperado, usado como referência para identificar desvios.
- **Rastreabilidade**: reconstruir origem, transformação e uso de uma informação.
- **Auditabilidade**: uma terceira parte consegue verificar origem, método, integridade e resultados.
- **Reprodutibilidade**: repetir o processo sob condições equivalentes e obter resultados compatíveis.
- **BDC**: Brazil Data Cube (INPE), fonte de dados de observação da Terra.
- **immudb**: banco imutável usado como camada de integridade; guarda hashes, não dados.
