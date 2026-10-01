# AGENTS.md

Este proyecto se construye desde cero a partir de la documentacion en
`ai_handoff/`. No hay codigo de referencia.

**Antes de escribir una sola linea, lee `ai_handoff/README.md`.**

Orden de lectura:

| Archivo | Responde a |
|---------|-----------|
| `ai_handoff/01_requisitos.md` | Que debe hacer el programa y por que |
| `ai_handoff/02_arquitectura.md` | Como estructurar el codigo |
| `ai_handoff/03_convenciones.md` | Como se escribe el codigo aqui |
| `ai_handoff/05_plan_trabajo.md` | En que orden construir y como medir avance |
| `ai_handoff/04_interfaz.md` | Como se ve la app, antes de la primera vista |

Reglas que no se negocian:

1. SQL solo en la capa de datos. Nunca en las vistas.
2. `import tkinter` nunca en `models/` ni `services/`.
3. `.place()` esta prohibido. Solo `grid` y `pack`.
4. Colores y rutas salen de `config.py`.
5. Todo I/O de disco, base de datos o PDF va en hilo secundario.
6. Un archivo por clase. Maximo 200 lineas por archivo.
7. Identificadores en ingles, comentarios en espanol, docstrings en ingles.
8. Type hints en todos los parametros y retornos.
9. Prohibido `from x import *`.
10. Nunca commit con tests fallando.

Ramas: `main` es produccion. `develop` es el trabajo activo. Nunca escribas
directo en `main`.

Commits en formato Conventional Commits:
`feat(catalog): Add size matrix with independent stock per variant`

Si una regla estorba, dimelo y propone el ajuste. No la ignores en silencio.
