import os

import httpx
from fastapi import Request
from fastapi.responses import PlainTextResponse

from agent.providers.base import MensajeEntrante, ProveedorWhatsApp


class ProveedorMeta(ProveedorWhatsApp):

    def __init__(self):
        self.access_token = os.getenv("META_ACCESS_TOKEN", "")
        self.phone_number_id = os.getenv("META_PHONE_NUMBER_ID", "")
        self.verify_token = os.getenv("META_VERIFY_TOKEN", "conduees-verify")

    async def validar_webhook(self, request: Request) -> PlainTextResponse | int | None:
        params = request.query_params
        if params.get("hub.verify_token") == self.verify_token:
            return PlainTextResponse(params.get("hub.challenge", ""))
        return 403

    async def parsear_webhook(self, request: Request) -> list[MensajeEntrante]:
        try:
            body = await request.json()
        except Exception:
            return []

        mensajes = []
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                valor = change.get("value", {})
                for msg in valor.get("messages", []):
                    tipo = msg.get("type", "text")
                    telefono = msg.get("from", "")
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
                            es_propio=False,
                            tipo=tipo,
                        ))

        return mensajes

    async def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": telefono,
            "type": "text",
            "text": {"body": mensaje},
        }

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                return resp.status_code == 200
            except Exception:
                return False
