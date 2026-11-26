from pydantic import BaseModel, Field, field_validator
from typing import Optional


class SolicitudAnalisis(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    texto: Optional[str] = Field(default=None, max_length=3000)
    autoriza_consulta_externa: bool = False

    @field_validator("url")
    @classmethod
    def url_no_vacia(cls, value):
        if not value.strip():
            raise ValueError("La URL no puede estar vacía.")
        return value


class RespuestaAnalisis(BaseModel):
    url: str
    probabilidad: float = Field(ge=0, le=100)
    nivel: str
    evidencias: dict
    senales_texto: list[str]
    reputacion: dict
    mensaje: str
