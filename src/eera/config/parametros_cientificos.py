"""Modelos pydantic dos parâmetros científicos (arquivo da Angela).

Regras de domínio (ver ADR-010 e steering/tech.md):

- NENHUM valor científico mora no código. Tudo (endmembers, bandas, índice,
  janela do baseline, limiares, máscaras) vem do YAML validado aqui.
- Os valores reais da Angela nunca entram em steering, specs, ADRs, testes
  ou exemplos; exemplos usam valores fictícios.
- Enquanto a Angela não aprova, ``status`` fica ``provisorio`` e o EC gerado
  é marcado "somente desenvolvimento/validação" (ver ADR-010 / Req. 7).

Este módulo só valida e falha rápido com mensagem por campo. Ele NÃO executa
nenhum passo do pipeline (coleta, unmixing etc.).
"""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StatusParametros(str, Enum):
    """Maturidade dos parâmetros científicos."""

    PROVISORIO = "provisorio"
    APROVADO = "aprovado"


class Baseline(BaseModel):
    """Janela histórica e regra mínima de observações do baseline."""

    model_config = ConfigDict(extra="forbid")

    janela_inicio: date
    janela_fim: date
    min_obs: int = Field(..., gt=0, description="Mínimo de observações por pixel")

    @model_validator(mode="after")
    def _janela_coerente(self) -> "Baseline":
        if self.janela_fim <= self.janela_inicio:
            raise ValueError(
                "baseline.janela_fim deve ser posterior a baseline.janela_inicio"
            )
        return self


class Indice(BaseModel):
    """Índice derivado das frações (ex.: índice de degradação)."""

    model_config = ConfigDict(extra="forbid")

    nome: str = Field(..., min_length=1)
    definicao: str = Field(..., min_length=1)


class Limiares(BaseModel):
    """Limiares que transformam índice/fração em nível de mudança.

    Os valores são científicos (vêm do YAML), mas a *relação de ordem* entre
    eles é uma invariante estrutural e pode ser verificada aqui.
    """

    model_config = ConfigDict(extra="forbid")

    baixo: float = Field(..., ge=0.0)
    medio: float = Field(..., ge=0.0)
    alto: float = Field(..., ge=0.0)

    @model_validator(mode="after")
    def _ordem_crescente(self) -> "Limiares":
        if not (self.baixo < self.medio < self.alto):
            raise ValueError(
                "limiares devem obedecer baixo < medio < alto "
                f"(recebido: baixo={self.baixo}, medio={self.medio}, alto={self.alto})"
            )
        return self


class Mascaras(BaseModel):
    """Quais máscaras aplicar e o limiar de contaminação (ADR-002 / C.7).

    O ``limiar_contaminacao`` é um parâmetro científico: decide quando um pixel
    parcialmente coberto conta como mascarado. Fica aqui, nunca no código.
    """

    model_config = ConfigDict(extra="forbid")

    nuvem: bool = True
    sombra: bool = True
    agua: bool = True
    limiar_contaminacao: float = Field(..., ge=0.0, le=1.0)


class ParametrosCientificos(BaseModel):
    """Raiz do arquivo de parâmetros científicos (``configs/parametros_cientificos/``).

    A assinatura espectral de cada endmember deve ter exatamente um valor por
    banda declarada em ``bandas`` — invariante verificada abaixo.
    """

    model_config = ConfigDict(extra="forbid")

    status: StatusParametros
    aprovado_por: str | None = None
    colecao: str = Field(..., min_length=1, description="Coleção/sensor do BDC")
    bandas: list[str] = Field(..., min_length=1)
    endmembers: dict[str, list[float]] = Field(..., min_length=1)
    baseline: Baseline
    indice: Indice
    limiares: Limiares
    mascaras: Mascaras
    # Precisão de arredondamento usada pela serialização canônica do EC e pelo
    # hash lógico das tabelas (ver design: determinismo do hash). Mora aqui
    # porque é parte do método versionado.
    precisao_decimal: int = Field(6, ge=0, le=12)

    @model_validator(mode="after")
    def _bandas_unicas(self) -> "ParametrosCientificos":
        if len(set(self.bandas)) != len(self.bandas):
            raise ValueError("bandas não podem conter nomes repetidos")
        return self

    @model_validator(mode="after")
    def _endmembers_cobrem_todas_as_bandas(self) -> "ParametrosCientificos":
        n = len(self.bandas)
        for nome, assinatura in self.endmembers.items():
            if len(assinatura) != n:
                raise ValueError(
                    f"endmember '{nome}' tem {len(assinatura)} valores, "
                    f"esperado {n} (um por banda em 'bandas')"
                )
        return self

    @model_validator(mode="after")
    def _aprovado_exige_responsavel(self) -> "ParametrosCientificos":
        if self.status is StatusParametros.APROVADO and not self.aprovado_por:
            raise ValueError(
                "status 'aprovado' exige 'aprovado_por' preenchido (a Angela)"
            )
        return self

    @property
    def liberado_para_uso_comercial(self) -> bool:
        """Parâmetros provisórios nunca liberam entrega comercial (ADR-010)."""
        return self.status is StatusParametros.APROVADO
