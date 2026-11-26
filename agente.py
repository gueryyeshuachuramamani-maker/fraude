"""Agente FraudGuard AI: percepción -> inferencia -> decisión."""
from urllib.parse import urlsplit
from analizador_url import dominio_sospechoso, estructura_anomala
from analizador_texto import contexto_manipulador
from red_bayesiana import p_fraude
from validador_url import validar_url

UMBRAL_MEDIO = 0.30
UMBRAL_ALTO = 0.70


def decidir_riesgo(probabilidad, evidencias):
    """Clasifica P(fraude), expresada entre 0 y 1."""
    if isinstance(probabilidad, bool) or not isinstance(probabilidad, (int, float)):
        raise ValueError("La probabilidad debe ser numérica.")
    if not 0 <= probabilidad <= 1:
        raise ValueError("La probabilidad debe estar entre 0 y 1.")

    reputacion = evidencias.get("R")
    contexto = evidencias.get("C")

    if probabilidad >= UMBRAL_ALTO:
        nivel = "ALTO"
        mensaje = "Se detectaron señales importantes de fraude. No abras el enlace ni introduzcas información personal."
    elif reputacion is None and contexto is None:
        nivel = "INSUFICIENTE"
        mensaje = "No hay información suficiente para valorar el enlace. No se puede considerar seguro."
    elif reputacion is None:
        nivel = "NO VERIFICADO"
        mensaje = "No se pudo comprobar la reputación. El resultado es provisional; evita introducir datos sensibles."
    elif probabilidad >= UMBRAL_MEDIO:
        nivel = "MEDIO"
        mensaje = "Se encontraron señales de riesgo. Verifica el enlace por otro medio antes de continuar."
    else:
        nivel = "BAJO"
        mensaje = "El modelo estima un riesgo bajo con la evidencia disponible. Esto no garantiza seguridad."
    return {"nivel": nivel, "mensaje": mensaje}


def decidir(p, ev):
    """Compatibilidad con el nombre de función anterior."""
    resultado = decidir_riesgo(p, ev)
    return resultado["nivel"], resultado["mensaje"]


def analizar(url, texto=None, reputacion=None):
    valida, resultado = validar_url(url)
    if not valida:
        return {"error": resultado}

    if texto is not None and not isinstance(texto, str):
        return {"error": "El texto del mensaje debe ser texto."}

    host = urlsplit(resultado).hostname
    c, senales = contexto_manipulador(texto)
    ev = {
        "D": dominio_sospechoso(host),
        "R": reputacion,
        "U": estructura_anomala(resultado),
        "C": c,
    }
    p = p_fraude(ev)
    nivel, msg = decidir(p, ev)
    return {
        "url": resultado,
        "evidencias": ev,
        "senales_texto": senales,
        "p_fraude": p,
        "nivel": nivel,
        "mensaje": msg,
    }
