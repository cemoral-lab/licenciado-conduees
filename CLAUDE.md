# El Licenciado — ConduEES

Agente de WhatsApp para la escuela de conducción ConduEES (UEES, Ecuador).

## Stack

- **Runtime**: Python 3.11
- **Web**: FastAPI + Uvicorn (async)
- **IA**: Anthropic Claude (claude-sonnet-4-6) via `AsyncAnthropic`
- **WhatsApp**: Whapi.cloud (principal), Meta Cloud API (alternativo)
- **Base de datos**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Config**: YAML para prompts y datos del negocio, dotenv para secretos

## Estructura

```
agent/
  main.py          # FastAPI + webhook + buffering de mensajes
  brain.py         # Llamada a Claude con historial
  memory.py        # Persistencia de conversaciones (SQLAlchemy)
  tools.py         # Funciones de negocio (cursos, requisitos, horarios)
  providers/
    base.py        # Interfaz abstracta ProveedorWhatsApp
    whapi.py       # Implementación Whapi.cloud
    meta.py        # Implementación Meta Cloud API
    __init__.py    # Factory: obtener_proveedor()
config/
  prompts.yaml     # System prompt de El Licenciado
  business.yaml    # Información del negocio
knowledge/
  conduees_info.txt  # Base de conocimiento de ConduEES
tests/
  test_local.py    # Chat en terminal para pruebas sin WhatsApp
```

## Variables de entorno

Copiar `.env.example` a `.env` y completar:

```
ANTHROPIC_API_KEY=sk-ant-...
WHATSAPP_PROVIDER=whapi
WHAPI_TOKEN=...
PORT=8000
DATABASE_URL=sqlite+aiosqlite:///./licenciado.db
```

## Desarrollo local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Probar el agente sin WhatsApp
python tests/test_local.py

# Levantar servidor
uvicorn agent.main:app --reload --port 8000
```

## Pruebas con webhook real

Usar ngrok para exponer el servidor local:
```bash
ngrok http 8000
# Configurar la URL pública en Whapi.cloud o Meta como webhook
```

## Despliegue

```bash
# Docker local
docker compose up --build

# Railway: conectar repo, configurar variables de entorno en el panel
```

## Lógica clave

- **Buffering**: los mensajes de un mismo número se acumulan 10 segundos antes de procesar,
  para no responder a cada mensaje suelto de una conversación fragmentada.
- **Proveedor abstracto**: cambiar `WHATSAPP_PROVIDER=meta` en `.env` para usar Meta en lugar de Whapi sin tocar código.
- **System prompt**: todo el comportamiento del agente se controla desde `config/prompts.yaml`.
  Editar ahí para ajustar tono, reglas o información del negocio.
