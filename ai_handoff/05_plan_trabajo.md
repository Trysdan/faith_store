# 05 - Plan de Trabajo

> En que orden construir, como medir el avance y cuando se considera terminado.
> Actualizar los checkboxes al cerrar cada tarea.

**Leyenda:** `[ ]` pendiente · `[~]` en curso · `[x]` completado

---

## 1. Estructura del Proyecto

Estos son los **modulos** del negocio, en orden de dependencia. No se puede
construir el punto de venta sin el catalogo. No se puede construir el catalogo
sin el modelo de datos.

| # | Modulo | Depende de |
|---|--------|-----------|
| 0 | Cimientos: repo, esquema, nucleo de dominio | - |
| 1 | Catalogo y matriz de tallas | 0 |
| 2 | Buscador inteligente | 1 |
| 3 | Importacion Excel y backup | 1 |
| 4 | Punto de venta y multimoneda | 1, 3 |
| 5 | Dashboard y alertas visuales | 1, 2, 4 |
| 6 | Empaquetado e instalador | Todos |
| 7 | QA, pulido y entrega | Todos |

---

## 2. Como Trabajar en Cada Sesion

### Al empezar

1. Leer `01_requisitos.md`, `02_arquitectura.md`, `03_convenciones.md`.
2. Revisar el estado de git: `git log --oneline -10` y `git status`.
3. Buscar el primer checkbox `[ ]` sin marcar en la fase actual.
4. Marcarlo `[~]`.
5. Decir que tarea se va a hacer y por que.

### Durante

- Tareas de 2 a 3 archivos maximo por ciclo.
- Tests escritos junto al codigo, no despues.
- `python -m pytest tests/ -v` antes de cada commit.
- Un commit por tarea.
- Si aparece una decision no prevista, documentarla en la seccion 8.

### Al terminar

1. Tests pasando.
2. Commit con Conventional Commits.
3. `git push origin develop`.
4. Marcar el checkbox.
5. Preguntar antes de arrancar la siguiente tarea.

---

## Fase 0 - Cimientos

**Objetivo:** repo listo, esquema creado, logica de dominio probada sin
interfaz.

### Repo

- [ ] Repositorio Git con ramas `main` y `develop`
- [ ] `main` es la rama por defecto
- [ ] `.gitignore` cubre base de datos, backups, builds, `.venv`, cache
- [ ] `requirements.txt` con el stack
- [ ] `README.md` con que es el proyecto y como correrlo
- [ ] `config.py` con paleta, rutas, umbrales y textos

### Esquema de datos

- [ ] `schema.py` con el DDL de `02_arquitectura.md`
- [ ] Indices creados
- [ ] `CHECK` constraints activos
- [ ] Migracion aplicada en una base vacia sin error
- [ ] Migracion idempotente: correrla dos veces no rompe

### Dominio puro (sin base de datos, sin interfaz)

- [ ] `ProductModel` con validacion y margen bruto
- [ ] `VariantModel` con stock y transiciones
- [ ] `StockStatus`: semaforo de tres estados
- [ ] `SizeValidator`: ropa y calzado
- [ ] `Money`: aritmetica de moneda
- [ ] Tests de los cuatro, incluyendo los tres casos minimos

### Punto de partida de la interfaz

- [ ] `main.py` arranca y cierra sin error
- [ ] Ventana vacia visible
- [ ] Sidebar con los 5 items de navegacion
- [ ] TopBar con buscador y tasas
- [ ] Navegar entre modulos vacios funciona

**Criterio de salida:** `python main.py` abre una ventana navegable, y
`python -m pytest tests/ -v` pasa completo.

---

## Fase 1 - Catalogo y Matriz de Tallas

**Objetivo:** alta, edicion y consulta de productos con stock por talla.

### Dominio y datos

