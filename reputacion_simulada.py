"""Proveedor simulado. No consulta internet y no afirma verificar un dominio."""
from dataclasses import dataclass


@dataclass
class ResultadoReputacion:
    estado: str
    fuente: str
    verificada: bool
    malicious: int | None = None
    suspicious: int | None = None
    mensaje: str = ""

    @property
    def evidencia_R(self):
        return True if self.estado == "reportado" else False if self.estado == "no_reportado" else None


class ReputacionSimulada:
    def consultar(self, url):
        return ResultadoReputacion(
            estado="desconocido",
            fuente="simulada",
            verificada=False,
            mensaje="Modo de demostración: no se consultó una fuente externa."
        )
