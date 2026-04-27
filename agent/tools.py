import os
from pathlib import Path

import yaml


def cargar_info_negocio() -> dict:
    path = Path(__file__).parent.parent / "config" / "business.yaml"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def obtener_cursos() -> str:
    return """
Cursos disponibles en ConduEES:

Categoría B (vehículos livianos):
- Curso inicial: 40 horas teóricas + 20 horas prácticas
- Precio: $280
- Duración: 5 semanas (lunes a viernes)

Categoría A (motocicletas):
- Curso inicial: 30 horas teóricas + 15 horas prácticas
- Precio: $200
- Duración: 4 semanas

Categoría C (vehículos pesados):
- Solo para conductores con licencia B vigente mínimo 1 año
- 30 horas teóricas + 20 horas prácticas
- Precio: $350
- Duración: 5 semanas

Renovación y revalidación:
- Curso de actualización: 8 horas
- Precio: $60
""".strip()


def obtener_requisitos() -> str:
    return """
Requisitos para inscribirse en ConduEES:

Documentos obligatorios:
1. Cédula de identidad o pasaporte (original y copia)
2. Certificado médico con aptitud para conducir (lo tramitamos en convenio)
3. Foto tamaño carné (2 fotos)
4. Pago de la matrícula

Requisitos de edad:
- Categoría A: mínimo 18 años
- Categoría B: mínimo 18 años
- Categoría C: mínimo 21 años y licencia B vigente 1+ año

No se requiere licencia previa para categorías A y B (primera vez).
""".strip()


def obtener_horarios() -> str:
    return """
Horarios de atención y clases:

Oficina de inscripciones:
- Lunes a viernes: 08h00 a 17h00
- Sábado: 08h00 a 12h00

Clases teóricas (salones UEES):
- Horario matutino: lunes, miércoles, viernes 07h00 - 09h00
- Horario vespertino: martes, jueves 17h00 - 20h00
- Horario intensivo sábado: 08h00 - 13h00

Clases prácticas (pista de manejo):
- Lunes a sábado: turnos de 2 horas (07h00, 09h00, 11h00, 14h00, 16h00)
- Previa coordinación con el instructor asignado
""".strip()


def obtener_proceso_licencia() -> str:
    return """
Proceso para obtener tu licencia en Ecuador:

1. Inscripción en ConduEES y pago de matrícula
2. Examen médico (aptitud visual y física)
3. Curso teórico (leyes de tránsito, señales, mecánica básica)
4. Examen teórico interno (debe aprobar con 70/100)
5. Clases prácticas de manejo con instructor
6. Examen práctico interno
7. Registro en el sistema ANT (Agencia Nacional de Tránsito)
8. Examen oficial ANT (teórico + psicosensométrico)
9. Pago de derechos ANT ($50 aproximadamente)
10. Entrega de licencia física (7-15 días hábiles)

ConduEES gestiona los pasos 1-7. Los pasos 8-10 son directamente con la ANT.
Apoyamos con la preparación para el examen ANT.
""".strip()


def buscar_en_conocimiento(consulta: str) -> str:
    path = Path(__file__).parent.parent / "knowledge"
    if not path.exists():
        return ""

    consulta_lower = consulta.lower()
    resultados = []

    for archivo in path.glob("*.txt"):
        contenido = archivo.read_text(encoding="utf-8")
        lineas = contenido.splitlines()
        for linea in lineas:
            if any(palabra in linea.lower() for palabra in consulta_lower.split()):
                resultados.append(linea.strip())

    return "\n".join(resultados[:10]) if resultados else ""
