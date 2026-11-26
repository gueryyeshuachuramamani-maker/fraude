from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agente import analizar
from reputacion import crear_proveedor
from backend.schemas import SolicitudAnalisis, RespuestaAnalisis
from backend.config import origenes_permitidos
import os

app = FastAPI(title="FraudGuard AI API", version="1.0.0",
              description="API de análisis preventivo de URLs.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def inicio():
    return {"nombre": "FraudGuard AI", "estado": "activo"}


@app.get("/api/salud")
def salud():
    return {"estado": "ok"}


@app.post("/api/analizar", response_model=RespuestaAnalisis)
def analizar_endpoint(solicitud: SolicitudAnalisis):
    modo = os.getenv("MODO_REPUTACION", "simulada").lower()
    reputacion = None
    fuente = "no_consultada"
    estado = "desconocido"

    # La consulta externa solo se realiza con consentimiento explícito.
    if modo == "virustotal" and solicitud.autoriza_consulta_externa:
        proveedor = crear_proveedor("virustotal")
        resultado_rep = proveedor.consultar(solicitud.url.strip())
        reputacion = resultado_rep.evidencia_R
        fuente = resultado_rep.fuente
        estado = resultado_rep.estado

    resultado = analizar(solicitud.url, solicitud.texto, reputacion)
    if "error" in resultado:
        raise HTTPException(status_code=422, detail=resultado["error"])

    return {
        "url": resultado["url"],
        "probabilidad": round(resultado["p_fraude"] * 100, 2),
        "nivel": resultado["nivel"],
        "evidencias": resultado["evidencias"],
        "senales_texto": resultado["senales_texto"],
        "reputacion": {"estado": estado, "fuente": fuente},
        "mensaje": resultado["mensaje"],
    }
