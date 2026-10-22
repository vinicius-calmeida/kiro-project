# ADR-010 — Parâmetros científicos como configuração versionada

- **Status:** Aceita
- **Data:** 2026-10-21

## Contexto

A Angela é a dona do julgamento científico (quais endmembers, quais bandas, qual índice, quais limiares de degradação) e tem pouca disponibilidade no dia a dia. A equipe de engenharia consegue implementar todo o resto. O blueprint exige preservar versão dos métodos e parâmetros e proteger o conhecimento científico como ativo.

## Decisão

O código **não contém nenhum número científico**. Tudo o que depende do julgamento da Angela entra por **um arquivo de configuração versionado** (YAML validado por pydantic), contendo no mínimo:

- componentes (endmembers) e suas assinaturas espectrais por banda;
- bandas utilizadas e fatores de escala;
- índice de degradação e sua definição;
- janela histórica e regras do baseline;
- limiares que transformam fração/índice em nível de degradação e em mudança relevante;
- regras de máscara (nuvem, sombra, água).

Durante o desenvolvimento, a equipe usa **valores fictícios ou de literatura, marcados como provisórios**. A Angela revisa e preenche o arquivo sem mexer em código. O **hash desse arquivo** entra no manifesto e no EC.

## Consequências

- Desenvolvimento e testes avançam sem depender da Angela; a fronteira entre engenharia e ciência é explícita.
- Reprodutibilidade: a versão do método fica atrelada ao hash do arquivo.
- O arquivo tem valor de propriedade intelectual: repositório privado, acesso mínimo, e **valores reais fora de steering, specs e prompts**.
- O EC deve registrar se os parâmetros usados são **provisórios** ou **aprovados** pela Angela.
