"""Módulo de percepción 1: análisis de la URL (código convencional, sin IA)."""
from urllib.parse import urlparse
import re

MARCAS = ["whatsapp", "facebook", "telegram", "instagram", "google", "paypal",
          "netflix", "amazon", "microsoft", "tiktok", "mercadolibre", "bancounion",
          "bnb", "bancosol", "tigo", "entel", "viva"]
TLD_RIESGO = {"xyz", "top", "click", "icu", "buzz", "live", "shop", "online", "site", "vip", "cc", "tk"}
ACORTADORES = {"bit.ly", "tinyurl.com", "cutt.ly", "is.gd", "t.co", "rb.gy"}
TLD_COMPUESTOS = {"com.bo", "com.ar", "com.mx", "co.uk", "com.br", "gob.bo", "org.bo"}
SUSTITUCION = str.maketrans("01358", "olesb")  # 0->o, 1->l, 3->e, 5->s(~), 8->b


def _lev(a: str, b: str) -> int:
    """Distancia de Levenshtein."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def separar_dominio(host: str):
    """Devuelve (subdominios, dominio_registrable, tld) sin depender de tldextract."""
    partes = host.lower().split(".")
    if len(partes) >= 3 and ".".join(partes[-2:]) in TLD_COMPUESTOS:
        return partes[:-3], partes[-3], ".".join(partes[-2:])
    if len(partes) >= 2:
        return partes[:-2], partes[-2], partes[-1]
    return [], host, ""


def dominio_sospechoso(host: str) -> bool:
    """D: imita una marca conocida sin ser el dominio oficial."""
    subs, nombre, tld = separar_dominio(host)
    base = nombre.translate(SUSTITUCION)
    for m in MARCAS:
        if nombre == m:                       # dominio oficial (p. ej. google.com)
            continue
        if m in nombre or m in base:          # marca dentro del nombre: paypal-seguro
            return True
        if len(m) >= 5 and 0 < _lev(nombre, m) <= 1:   # error tipográfico: faceboook
            return True
        if any(m in s for s in subs) and nombre != m:  # marca en subdominio ajeno
            return True
    return False


def estructura_anomala(url: str) -> bool:
    """U: dos o más rasgos anómalos en la URL."""
    p = urlparse(url)
    host = p.hostname or ""
    subs, nombre, tld = separar_dominio(host)
    rasgos = 0
    rasgos += bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))      # IP en lugar de dominio
    rasgos += "@" in url.split("?")[0]                                 # usuario@host
    rasgos += host.startswith("xn--") or ".xn--" in host               # punycode
    rasgos += len(subs) >= 3                                           # muchos subdominios
    rasgos += host.count("-") >= 2                                     # muchos guiones
    rasgos += tld in TLD_RIESGO                                        # TLD frecuente en abuso
    rasgos += len(url) > 90                                            # URL muy larga
    rasgos += host in ACORTADORES                                      # acortador (destino oculto)
    rasgos += p.scheme == "http"                                       # sin cifrado
    rasgos += bool(re.search(r"(login|verif|segur|clave|codigo|cuenta|update|premio)", p.path.lower()))
    return rasgos >= 2
