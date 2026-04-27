from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from fastapi import Request


@dataclass
class MensajeEntrante:
    telefono: str
    texto: str
    mensaje_id: str
    es_propio: bool
    tipo: str = "text"


class ProveedorWhatsApp(ABC):

    @abstractmethod
    async def parsear_webhook(self, request: Request) -> list[MensajeEntrante]:
        """Convierte el payload del webhook a una lista de mensajes normalizados."""

    @abstractmethod
    async def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        """Envía un mensaje de texto al número indicado. Retorna True si fue exitoso."""

    async def validar_webhook(self, request: Request) -> dict | int | None:
        """Validación opcional del webhook (usado por Meta). Retorna respuesta o None."""
        return None