- [ ] `ProductRepository`: alta, edicion, desactivacion, busqueda por codigo
- [ ] `VariantRepository`: alta, edicion, ajuste de stock, listar por producto
- [ ] `CatalogService`: orquesta las operaciones
- [ ] Transaccion: producto y sus tallas se guardan juntos o no se guardan
- [ ] `ProductModel` y `VariantModel` persistidos y recuperados
- [ ] Un producto con ventas no se borra, se desactiva

### Interfaz

- [ ] `main_window.py` con sidebar, topbar y contenedor
- [ ] `catalog_view.py`: listado en grid de 3 columnas
- [ ] `product_card.py` con la anatomia de `04_interfaz.md`
- [ ] `size_pill.py`: pildoras de talla con estado
- [ ] `stock_bar.py`: barra vertical
- [ ] `stock_badge.py`: badge de estado
- [ ] `empty_state.py`: estado vacio
- [ ] Formulario de alta y edicion
- [ ] Detalle del producto con su matriz de tallas

### Controller

- [ ] `CatalogController` con dependencias inyectadas
- [ ] Sin SQL, sin widgets, sin logica de negocio
- [ ] I/O de carga en hilo secundario

### Tests

- [ ] `test_product.py`
- [ ] `test_variant.py`
- [ ] `test_stock_status.py`
- [ ] `test_catalog_service.py`
- [ ] Test de integracion: crear producto con tallas y leerlo

**Criterio de salida:** se crea un producto con tallas desde la interfaz, se ve
en el grid, y su margen se muestra con el color correcto.

---

## Fase 2 - Buscador Inteligente

**Objetivo:** encontrar productos en milisegundos, ignorando tildes.

### Dominio

- [ ] `text_normalizer.py`: NFD, quitar diacriticos, minusculas
- [ ] `SearchService.buscar(query)` por codigo y por nombre
- [ ] Indice normalizado para busqueda: precalcular en la tabla o columna
- [ ] Resaltado de la parte que coincide

### Interfaz

- [ ] `search_bar.py`: `CTkEntry` con lupa, `corner_radius=20`
- [ ] `search_suggestion.py`: desplegable flotante
- [ ] Sugerencia con foto, nombre, codigo, precio, tallas disponibles
- [ ] Debounce de 300 ms, cancelando la consulta anterior
- [ ] Navegar sugerencias con flechas, seleccionar con Enter
- [ ] `Esc` cierra el desplegable

### Rendimiento

- [ ] Indice sobre la columna normalizada
- [ ] Consulta parametrizada, nunca `f-string` con datos del usuario
- [ ] Bajo 100 ms con 5000 productos

### Tests

- [ ] `test_text_normalizer.py`: acentos, mayusculas, espacios
- [ ] `test_search.py`: por codigo, por nombre, por prefijo, sin resultados
- [ ] `test_search.py`: `"pantalon"` encuentra `"Pantalón"`
- [ ] `test_search.py`: `"PANTALON"` encuentra `"Pantalón"`
- [ ] Test de rendimiento con 5000 productos

**Criterio de salida:** escribir `pantalon` muestra `Pantalón` sin pulsar Enter,
en menos de 100 ms con 5000 productos cargados.

---

## Fase 3 - Importacion Excel y Backup

**Objetivo:** cargar el inventario completo sin tipear, y proteger los datos.

### Plantilla

- [ ] `plantilla_inventario.xlsx` con columnas documentadas
- [ ] Formato claro, con ejemplo de una fila
- [ ] Validacion de formato de columnas

### Importacion

- [ ] `ImportService` lee `.xlsx` con pandas
- [ ] Deteccion de separador decimal: `1.234,56` y `1,234.56`
- [ ] Validacion de cada fila antes de escribir
- [ ] **Transaccional:** una fila invalida, cero productos importados
- [ ] Reporte de resultado: importadas, rechazadas y motivo por fila
- [ ] `ReportValidationError` con lista de errores
- [ ] I/O en hilo secundario
- [ ] Progreso visible si supera 1 segundo

