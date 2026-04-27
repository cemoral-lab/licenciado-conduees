import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agent import brain, memory
from agent.providers import obtener_proveedor

# Buffers: telefono -> list[str]
_buffers: dict[str, list[str]] = {}
_timers: dict[str, asyncio.Task] = {}
_ESPERA_SEGUNDOS = 10

proveedor = obtener_proveedor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await memory.inicializar_db()
    yield


app = FastAPI(title="El Licenciado — ConduEES", lifespan=lifespan)


async def _procesar_mensajes(telefono: str):
    await asyncio.sleep(_ESPERA_SEGUNDOS)

    textos = _buffers.pop(telefono, [])
    _timers.pop(telefono, None)

    if not textos:
        return

    mensaje_usuario = " ".join(textos)
    historial = await memory.obtener_historial(telefono)

    respuesta = await brain.generar_respuesta(mensaje_usuario, historial)

    await memory.guardar_mensaje(telefono, "user", mensaje_usuario)
    await memory.guardar_mensaje(telefono, "assistant", respuesta)

    await proveedor.enviar_mensaje(telefono, respuesta)


def _programar_respuesta(telefono: str):
    if telefono in _timers:
        _timers[telefono].cancel()

    loop = asyncio.get_event_loop()
    task = loop.create_task(_procesar_mensajes(telefono))
    _timers[telefono] = task


@app.get("/webhook")
async def verificar_webhook(request: Request):
    resultado = await proveedor.validar_webhook(request)
    if resultado is None:
        return JSONResponse({"status": "ok"})
    if isinstance(resultado, int):
        return JSONResponse({"error": "Token inválido"}, status_code=resultado)
    return resultado


@app.post("/webhook")
@app.post("/webhook/messages")
async def recibir_webhook(request: Request):
    mensajes = await proveedor.parsear_webhook(request)

    for msg in mensajes:
        if msg.es_propio:
            continue

        if msg.tipo != "text":
            await proveedor.enviar_mensaje(
                msg.telefono,
                "Por el momento solo proceso mensajes de texto. "
                "Escríbeme tu consulta y con gusto te ayudo."
            )
            continue

        if msg.telefono not in _buffers:
            _buffers[msg.telefono] = []
        _buffers[msg.telefono].append(msg.texto)
        _programar_respuesta(msg.telefono)

    return JSONResponse({"status": "ok"})


@app.get("/")
async def health():
    return {"status": "ok", "agente": "El Licenciado", "escuela": "ConduEES"}
