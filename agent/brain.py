from pathlib import Path

import yaml
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

_prompts: dict = {}


def _cargar_prompts() -> dict:
    global _prompts
    if not _prompts:
        path = Path(__file__).parent.parent / "config" / "prompts.yaml"
        with open(path, encoding="utf-8") as f:
            _prompts = yaml.safe_load(f)
    return _prompts


async def generar_respuesta(mensaje: str, historial: list[dict]) -> str:
    prompts = _cargar_prompts()
    system_prompt = prompts.get("system_prompt", "")
    fallback = prompts.get("fallback_message", "Disculpa, no entendí tu mensaje.")
    error_msg = prompts.get("error_message", "Lo siento, estoy teniendo problemas técnicos.")

    if not mensaje.strip():
        return fallback

    messages = historial + [{"role": "user", "content": mensaje}]

    try:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        text = response.content[0].text.strip() if response.content else ""
        return text if text else fallback
    except Exception:
        return error_msg