### Exportacion

- [ ] `ExportService` a `.xlsx` para catalogo, ventas y stock
- [ ] Respeta los filtros activos
- [ ] I/O en hilo secundario

### Backup

- [ ] `BackupService` con `Connection.backup()`, no copiando el archivo
- [ ] Nombre con fecha y hora
- [ ] Selector de destino: USB, carpeta local, unidad de red
- [ ] Reporta donde se guardo y cuanto pesa
- [ ] Restaura un backup identico a la base original
- [ ] I/O en hilo secundario

### Tests

- [ ] `test_import.py`: caso feliz, fila invalida, archivo vacio, columnas faltantes
- [ ] `test_import.py`: verifica atomicidad, cero escrituras si falla
- [ ] `test_import.py`: ambos formatos de separador decimal
- [ ] `test_backup.py`: crea backup, restaura, compara identico

**Criterio de salida:** 1000 productos importados en menos de 10 segundos, y un
backup restaurado es identico a la original.

---

## Fase 4 - Punto de Venta y Multimoneda

**Objetivo:** registrar ventas rapido, con las tres divisas y tasa congelada.

### Dominio

- [ ] `ExchangeRateModel` con fecha
- [ ] `RateService`: tasa vigente de una fecha, historial, CRUD
- [ ] `Money`: conversion USD a Bs. y USDT
- [ ] `SaleModel`: totales y validaciones
- [ ] Redondeo explicito y consistente, documentado

### Venta atomica

- [ ] `SalesService.registrar_venta` en una transaccion
- [ ] Bloquea la variante, valida stock, descuenta, inserta
- [ ] Si algo falla, no hay descuento ni venta
- [ ] La tasa queda congelada en la fila
- [ ] Test: forzar fallo y verificar que el stock no cambio

### Interfaz

- [ ] `pos_view.py`: buscador izquierda, carrito derecha
- [ ] Talla **obligatoria**. No se puede agregar sin ella
- [ ] Feedback inmediato de stock insuficiente
- [ ] Totales en las tres divisas, actualizados al instante
- [ ] Cantidades por linea, edicion y eliminacion
- [ ] `pdf_service.py`: ticket con ReportLab
- [ ] Ticket con datos del negocio, fecha, numero, lineas, totales, tasa
- [ ] Boton de imprimir

### Tests

- [ ] `test_money.py`: conversiones, redondeos, precision
- [ ] `test_exchange_rate.py`: vigente por fecha, historial
- [ ] `test_sale.py`: totales, caso limite de cantidad 0
- [ ] `test_sales_service.py`: camino feliz
- [ ] `test_sales_service.py`: stock insuficiente rechaza y no descuenta
- [ ] `test_sales_service.py`: la tasa queda congelada
- [ ] `test_sales_service.py`: atomicidad ante fallo

**Criterio de salida:** una venta descuenta stock, congela la tasa, y genera un
ticket PDF con los tres totales. Ningun test falla.

---

## Fase 5 - Dashboard y Alertas

**Objetivo:** ver el rendimiento y enterarse antes de perder una venta.

### Reportes

- [ ] `ReportService`: ingresos por dia, semana, mes
- [ ] Ganancias netas, no solo ingresos
- [ ] Detalle por producto y por categoria
- [ ] Ticket promedio
- [ ] Top productos

### Dashboard

- [ ] `dashboard_view.py` con selector de periodo
- [ ] Tarjetas de indicador: ingresos, ticket promedio, unidades, tasa vigente
- [ ] `trend_chart.py`: grafica de evolucion
- [ ] Grafica de top productos
- [ ] Grafica de distribucion por categoria
- [ ] Graficas embebidas con `FigureCanvasTkAgg`
- [ ] Ejes legibles, sin decimales de mas, coherentes con la paleta
- [ ] Calculo en hilo secundario
- [ ] `report_view.py` con filtros y exportacion a Excel

