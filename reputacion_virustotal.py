"""Consulta de URL en VirusTotal API v3. No envía URLs automáticamente."""
import base64
import os
import requests
from reputacion_simulada import ResultadoReputacion


class ReputacionVirusTotal:
    ENDPOINT = "https://www.virustotal.com/api/v3/urls/{}"

    def __init__(self, api_key=None, timeout=12):
        self.api_key = api_key or os.getenv("VIRUSTOTAL_API_KEY")
        self.timeout = timeout

    def consultar(self, url):
        if not self.api_key:
            return ResultadoReputacion("desconocido", "virustotal", False,
                                       mensaje="No está configurada la clave API.")
        encoded = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
        try:
            r = requests.get(self.ENDPOINT.format(encoded),
                             headers={"x-apikey": self.api_key}, timeout=self.timeout)
            if r.status_code == 404:
                return ResultadoReputacion("desconocido", "virustotal", False,
                                           mensaje="No existe un informe disponible.")
            if r.status_code in (401, 403):
                return ResultadoReputacion("desconocido", "virustotal", False,
                                           mensaje="La clave API no fue aceptada.")
            if r.status_code == 429:
                return ResultadoReputacion("desconocido", "virustotal", False,
                                           mensaje="Se alcanzó el límite de consultas.")
            r.raise_for_status()
            stats = r.json()["data"]["attributes"]["last_analysis_stats"]
            mal = int(stats.get("malicious", 0))
            sus = int(stats.get("suspicious", 0))
            if mal > 0:
                estado, msg = "reportado", "La URL tiene detecciones maliciosas."
            elif sus > 0:
                estado, msg = "desconocido", "Hay detecciones sospechosas; requiere revisión."
            else:
                estado, msg = "no_reportado", "El informe no muestra detecciones maliciosas."
            return ResultadoReputacion(estado, "virustotal", True, mal, sus, msg)
        except (requests.RequestException, ValueError, KeyError, TypeError):
            return ResultadoReputacion("desconocido", "virustotal", False,
                                       mensaje="No se pudo obtener un informe válido.")
