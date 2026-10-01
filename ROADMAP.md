# ROADMAP.md - Plan de Ejecucion de Faith Store

> **Que es este archivo:** El plan de trabajo. Marca que falta y en que orden.
> Actualizar los checkboxes al cerrar cada tarea.

**Leyenda:** `[ ]` pendiente · `[~]` en curso · `[x]` completado

---

## Fase 0 - Cimientos (Semana 1)

Objetivo: repo limpio, BD funcionando, modelos puros testeados.

- [x] Repositorio Git inicializado con ramas `main` y `develop`
- [x] `main` configurada como rama por defecto en GitHub
- [x] `.gitignore` ignora `documento.txt`, `instrucciones.md`, `*.db`, `build/`, `*.exe`
- [x] `requirements.txt` con el stack aprobado
- [x] `config.py` con paleta, rutas y umbrales centralizados
- [ ] `database/connection.py` cierra la conexion real en `__exit__` (bug actual)
- [ ] `database/schema.sql` con el DDL del modelo de datos de `PROJECT_CONTEXT.md`
- [ ] `models/product_model.py` con identificadores en ingles
- [ ] `models/variant_model.py` con identificadores en ingles
- [ ] `tests/` cubren producto, variante y esquema
- [ ] `main.py` arranca una ventana vacia sin errores

---

## Fase 1 - Catalogo y Matriz de Tallas (Semana 1-2)

Objetivo: alta y gestion de productos con stock independiente por talla.

- [ ] `models/product_model.py` - CRUD de producto + margen bruto
- [ ] `models/variant_model.py` - CRUD de variante + estado del semaforo
- [ ] `models/size_validator.py` - valida tallas de letra y numericas
- [ ] `views/main_window.py` - sidebar + topbar + contenedor
- [ ] `views/catalog_view.py` - listado de productos
- [ ] `views/components/product_card.py` - tarjeta con matriz de tallas
- [ ] `views/components/stock_bar.py` - barra vertical de stock
- [ ] `views/components/size_pill.py` - pildora de talla con alerta
- [ ] `controllers/catalog_controller.py` - puente con inyeccion
- [ ] `tests/test_product_model.py`
- [ ] `tests/test_variant_model.py`
- [ ] Alta, edicion y baja funcionando desde la GUI

---

## Fase 2 - Buscador Inteligente (Semana 2)

- [ ] `services/text_normalizer.py` - NFD, quita tildes, pasa a minusculas
- [ ] `services/search_service.py` - busqueda por codigo y por nombre
- [ ] La busqueda ignora tildes: "pantalon" encuentra "Pantalón"
- [ ] `views/components/search_bar.py` - `CTkEntry` con `corner_radius=20`
- [ ] Autocompletado flotante en tiempo real
- [ ] Debounce de 300 ms para no consultar en cada tecla
- [ ] `tests/test_search.py`

---

## Fase 3 - Importacion Excel y Backup (Semana 3)

- [ ] `services/excel_service.py` - lee `.xlsx` con pandas
- [ ] Plantilla estandarizada de importacion
- [ ] Importacion **transaccional**: si una fila falla, no se importa nada
- [ ] Reporte de filas importadas y rechazadas
- [ ] `services/backup_service.py` - clona la BD con `sqlite3.Connection.backup()`
- [ ] Backup con fecha y hora en el nombre
- [ ] Selector de destino (USB, carpeta, red local)
- [ ] Todo el I/O de Excel y backup en hilo secundario
- [ ] `tests/test_excel_service.py`
- [ ] `tests/test_backup_service.py`

---

## Fase 4 - Punto de Venta y Multimoneda (Semana 4)

- [ ] `models/sale_model.py` - registro de venta
- [ ] `models/exchange_rate_model.py` - tasa BCV con fecha
- [ ] `services/currency_converter.py` - USD / Bs. / USDT
- [ ] La venta congela la tasa usada en el momento
- [ ] El descuento de stock y el registro de venta son atomicos
- [ ] `views/pos_view.py` - caja con seleccion de prenda y talla
- [ ] `services/pdf_service.py` - ticket con ReportLab
- [ ] `tests/test_currency_converter.py`
- [ ] `tests/test_sale_model.py`

---

## Fase 5 - Dashboard y Alertas (Semana 5)

- [ ] `services/report_service.py` - agregaciones por periodo
- [ ] `views/dashboard_view.py` - panel de metricas
- [ ] Graficas matplotlib embebidas con `FigureCanvasTkAgg`
- [ ] Ejes ocultos, grafica limpia, estilo coherente con la paleta
- [ ] `views/components/stock_alert_popup.py` - aviso al quedar critico
- [ ] Filtros por rango: diario, semanal, mensual
- [ ] Exportar reporte a `.xlsx` con un boton
- [ ] `tests/test_report_service.py`

