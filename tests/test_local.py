"""
Simulador de chat local para probar El Licenciado sin WhatsApp.
Uso: python tests/test_local.py
Comandos: 'salir' para terminar, 'limpiar' para borrar historial.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from agent import brain, memory

TELEFONO_TEST = "test-local-001"


async def chat():
    await memory.inicializar_db()
    print("\n=== El Licenciado — ConduEES (modo local) ===")
    print("Escribe 'salir' para terminar, 'limpiar' para borrar historial.\n")

    while True:
        try:
            entrada = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta pronto.")
            break

        if not entrada:
            continue

        if entrada.lower() == "salir":
            print("Hasta pronto.")
            break

        if entrada.lower() == "limpiar":
            await memory.limpiar_historial(TELEFONO_TEST)
            print("[Historial borrado]\n")
            continue

        historial = await memory.obtener_historial(TELEFONO_TEST)
        respuesta = await brain.generar_respuesta(entrada, historial)

        await memory.guardar_mensaje(TELEFONO_TEST, "user", entrada)
        await memory.guardar_mensaje(TELEFONO_TEST, "assistant", respuesta)

        print(f"\nEl Licenciado: {respuesta}\n")


if __name__ == "__main__":
    asyncio.run(chat())
