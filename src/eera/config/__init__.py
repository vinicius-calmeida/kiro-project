"""Modelos pydantic e carregamento das configurações do pipeline EERA.

Ponto de entrada do módulo ``config``: valida território, parâmetros
científicos e relatório antes de qualquer execução (ver ADR-010).
"""

from .loader import ConfigInvalida, carregar_config
from .modelos import ConfigExecucao
from .parametros_cientificos import (
    Baseline,
    Indice,
    Limiares,
    Mascaras,
    ParametrosCientificos,
    StatusParametros,
)
from .relatorio import ConfigRelatorio
from .territorio import Periodo, Territorio

__all__ = [
    "Baseline",
    "ConfigExecucao",
    "ConfigInvalida",
    "ConfigRelatorio",
    "Indice",
    "Limiares",
    "Mascaras",
    "ParametrosCientificos",
    "Periodo",
    "StatusParametros",
    "Territorio",
    "carregar_config",
]
