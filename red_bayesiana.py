"""Módulo de razonamiento: red bayesiana tipo Bayes ingenuo (F -> D, R, U, C).
pgmpy no está instalado en el entorno de pruebas; la inferencia se implementa
de forma directa (equivale a eliminación de variables en esta estructura)."""
from math import prod

P_F = {"si": 0.10, "no": 0.90}
# P(E = positiva | F)  -- valores hipotéticos del documento (sección IV.C)
CPT = {
    "D": {"si": 0.70, "no": 0.05},
    "R": {"si": 0.80, "no": 0.02},
    "U": {"si": 0.60, "no": 0.10},
    "C": {"si": 0.75, "no": 0.10},
}


def p_fraude(evidencias: dict, desconocida_como_negativa=False) -> float:
    """P(F=Sí | e). evidencias: {'D': True/False/None, ...}. None = desconocida (se omite)."""
    pesos = {}
    for f in ("si", "no"):
        w = P_F[f]
        for nodo, cpt in CPT.items():
            v = evidencias.get(nodo)
            if v is None:
                if not desconocida_como_negativa:
                    continue          # marginalización: se omite la evidencia
                v = False
            w *= cpt[f] if v else (1 - cpt[f])
        pesos[f] = w
    return pesos["si"] / (pesos["si"] + pesos["no"])
