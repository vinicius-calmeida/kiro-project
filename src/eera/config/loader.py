"""Carregamento e validação da configuração (falha rápida, mensagem por campo).

Fluxo: lê os três YAML -> valida com pydantic -> devolve ``ConfigExecucao``.
Nada de acesso a dados externos acontece aqui; isso roda ANTES da coleta
(ver Req. 1.1). Em erro, levanta ``ConfigInvalida`` com os campos ofensores.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from .modelos import ConfigExecucao
from .parametros_cientificos import ParametrosCientificos
from .relatorio import ConfigRelatorio
from .territorio import Territorio


class ConfigInvalida(Exception):
    """Erro de configuração legível, com o caminho do arquivo e os campos."""


def _ler_yaml(caminho: Path) -> dict[str, Any]:
    caminho = Path(caminho)
    if not caminho.exists():
        raise ConfigInvalida(f"arquivo de configuração não encontrado: {caminho}")
    try:
        dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # YAML malformado
        raise ConfigInvalida(f"YAML inválido em {caminho}: {exc}") from exc
    if not isinstance(dados, dict):
        raise ConfigInvalida(f"{caminho} deve conter um mapeamento no topo")
    return dados


def _validar(modelo: type[BaseModel], dados: dict[str, Any], caminho: Path) -> Any:
    try:
        return modelo.model_validate(dados)
    except ValidationError as exc:
        linhas = [
            f"  - {'.'.join(str(p) for p in e['loc'])}: {e['msg']}"
            for e in exc.errors()
        ]
        raise ConfigInvalida(
            f"configuração inválida em {caminho}:\n" + "\n".join(linhas)
        ) from exc


def carregar_config(
    territorio_path: Path,
    parametros_path: Path,
    relatorio_path: Path,
    *,
    bdc_uso_comercial_confirmado: bool = False,
) -> ConfigExecucao:
    """Carrega e valida as três configs e devolve a execução pronta.

    Levanta ``ConfigInvalida`` no primeiro arquivo com problema. Aceita
    ``str`` ou ``Path`` nos caminhos.
    """
    territorio_path = Path(territorio_path)
    parametros_path = Path(parametros_path)
    relatorio_path = Path(relatorio_path)

    territorio = _validar(Territorio, _ler_yaml(territorio_path), territorio_path)
    parametros = _validar(
        ParametrosCientificos, _ler_yaml(parametros_path), parametros_path
    )
    relatorio = _validar(ConfigRelatorio, _ler_yaml(relatorio_path), relatorio_path)

    return ConfigExecucao(
        territorio=territorio,
        parametros=parametros,
        relatorio=relatorio,
        bdc_uso_comercial_confirmado=bdc_uso_comercial_confirmado,
    )
