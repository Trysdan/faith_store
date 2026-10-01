# Prompt Inicial

Copiar el bloque de abajo, pegarlo en el primer mensaje del agente, y esperar
su respuesta antes de dejarle escribir codigo.

---

## Prompt Completo

```text
Vamos a construir "Faith Store", una aplicacion de escritorio de control de
inventario para una tienda de ropa y calzado, para Windows 10/11, que funcione
100% offline y se entregue como instalador .exe.

El repositorio esta inicializado en GitHub. Toda la especificacion esta escrita
en la carpeta `ai_handoff/`. Ese proyecto se construye desde cero, a partir de
esos documentos. No existe codigo de referencia: no copies de ningun lado, no
busques implementaciones previas, no asumas que hay algo hecho.

PASO 0 - LEE LA DOCUMENTACION (obligatorio, antes de cualquier otra cosa)

Lee estos archivos en este orden:

1. `ai_handoff/01_requisitos.md`      Que debe hacer el programa y por que.
2. `ai_handoff/02_arquitectura.md`    Capas, modelo de datos, concurrencia.
3. `ai_handoff/03_convenciones.md`    Como se escribe el codigo aqui.
4. `ai_handoff/05_plan_trabajo.md`    Orden de construccion y checkboxes.
5. `ai_handoff/04_interfaz.md`        Como se ve la app. Antes de la primera
                                       vista, no antes.

PASO 1 - CONFIRMA QUE ENTENDISTE (obligatorio, antes de escribir codigo)

Respondeme de forma breve y explicita:

a) Que problema de negocio resuelve Faith Store y cual es su concepto central.
b) Las cuatro capas de la arquitectura y que puede y que no puede hacer cada
   una. Dame un ejemplo concreto de algo prohibido.
c) Por que la tasa BCV se congela en la fila de la venta y no se lee de la
   configuracion al mostrar un reporte.
d) Las tres convenciones de codigo que mas se ignoran sin querer.
e) Que tarea del plan de trabajo vas a hacer primero y por que esa.

No escribas codigo hasta que te confirme que tu understanding es correcto.

PASO 2 - LIBERTAD DE IMPLEMENTACION

Tu decides la implementacion. Los documentos definen que construir y como
debe comportarse, no como escribir cada linea.

Decide tu: la estructura concreta de carpetas, las librerias, los patrones
internos, tu estrategia de testing, como descompones los componentes de
interfaz.

El stack sugerido es Python con CustomTkinter, SQLite, pandas, matplotlib,
ReportLab, PyInstaller e Inno Setup. Puedes sustituirlo si una alternativa
cumple mejor los criterios de aceptacion, siempre que Documente el motivo en la
seccion 8 del plan de trabajo. Lo que NO es negociable: que sea un ejecutable
nativo de Windows, que funcione sin internet, y que cumpla los criterios de
aceptacion.

PASO 3 - TRABAJA EN CICLOS CORTOS

1. Tarea pequena y verificable. Maximo 2 o 3 archivos por ciclo.
2. Escribe el codigo.
3. Escribe los tests, junto al codigo, no despues.
4. Corre `python -m pytest tests/ -v`. Debe pasar completo.
5. Commit en `develop`:
   `git add . && git commit -m "feat(modulo): descripcion en imperativo e ingles"`
6. `git push origin develop`
7. Espera mi confirmacion antes de la siguiente tarea.

La rama `main` solo recibe codigo verificado, mediante merge y tag.

PASO 4 - REGLAS QUE NO SE NEGOCIAN

Arquitectura, de `02_arquitectura.md`:
- SQL solo en la capa de datos. Nunca en `views/`.
- `import tkinter` o `import customtkinter` nunca en `models/` ni `services/`.
- Las vistas no contienen reglas de negocio ni calculos.
- Los controllers inyectan dependencias, no las instancian.
- Todo I/O de disco, base de datos o generacion de documentos va en hilo
  secundario. Nunca se toca un widget desde un hilo que no sea el de la GUI:
  se vuelve con `root.after(0, callback)`.
- Sin `.place()`. Solo `grid` y `pack`.
- Colores y rutas salen de `config.py`. Nunca literales en las vistas.

Codigo, de `03_convenciones.md`:
- Identificadores, funciones, variables y archivos en INGLES.
  `sale_price`, `stock_quantity`, `calculate_margin`.
  NO: `precio_venta`, `stock_actual`, `calcular_margen`.
- Comentarios en ESPANOL, solo caracteres ASCII, sin tildes ni enie.
  `# Verifica el stock minimo`
- Docstrings en INGLES, PEP 257, con Args, Returns y Raises.
- Textos de la interfaz en ESPANOL.
- Type hints en todos los parametros y todos los retornos.
- Maximo 79 caracteres por linea. 4 espacios de indentacion.
- Prohibido `from x import *`.
- Un archivo por clase. Maximo 200 lineas por archivo, 30 por metodo.

Git, de `03_convenciones.md`:
- Conventional Commits: `feat(catalog): Add size matrix with variants`.
- Nunca commit con tests fallando.
- Nunca secretos, tokens ni claves.

PASO 5 - ESTILO DE TRABAJO

- Codigo limpio para produccion, no ejercicios ni prototipos.
- Si una clase pasa de 200 lineas, tiene mas de una responsabilidad. Partela.
- Si un metodo hace tres cosas, partelo en tres metodos.
- No agregues dependencias fuera del stack aprobado sin justificar.
- No implementes nada fuera del alcance de la tarea actual.
- Si un requerimiento es ambiguo, preguntame. No inventes comportamiento.
- Si encuentras un bug, reportalo antes de arreglarlo.
- Si una regla de la documentacion estorba, dimelo y propón el ajuste. No la
  ignores en silencio.

Empieza por el Paso 0. Leeme los cinco documentos y despues respondeme el
Paso 1.
```

---

## Notas

**Por que el Paso 1 es obligatorio:** un agente que arranca a escribir sin
confirmar el understanding construye la arquitectura equivocada, y corregirla
despues cuesta mas que rehacerla. Las cinco preguntas del Paso 1 apuntan a los
puntos donde es mas facil equivocarse: el concepto de variantes, la frontera
entre capas, la tasa congelada, las convenciones de estilo, y el orden de
construccion.

**Por que los ciclos son cortos:** con tareas de 2 a 3 archivos, un commit
revisable y un push, hay siempre un punto de retorno. Si algo sale mal, se
revierte un commit, no un dia de trabajo.

**Por que la libertad de implementacion esta explicita:** el agente rinde mejor
cuando decide el como. Documentar *que* y *como debe comportarse*, y dejarlo
decidir el *como escribir*, produce mejor resultado que prescribir cada
detalle.

**Si la sesion se corta**, al volver pegale solo esto:

```text
Lee `ai_handoff/01_requisitos.md` y `ai_handoff/05_plan_trabajo.md`.
Revisa `git log --oneline -10` y `git status`.
Dime cual es la siguiente tarea del plan y esperame para confirmar.
```
