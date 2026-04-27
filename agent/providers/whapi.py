import os

import httpx
from fastapi import Request

from agent.providers.base import MensajeEntrante, ProveedorWhatsApp

WHAPI_URL = "https://gate.whapi.cloud/messages/text"


class ProveedorWhapi(ProveedorWhatsApp):

    def __init__(self):
        self.token = os.getenv("WHAPI_TOKEN", "")

    async def parsear_webhook(self, request: Request) -> list[MensajeEntrante]:
        try:
            body = await request.json()
        except Exception:
            return []

        mensajes = []
        for msg in body.get("messages", []):
            tipo = msg.get("type", "text")
            es_propio = msg.get("from_me", False)
            telefono = msg.get("chat_id", msg.get("from", ""))
            mensaje_id = msg.get("id", "")

            if tipo == "text":
                texto = msg.get("text", {}).get("body", "")
            else:
                texto = f"[{tipo}]"

            if telefono and mensaje_id:
                mensajes.append(MensajeEntrante(
                    telefono=telefono,
                    texto=texto,
                    mensaje_id=mensaje_id,
                    es_propio=es_propio,
                    tipo=tipo,
                ))

        return mensajes

    async def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"to": telefono, "body": mensaje}

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(WHAPI_URL, json=payload, headers=headers)
                return resp.status_code == 200
            except Exception:
                return False
