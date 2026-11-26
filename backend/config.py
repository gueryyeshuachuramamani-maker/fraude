import os


def origenes_permitidos():
    valor = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    return [x.strip() for x in valor.split(",") if x.strip()]
