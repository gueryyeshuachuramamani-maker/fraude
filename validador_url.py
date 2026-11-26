"""Validación sintáctica de URLs; no determina si un sitio es seguro."""
from urllib.parse import urlsplit
import ipaddress
import re

MAX_URL_LENGTH = 2048
_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def validar_url(valor):
    if not isinstance(valor, str):
        return False, "La dirección debe ser texto."
    url = valor.strip()
    if not url:
        return False, "Escribe una dirección web."
    if len(url) > MAX_URL_LENGTH:
        return False, f"La dirección supera {MAX_URL_LENGTH} caracteres."
    if any(ord(c) < 32 or ord(c) == 127 for c in url) or any(c.isspace() for c in url):
        return False, "La dirección contiene espacios o caracteres no permitidos."
    if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", url):
        return False, "Incluye http:// o https:// al inicio."
    try:
        p = urlsplit(url)
        if p.scheme.lower() not in ("http", "https"):
            return False, "Solo se permiten direcciones HTTP o HTTPS."
        if not p.hostname:
            return False, "No se encontró un dominio o dirección IP."
        if p.username is not None or p.password is not None:
            return False, "No se permiten credenciales dentro de la dirección."
        _ = p.port  # fuerza validación del puerto
        host = p.hostname
        try:
            ipaddress.ip_address(host)
        except ValueError:
            host_ascii = host.encode("idna").decode("ascii")
            if len(host_ascii) > 253:
                return False, "El dominio es demasiado largo."
            labels = host_ascii.rstrip(".").split(".")
            if not labels or any(not _LABEL.fullmatch(x) for x in labels):
                return False, "El dominio tiene un formato inválido."
        return True, url
    except (ValueError, UnicodeError):
        return False, "La dirección o el puerto tienen un formato inválido."
