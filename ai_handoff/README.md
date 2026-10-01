# Faith Store - Documentacion para Construccion desde Cero

Esta carpeta contiene **todo** lo necesario para construir Faith Store desde
cero, sin depender de ningun codigo previo.

**No leas codigo existente.** Este proyecto se diseña aqui, desde los
requerimientos. Cualquier intento previo es descartable.

---

## Orden de Lectura

| # | Archivo | Responde a | Cuando se lee |
|---|---------|-----------|---------------|
| 1 | `01_requisitos.md` | Que debe hacer el programa y por que | Al inicio, siempre |
| 2 | `02_arquitectura.md` | Como estructurar el codigo | Al inicio, antes de escribir |
| 3 | `03_convenciones.md` | Como se escribe el codigo aqui | Al inicio, antes de escribir |
| 4 | `04_interfaz.md` | Como se ve y se siente la aplicacion | Antes de la primera vista |
| 5 | `05_plan_trabajo.md` | En que orden construir y como medir avance | Al inicio, y en cada sesion |
| 6 | `PROMPT_INICIAL.md` | El prompt para pegar en el agente | El primer mensaje |

---

## Principio de Trabajo

**Tu decides la implementacion.** Estos documentos definen *que* construir y
*como debe comportarse*, no *como escribir cada linea*.

Libertad que tienes:

- Elegir estructura de carpetas concreta.
- Elegir librerias y herramientas, siempre que cumplas los requisitos.
- Proponer frameworks internos, patrones y helpers.
- Decidir si las vistas se construyen por codigo o declarativamente.
- Elegir tu propia estrategia de testing si la de `03_convenciones.md` no encaja.

Restricciones que no puedes cambiar:

- Debe funcionar **100% offline**. Cero llamadas de red en ejecucion.
- Debe ser un **ejecutable nativo de Windows 10/11**, no una web app.
- Debe cumplir los **criterios de aceptacion** de `01_requisitos.md`.
- Debe seguir las **convenciones de codigo** de `03_convenciones.md`.
- Debe seguir el **modelo de datos** de `02_arquitectura.md`.

**Si una herramienta aprobada no resuelve un caso, sustituyela y documenta el
motivo.** No te detengas a preguntar por cada decision tecnica: documenta y
sigue.

---

## Stack Sugerido (no obligatorio)

El cliente aprobo un stack. Es un punto de partida razonable, no un dogma.

| Necesidad | Sugerencia | Alternativas validas |
|-----------|------------|---------------------|
| Lenguaje | Python 3.11+ | - |
| GUI | CustomTkinter | PySide6, wxPython, .NET WPF |
| BD | SQLite 3 | - (es la unica que se puede embeber sin servidor) |
| Excel | pandas + openpyxl | openpyxl solo, polars |
| Graficas | matplotlib | pyqtgraph, plotly embebido |
| PDF | ReportLab | fpdf2, weasyprint |
| Empaquetado | PyInstaller + Inno Setup | Nuitka + Inno Setup |

**Criterio para sustituir:** la alternativa debe cumplir los mismos criterios de
aceptacion, seguir disponible sin conexion, y ser mantenible. Si cambias algo,
anotalo en `05_plan_trabajo.md` con el motivo.

---

## Estado

Proyecto en fase de documentacion. **Cero lineas de codigo produccion.**

Rama de trabajo: `develop`. Rama de produccion: `main`.

---

**Empieza por `01_requisitos.md`.**
