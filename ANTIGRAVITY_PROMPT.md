# ANTIGRAVITY_PROMPT.md

Prompt inicial para Antigravity. Copiar el bloque de abajo y pegarlo en el
primer chat.

---

## Prompt

```text
Voy a desarrollar la aplicacion de escritorio "Faith Store", un sistema de
control de inventario para Windows 10/11. El repositorio ya esta inicializado
en GitHub y tiene documentacion de contexto que debes leer ANTES de escribir
una sola linea de codigo.

PASO 0 - OBLIGATORIO: LEE LA DOCUMENTACION

Antes de cualquier otra cosa, lee estos archivos en este orden:

1. PROJECT_CONTEXT.md   -> Que es el proyecto, el dominio del negocio, el modelo
                           de datos y los criterios de aceptacion.
2. AGENTS.md            -> Las reglas de trabajo: convenciones de codigo,
                           arquitectura, git y testing. Son obligatorias.
3. ROADMAP.md           -> El plan de trabajo por fases. Busca el primer
                           checkbox sin marcar y trabaja ahi.
4. UI_SPEC.md           -> Como se ve la aplicacion. Leer antes de tocar
                           cualquier archivo en views/.

Tambien revisa el estado actual del codigo en la seccion final de ROADMAP.md
("Estado de la Implementacion Actual"). Ahi hay una auditoria que reporta bugs
concretos en el codigo existente. Tenla en cuenta: parte de ese codigo no
funciona correctamente y hay que corregirlo o reescribirlo.

PASO 1 - CONFIRMA QUE ENTENDISTE

Antes de escribir codigo, responde de forma explicita y breve:

a) Que problema de negocio resuelve Faith Store y cual es su pieza central.
b) Como se estructura el proyecto en capas y que puede y que no puede hacer
   cada capa.
c) Que 3 bugs concretos encontraste en el codigo actual.
d) Que tarea del ROADMAP.md vas a hacer primero y por que.

No empieces a escribir codigo hasta que yo confirme que tu understanding es
correcto.

PASO 2 - TRABAJA MODULO A MODULO

Una vez confirmado, trabaja en ciclos cortos. En cada ciclo:

1. Tarea pequena y verificable. Nunca mas de 2-3 archivos.
2. Escribe el codigo.
3. Escribe los tests correspondientes.
4. Corre `python -m pytest tests/ -v` y verifica que todo pasa.
5. Commit en la rama `develop` con Conventional Commits:
   `git add . && git commit -m "feat(modulo): descripcion en imperativo e ingles"`
6. Push: `git push origin develop`
7. Espera mi confirmacion antes de seguir con la siguiente tarea.

En la rama `main` solo entra codigo verificado..Work en `develop`.

PASO 3 - REGLAS QUE NO SE NEGOCIAN

Estas reglas estan en AGENTS.md y son obligatorias:

- Un archivo por clase. Limite de 150 a 200 lineas por archivo.
- Identificadores, funciones y variables en INGLES.
  Ejemplo: `sale_price`, `stock_quantity`, `calculate_margin`.
  NO: `precio_venta`, `stock_actual`, `calcular_margen`.
- Comentarios en ESPANOL y sin tildes (solo caracteres ASCII).
  Ejemplo: `# Verifica el stock minimo`
  NO: `# Verifica el stock mínimo`
- Docstrings en INGLES, formato PEP 257, con Args, Returns y Raises.
- Type hints obligatorios en todos los parametros y todos los retornos.
- Maximo 79 caracteres por linea.
- Prohibido `from modulo import *`.
- Prohibido `.place()` en vistas. Solo `grid` y `pack`.
- Prohibido SQL dentro de `views/`.
- Prohibido `import tkinter` o `import customtkinter` en `models/` o `services/`.
- Los colores y las rutas salen de `config.py`. Nunca literales en vistas.
- Toda operacion de I/O (SQLite, Excel, PDF, backup) en hilo secundario.
  Nunca se toca un widget desde un hilo que no sea el de la GUI; se usa
  `root.after(0, callback)`.

PASO 4 - SOBRE EL STACK

El stack ya esta decidido y aprobado. Puedes elegir la version de las librerias
y organizar las dependencias como lo veas conveniente, pero el stack es:

- Python 3.11+
- CustomTkinter para la GUI
- SQLite 3 para la base de datos
- pandas y openpyxl para Excel
- matplotlib para graficas
- ReportLab para PDF
- PyInstaller e Inno Setup para el empaquetado

Requisito critico: la aplicacion debe funcionar 100% offline. Ninguna
dependencia de red en tiempo de ejecucion.

PASO 5 - ESTILO DE TRABAJO

- Escribe codigo limpio, no ejercicios ni prototipos.
- Si una clase se pasa de 200 lineas, es que tiene mas de una responsabilidad.
  Partela.
- Si un metodo hace 3 cosas, partelo en 3 metodos.
- No agregues dependencias que no esten en el stack aprobado.
- No implementes funciones que no esten en el alcance de la tarea actual.
- Si algo no esta claro de las specs, preguntame antes de inventar.
- Si encuentras un bug en codigo existente, reportalo antes de arreglarlo.

Empecemos. Lee los 4 archivos y respondeme el Paso 1.
```

---

## Notas para el Usuario

**Por que 4 archivos y no uno:**

| Archivo | Pregunta que responde | Se lee |
|---------|----------------------|---------|
| `PROJECT_CONTEXT.md` | Que es esto y por que | 1ro |
| `AGENTS.md` | Como se escribe codigo aqui | 2do |
| `ROADMAP.md` | Que sigue y en que orden | 3ro |
| `UI_SPEC.md` | Como se ve | Al tocar la UI |

Separarlos permite que `AGENTS.md` sea estable mientras el contexto de negocio
cambia, y que la UI se pueda rediseñar sin tocar las reglas de codigo.

**Respondi a tu pregunta:** si, ambos. Un archivo unico seria mas simple al
principio pero en la practica se vuelve inmanejable. Con 4 archivos, el agente
tiene un orden de lectura claro y cada uno tiene un unico proposito.

**El prompt le dice que los lea primero** antes de escribir codigo, y que
confirme su understanding antes de arrancar. Eso evita que un agente arranque a
inventar una arquitectura que despues cuesta deshacer.

**Sugerencia operativa:** al inicio de cada sesion nueva con Antigravity,
pegale solo esto:

```text
Lee PROJECT_CONTEXT.md, AGENTS.md y ROADMAP.md. Revisa el estado del git.
Dime cual es la siguiente tarea del roadmap y esperame para confirmar.
```
