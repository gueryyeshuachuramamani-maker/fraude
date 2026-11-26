"""Módulo de percepción 2: señales de manipulación en el mensaje (patrones de texto)."""
import re, unicodedata

PATRONES = {
    "urgencia": r"urgente|ultim[oa]s? (hora|aviso|oportunidad)|en (las )?pr[oó]ximas? \d+ horas|expira|vence hoy|inmediatamente|ahora mismo",
    "premio": r"ganaste|ganador|premio|sorteo|regalo gratis|felicidades|has sido seleccionad",
    "amenaza": r"cuenta (ser[aá] )?(bloquead|suspendid|cancelad)|bloqueo|suspensi[oó]n|sancion|multa|denuncia",
    "credenciales": r"c[oó]digo de (verificaci[oó]n|seguridad|6 d[ií]gitos)|contrase[nñ]a|clave|pin\b|datos (personales|bancarios)|verifica (tu|su) (cuenta|identidad)|confirma (tu|su)",
    "dinero": r"transferencia|deposit[ao]|pago pendiente|reembolso|ganancia[s]? (r[aá]pida|garantizad)|invierte",
}


def _norm(t: str) -> str:
    return unicodedata.normalize("NFC", t.lower())


def contexto_manipulador(texto):
    """C: True si hay >=2 categorías de manipulación; None si no hay texto."""
    if texto is None or not texto.strip():
        return None, []
    t = _norm(texto)
    hallados = [k for k, p in PATRONES.items() if re.search(p, t)]
    return len(hallados) >= 2, hallados