---

## Fase 6 - Empaquetado (Semana 6)

- [ ] `faith_store.spec` de PyInstaller
- [ ] Icono `.ico` y datos de version
- [ ] Verificar arranque en limpio, sin Python instalado
- [ ] `installer.iss` de Inno Setup
- [ ] Estructura de instalador con acceso directo y desinstalacion
- [ ] Verificacion 100% offline en Windows 10 y 11

---

## Fase 7 - QA y Entrega (Semana 7)

- [ ] Carga de 1000+ productos y medir tiempos
- [ ] Busqueda sobre 5000 productos: respuesta < 100 ms
- [ ] Pruebas de uso continuo de 8 horas
- [ ] Revision de fugas de conexiones y memoria
- [ ] Pulido visual de componentes
- [ ] Guia de usuario en PDF
- [ ] `main.py` actualizado a `v1.0.0`

---

## Como Usar Este Archivo

**Al iniciar cada sesion de trabajo:**

1. Leer `PROJECT_CONTEXT.md` (recordar el problema)
2. Leer `AGENTS.md` (recordar las reglas)
3. Leer este archivo y buscar el primer `[ ]` sin marcar
4. Marcar `[~]` en la tarea al comenzarla

**Al terminar cada tarea:**

1. Correr `python -m pytest tests/ -v`
2. Commit en `develop` con Conventional Commits
3. `git push origin develop`
4. Marcar la tarea como `[x]`

**Al cerrar una Fase completa:**

1. Verificar que la funcionalidad se ve desde `main.py`
2. `git checkout main && git merge develop`
3. `git tag -a v0.X.0 -m "Fase N completada"`
4. `git checkout develop`

---

## Estado de la Implementacion Actual

Auditoria honesta del codigo existente en `develop`, para saber que se puede
reusar y que hay que reescribir.

### Funciona y se puede reusar

| Archivo | Observacion |
|---------|-------------|
| `config.py` | Estructura correcta. Expandir con la paleta de `UI_SPEC.md`. |
| `database/migrations.py` | DDL completo y funcional. Ajustar al modelo de datos final. |
| `tests/test_migrations.py` | 6 tests pasando. Buen patron de `fixture` con `:memory:`. |
| `tests/test_database.py` | 6 tests pasando. Patron de `tmp_path` correcto. |
| `.gitignore`, `requirements.txt` | Correctos. |

### Bugs que hay que corregir

| Archivo | Problema | Impacto |
|---------|----------|---------|
| `database/connection.py:77` | `__exit__` abre una conexion **nueva** en vez de cerrar la de `__enter__` | Fuga de conexiones. Se acumularan con el uso. |
| `controllers/catalog_controller.py` | Busca atributos `sale_price`, `costo_precio`, `product_id`, `code`, `name` que **no existen** en los modelos (que usan `precio_venta`, `costo`, `id`, `codigo`, `nombre`) | El catalogo muestra `Producto`, `None` y margen `0.0%` siempre. |
| `models/product_model.py`<br>`models/variant_model.py` | Atributos en espanol, violan la Regla #3 | Rompe la convencion del proyecto. |

### Violaciones de las reglas

| Archivo | Lineas | Regla violada |
|---------|--------|---------------|
| `views/catalog_view.py` | 437 | Regla #1 (max 200). deberia partirse en `views/components/`. |
| `controllers/catalog_controller.py` | 267 | Regla #1 (max 200). |
| `views/catalog_view.py` | - | Regla #4: usa `tkinter` crudo, no `CTkFrame` / `CTkScrollableFrame`. |
| `views/catalog_view.py` | - | Regla #5: colores hex como literales en la vista. |
| `main.py` | - | Colores hex como literales. Deberian venir de `config.py`. |
| `views/catalog_view.py` | - | `_on_keyrelease` agenda un `after(300)` por tecla sin cancelar el anterior. No hay debounce real. |

### Decision Sugerida

El esqueleto actual es util como referencia de la estructura de carpetas, pero
**no cumple las reglas del proyecto y tiene bugs que se manifiestan en la UI**.

Dos caminos:

1. **Reescribir desde cero** siguiendo `PROJECT_CONTEXT.md` + `AGENTS.md`.
   Es lo mas limpio. El volumen de codigo actual es pequeno.
2. **Corregir sobre la marcha** durante la Fase 1.

Recomendacion: **reescribir `models/`, `controllers/` y `views/` desde cero**,
conservando `config.py`, `requirements.txt`, `.gitignore`, `migrations.py` y los
dos archivos de test, que si son solidos.
