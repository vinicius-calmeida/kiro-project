"""Modelo pydantic da configuração de território (``configs/territorio/``).

Território = qual fazenda, qual geometria, qual período de análise. É entrada
do passo de coleta. Sem segredo nem valor científico aqui.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Periodo(BaseModel):
    """Intervalo fechado de análise."""

    model_config = ConfigDict(extra="forbid")

    inicio: date
    fim: date

    @model_validator(mode="after")
    def _ordem(self) -> "Periodo":
        if self.fim <= self.inicio:
            raise ValueError("periodo.fim deve ser posterior a periodo.inicio")
        return self


class Territorio(BaseModel):
    """Raiz do arquivo de território."""

    model_config = ConfigDict(extra="forbid")

    nome: str = Field(..., min_length=1)
    geometria: Path = Field(..., description="Caminho do GeoJSON do polígono da fazenda")
    periodo_analise: Periodo