### Alertas

- [ ] `stock_alert_popup.py`: aviso al caer bajo el minimo
- [ ] El aviso dice **que talla** se agota y **cuantas unidades** faltan
- [ ] Dismissible
- [ ] `ReporteController` con el reporte de faltantes por talla, ordenado por
      urgencia

### Tests

- [ ] `test_report_service.py`: agregaciones correctas por periodo
- [ ] `test_report_service.py`: rango vacio devuelve cero, no error
- [ ] `test_stock_status.py`: los cuatro estados

**Criterio de salida:** los totales del reporte coinciden con las ventas
registradas, y el dashboard no se congela al calcular.

---

## Fase 6 - Empaquetado

**Objetivo:** un `.exe` que un usuario no tecnico instale con doble clic.

- [ ] `faith_store.spec` de PyInstaller
- [ ] Icono `.ico` y metadatos de version
- [ ] Las librerias de terceros incluidas correctamente
- [ ] **Probado en una maquina limpia, sin Python instalado**
- [ ] Base de datos creada en el primer arranque
- [ ] Permisos de escritura en la carpeta de instalacion resueltos
- [ ] `installer.iss` de Inno Setup
- [ ] Acceso directo en el menu de inicio
- [ ] Desinstalador limpio
- [ ] Verificado offline en Windows 10 y en Windows 11

**Criterio de salida:** el instalador corre en una VM limpia de Windows, sin
Python, con el cable de red desconectado, y la app abre.

---

## Fase 7 - QA, Pulido y Entrega

**Objetivo:** confianza para entregar.

### Carga y rendimiento

- [ ] 1000 productos, medir tiempo de importacion
- [ ] 5000 productos, medir tiempo de busqueda
- [ ] 5000 productos, medir tiempo de apertura del catalogo
- [ ] Confirmar que la interfaz responde durante operaciones largas
- [ ] Sin fugas de conexiones ni de memoria tras uso prolongado

### Funcional

- [ ] Recorrer los 11 criterios de aceptacion de `01_requisitos.md`
- [ ] Casos limite: 0 unidades, stock 0, precio 0, lista vacia
- [ ] Casos de error: stock insuficiente, codigo duplicado, sin permisos de escritura
- [ ] Importacion con archivo corrupto o con formato incorrecto
- [ ] Base de datos corrupta: el usuario recibe un mensaje, no un crash

### Pulido

- [ ] Revisar alineacion y espaciado de todas las vistas
- [ ] Revisar contraste de todos los textos
- [ ] Corregir TODOS los textos de la interfaz que esten en ingles
- [ ] Corregir TODOS los identificadores en espanol que quedaran
- [ ] Verificar el comportamiento al redimensionar en distintas resoluciones
- [ ] Verificar a 100% y 150% de zoom

### Entrega

- [ ] Guia de usuario en PDF, ilustrada, paso a paso
- [ ] Plantilla de Excel entregada junto al instalador
- [ ] `README.md` actualizado con instrucciones de uso
- [ ] Numero de version en `config.py`
- [ ] Merge a `main` con tag de version

**Criterio de salida:** los 11 criterios de aceptacion verificados, y los tres
entregables en manos del cliente.

---

## 8. Registro de Decisiones

Toda decision tecnica no prevista en los documentos, anotada aqui.

| Fecha | Decision | Motivo | Alternativas descartadas |
|-------|----------|--------|--------------------------|
| | | | |

Ejemplos de lo que debe anotarse:

- Sustitucion de una libreria del stack sugerido.
- Cambio de estructura de carpetas.
- Un umbral del semaforo distinto al default.
- Una excepcion a una regla de `03_convenciones.md`.
- Un criterio de aceptacion redefinido por acuerdo con el cliente.

---

## 9. Registro de Progreso

| Fecha | Fase | Completado | Notas |
|-------|------|------------|-------|
| | | | |

---

**Volver a:** `README.md`
