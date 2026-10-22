"""Modelo pydantic da configuração de relatório (``configs/relatorio/``).

O pipeline é orientado a configuração: o modelo de relatório é um arquivo por
cliente. A lógica não conhece o cliente (ver product.md / ADR-007).
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ConfigRelatorio(BaseModel):
    """Raiz do arquivo de modelo de relatório."""

    model_config = ConfigDict(extra="forbid")

    titulo: str = Field(..., min_length=1)
    idioma: str = Field("pt-BR", min_length=2)
    secoes: list[str] = Field(..., min_length=1)
    logotipo: Path | None = None
    texto_limitacoes: str = Field(..., min_length=1)
