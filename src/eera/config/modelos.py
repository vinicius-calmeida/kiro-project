"""Agregação da configuração de uma execução e travas de liberação.

``ConfigExecucao`` reúne território, parâmetros científicos e relatório e
expõe, num único lugar, se a execução pode ser entregue comercialmente.

Travas de uso comercial (ver Req. 2.7, Req. 7.7 e ADR-001/ADR-010):

- parâmetros provisórios  -> não liberado para uso comercial;
- termos do BDC não confirmados -> não liberado para uso comercial.

O passo de ``ec`` consome ``uso_comercial_liberado`` para marcar o EC e o
relatório como "somente desenvolvimento/validação" quando for o caso.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .parametros_cientificos import ParametrosCientificos
from .relatorio import ConfigRelatorio
from .territorio import Territorio


class ConfigExecucao(BaseModel):
    """Configuração completa e validada de uma rodada."""

    model_config = ConfigDict(extra="forbid")

    territorio: Territorio
    parametros: ParametrosCientificos
    relatorio: ConfigRelatorio
    # Confirmação dos termos de uso comercial do BDC (ADR-001, ponto em aberto).
    # Default conservador: até confirmar, nada é liberado para uso comercial.
    bdc_uso_comercial_confirmado: bool = False

    @property
    def uso_comercial_liberado(self) -> bool:
        """Só libera entrega comercial se parâmetros aprovados E termos do BDC ok."""
        return (
            self.parametros.liberado_para_uso_comercial
            and self.bdc_uso_comercial_confirmado
        )

    @property
    def motivo_bloqueio_comercial(self) -> str | None:
        """Texto curto explicando por que a execução não é liberável (ou None)."""
        motivos: list[str] = []
        if not self.parametros.liberado_para_uso_comercial:
            motivos.append("parâmetros científicos provisórios (não aprovados pela Angela)")
        if not self.bdc_uso_comercial_confirmado:
            motivos.append("termos de uso comercial do BDC não confirmados")
        return "; ".join(motivos) if motivos else None
