import os

from agent.providers.base import ProveedorWhatsApp


def obtener_proveedor() -> ProveedorWhatsApp:
    proveedor = os.getenv("WHATSAPP_PROVIDER", "whapi").lower()
    if proveedor == "whapi":
        from agent.providers.whapi import ProveedorWhapi
        return ProveedorWhapi()
    elif proveedor == "meta":
        from agent.providers.meta import ProveedorMeta
        return ProveedorMeta()
    else:
        raise ValueError(f"Proveedor desconocido: {proveedor}")
