# 02 - Arquitectura

> Como estructurar el codigo. Este archivo define las fronteras entre capas y
> el modelo de datos. Las decisiones concretas de estructura de carpetas son
> tuyas; los limites entre capas no.

---

## 1. Idea Central

El problema que mas se repite en proyectos de escritorio es mezclar la logica
con la interfaz. Cuando eso pasa, probar es dificil, la interfaz se cuelga y
cada cambio rompe tres cosas.

La solucion es una separacion estricta de responsabilidades, donde **cada
capa puede entenderse y probarse sin las otras**.

---

## 2. Las Cuatro Capas

```
                    +-------------------------+
   El usuario  ---> |          VIEWS          |  Solo interfaz
                    |  CustomTkinter, widgets  |
                    +------------+------------+
                                 |
                          eventos / datos
                                 |
                    +------------v------------+
                    |      CONTROLLERS        |  El puente
                    |  Inyecta dependencias   |
                    +------------+------------+
                                 |
                          llamadas / filas
                                 |
                    +------------v------------+
                    |   MODELS  y  SERVICES   |  Logica y datos
                    |  Reglas, SQL, ETL, I/O  |
                    +------------+------------+
                                 |
                    +------------v------------+
                    |         SQLite           |  Persistencia
                    +-------------------------+
```

**Regla de oro:** las flechas solo bajan. Una capa nunca llama a la de arriba.

### 2.1 Views

Responsabilidad unica: mostrar datos y capturar eventos del usuario.

**Puede:**
- Crear y configurar widgets.
- Leer lo que el usuario escribe.
- Pedirle al controller que haga algo.
- Mostrar los datos que el controller le entrega.
- Mostrar mensajes de error al usuario.

**No puede:**
- Escribir SQL. Jamas.
- Abrir la base de datos.
- Contener reglas de negocio.
- Calcular totales, margenes o conversiones.
- Conocer la estructura de las tablas.
- Hacer I/O de disco, ni siquiera un `open()` sin hilo.

### 2.2 Controllers

Responsabilidad unica: traducir entre el mundo de la vista y el mundo de la
logica.

**Puede:**
- Recibir eventos de la vista.
- Llamar a models y services.
- Recibir resultados y pedirle a la vista que los muestre.
- Coordinar operaciones que tocan varios models.
- Lanzar operaciones pesadas en un hilo y recoger el resultado.

**No puede:**
- Crear widgets.
- Contener SQL.
- Contener reglas de negocio complejas. Si la tiene, va a un service.
- Instanciar sus propias dependencias.

### 2.3 Models

Responsabilidad unica: representar y validar los datos del negocio.

**Puede:**
- Atributar datos de una entidad.
- Validar invariantes del dominio.
- Calcular valores derivados: margen, total, estado del semaforo.
- Know nada de como se guardan los datos.

**No puede:**
- Importar `tkinter` ni `customtkinter`. Nunca.
- Ejecutar SQL.
- Hablar con la base de datos.

Un model es codigo Python puro. Se puede probar sin levantar la interfaz.

### 2.4 Services

Responsabilidad unica: operaciones que cruzan varios models o tocan el mundo
exterior.

**Puede:**
- Ejecutar SQL.
- Leer y escribir archivos.
- Importar y exportar Excel.
- Generar PDF.
- Hacer backups.
- Lanzar y manejar hilos.
- Orquestar una operacion transaccional.

**No puede:**
- Importar `tkinter` ni `customtkinter`. Nunca.
- Crear widgets.
- Hablar con la capa de vista.

---

## 3. Por que esta separacion

Tres razones concretas, no dogmas:

**1. Se puede probar sin interfaz.** El margen bruto, la conversion de moeda y
el semaforo de stock se prueban con `assert`. No hace falta abrir una ventana.
Una suite de tests que tarda 2 segundos en lugar de 2 minutos es una suite que
se ejecuta siempre.

**2. La interfaz no se cuelga.** Si toda consulta a la base de datos vive en la
capa de datos, es facil guaranteeing que corra en un hilo secundario. Regla
mecanica: si esta en `views/`, corre en el hilo principal; si esta en
`services/`, corre en hilo secundario.

**3. Cambiar una capa no rompe las otras.** Si la base de datos pasa de SQLite
a otro motor, solo cambian los services. Si la interfaz pasa de CustomTkinter
a otro toolkit, solo cambian las views. El nucleo del negocio no se toca.

---

## 4. Modelo de Datos

### 4.1 Diagrama

```
productos 1 ────────< variantes 1 ────────< ventas
                              │
                              └── product_id

productos         tiene N variantes (tallas)
variantes         es una talla concreta de un producto
ventas            registra la salida de N unidades de una variante
config_sistema    pares clave-valor de configuracion
tasas_bcv         historial de la tasa con su fecha
```

### 4.2 DDL de Referencia

Este es el esquema. Puedes ajustarlo si documentas el motivo, pero la forma
debe responder al dominio de `01_requisitos.md`.

```sql
-- Productos: la entidad base. El codigo es unico porque se escanea.
CREATE TABLE productos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo          TEXT    NOT NULL UNIQUE,
    nombre          TEXT    NOT NULL,
    categoria       TEXT,
    tipo            TEXT    NOT NULL DEFAULT 'ropa',
    costo_usd       REAL    NOT NULL DEFAULT 0.0,
    precio_usd      REAL    NOT NULL DEFAULT 0.0,
    imagen_path     TEXT,
    activo          INTEGER NOT NULL DEFAULT 1,
    creado_en       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (costo_usd  >= 0),
    CHECK (precio_usd >= 0),
    CHECK (tipo IN ('ropa', 'calzado'))
);

-- Variantes: una fila por talla, con su propio stock.
CREATE TABLE variantes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id     INTEGER NOT NULL,
    codigo_talla    TEXT    NOT NULL,
    stock_actual    INTEGER NOT NULL DEFAULT 0,
    stock_minimo    INTEGER NOT NULL DEFAULT 5,
    precio_ajuste   REAL    NOT NULL DEFAULT 0.0,
    activo          INTEGER NOT NULL DEFAULT 1,
    creado_en       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE,
    UNIQUE (producto_id, codigo_talla),
    CHECK (stock_actual  >= 0),
    CHECK (stock_minimo  >= 0)
);

-- Ventas: la tasa queda congelada en la fila.
CREATE TABLE ventas (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    variante_id           INTEGER NOT NULL,
    cantidad              INTEGER NOT NULL,
    precio_unitario_usd   REAL    NOT NULL,
    tasa_bcv_congelada    REAL    NOT NULL,
    total_usd             REAL    NOT NULL,
    total_bs              REAL    NOT NULL,
    total_usdt            REAL    NOT NULL,
    medio_pago            TEXT    NOT NULL DEFAULT 'usd',
    vendido_en            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (variante_id) REFERENCES variantes (id) ON DELETE RESTRICT,
    CHECK (cantidad > 0)
);

-- Tasas BCV con su fecha. Permite auditar el historico.
CREATE TABLE tasas_bcv (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha         DATE    NOT NULL UNIQUE,
    tasa          REAL    NOT NULL,
    registrado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (tasa > 0)
);

-- Configuracion como pares clave-valor.
CREATE TABLE config_sistema (
    clave            TEXT PRIMARY KEY,
    valor            TEXT NOT NULL,
    actualizado_en   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 4.3 Indice

| Indice | Columnas | Por que |
|--------|----------|--------|
| `idx_productos_codigo` | `productos(codigo)` | Unique ya crea indice, pero explicito por claridad |
| `idx_productos_nombre` | `productos(nombre)` | Busqueda por nombre |
| `idx_variantes_producto` | `variantes(producto_id)` | Listar tallas de un producto |
| `idx_ventas_fecha` | `ventas(vendido_en DESC)` | Reportes por periodo |

### 4.4 Decisiones de Diseno y su Por Que

| Decision | Motivo |
|----------|--------|
| `codigo` UNIQUE | Es el ID que se escanea. No puede haber dos productos con el mismo codigo. |
| `tasa_bcv_congelada` en `ventas` | El historico no se recalcula. Si guardamos solo la tasa actual, los reportes pasados se distorsionan. |
| `ON DELETE RESTRICT` en `ventas` | No se puede borrar una variante que ya tiene ventas. Se desactiva con `activo = 0`. |
| `ON DELETE CASCADE` en `variantes` | Si un producto no tiene ventas, sus tallas se van con el. |
| `activo` en vez de borrar | Soft delete. Preserva el historico y las referencias. |
| `CHECK` en vez de validacion solo en Python | La base se protege aunque alguien escriba SQL a mano. |
| `timestamps` en todas las tablas | Auditoria. "Cuando se creo y cuando se toco por ultima vez" resuelve el 80% de los soporte. |
| `CHECK (tipo IN ('ropa','calzado'))` | El dominio tiene un conjunto cerrado de tipos. La base lo hace explicito. |

### 4.5 Transacciones

Dos operaciones **deben** ser atomicas:

**Venta.** El descuento de stock y el registro de la venta van en la misma
transaccion.

```python
with database.transaction() as connection:
    variant = lock_variant(connection, variant_id)
    if variant.stock_actual < cantidad:
        raise InsufficientStock(variant.codigo_talla)
    decrement_stock(connection, variant_id, cantidad)
    insert_sale(connection, sale_data)
# Si algo fallo arriba, no hay venta ni descuento.
```

**Importacion de Excel.** Si una fila es invalida, no se importa nada. El
usuario no quiere descubrir 300 productos importados y 1 rejecting despues.

---

## 5. Modelo de Concurrencia

### 5.1 La Regla

> La interfaz solo se toca desde el hilo principal de la GUI.
> Todo lo demas vive en hilos secundarios y vuelve con `after(0, callback)`.

### 5.2 Patron de Worked Operation

```python
# En la vista: el usuario hace clic y recibe feedback inmediato
def on_click_backup(self) -> None:
    """Lanza el backup sin bloquear la interfaz."""
    self.backup_button.configure(state="disabled", text="Respaldando...")
    worker = Thread(
        target=self._backup_worker,
        daemon=True,
    )
    worker.start()

# En la vista: el metodo que corre fuera del hilo principal
def _backup_worker(self) -> None:
    """Clona la base de datos. No toca ningun widget."""
    try:
        destination = self.backup_service.backup_now()
    except Exception as error:
        self.root.after(0, self._on_backup_failed, error)
    else:
        self.root.after(0, self._on_backup_done, destination)

# Vuelve al hilo principal
def _on_backup_done(self, destination: Path) -> None:
    """Confirma el backup en la interfaz."""
    self.backup_button.configure(state="normal", text="Respaldar")
    self.status_label.configure(text=f"Backup guardado en {destination.name}")
```

### 5.3 Cual I/O Va en Hilo Secundario

| Operacion | Razon |
|-----------|-------|
| Consultas SQLite pesadas | Bloquean el event loop |
| Lectura de Excel | Un archivo de 5000 filas tarda segundos |
| Escritura de Excel | Idem, mas el costo de escribir |
| Generacion de PDF | Costo de layout no trivial |
| Backup de la base | Copia completa del archivo |
| Carga de imagenes | Decodificar un JPEG grande tarda |
| Limpieza de imagenes en disco | I/O de disco |

**No** va en hilo secundario:Actualizar un label, redibujar un widget, leer el
texto de un campo que el usuario esta escribiendo.

### 5.4 SQLite y Hilos

SQLite no maneja bien la concurrencia. Decisiones a tomar:

- **Recomendado:** una conexion por hilo, creada dentro del hilo. Nunca
  compartir un objeto `Connection` entre hilos.
- Activar `PRAGMA foreign_keys = ON` en **cada** conexion. Es por conexion, no
  global.
- `PRAGMA journal_mode = WAL` mejora la concurrencia de lectura.
- Para el backup, usar la API `Connection.backup()` en vez de copiar el archivo
  a mano: es seguro aunque haya escrituras en curso.

---

## 6. Estructura de Carpetas

**Sugerencia, no imposicion.** Respeta la idea: una capa por directorio, un
componente por archivo.

```
faith_store/
|
|-- main.py                  Arranque. Inyecta dependencias y abre la ventana.
|-- config.py                Constantes: paleta, rutas, umbrales, textos.
|-- requirements.txt         Dependencias.
|
|-- database/                Capa de persistencia
|   |-- connection.py        Gestion de conexiones y transacciones.
|   |-- schema.py            DDL. Todo el SQL de estructura en un lugar.
|   `-- repositories/        Uno por entidad. SQL de datos.
|       |-- product_repository.py
|       |-- variant_repository.py
|       |-- sale_repository.py
|       `-- rate_repository.py
|
|-- models/                  Logica de datos pura
|   |-- product.py           Entidad, margen, validaciones.
|   |-- variant.py           Entidad, semaforo, transiciones de stock.
|   |-- sale.py              Entidad, totales.
|   |-- exchange_rate.py     Entidad, conversiones.
|   |-- size_validator.py    Tallas de ropa y calzado.
|   |-- stock_status.py      Semaforo de tres estados.
|   `-- money.py             Aritmetica de moneda sin flotantes sueltos.
|
|-- services/                Operaciones y mundo exterior
|   |-- catalog_service.py   Orquesta CRUD de producto y variantes.
|   |-- sales_service.py     Venta atomica, con tasa congelada.
|   |-- search_service.py    Busqueda normalizada, con debounce.
|   |-- import_service.py    ETL de Excel, transaccional.
|   |-- export_service.py    Exportacion a Excel.
|   |-- backup_service.py    Clone de la base con fecha y hora.
|   |-- pdf_service.py       Tickets y reportes en PDF.
|   |-- report_service.py    Agregaciones por periodo.
|   |-- text_normalizer.py   NFD, sin tildes, minusculas.
|   `-- rate_service.py      Gestion de la tasa BCV.
|
|-- views/                   Solo interfaz
|   |-- main_window.py       Ventana raiz: sidebar, topbar, contenedor.
|   |-- catalog_view.py      Modulo de catalogo.
|   |-- pos_view.py          Modulo de punto de venta.
|   |-- dashboard_view.py    Modulo de metricas.
|   |-- report_view.py       Modulo de reportes.
|   |-- settings_view.py     Modulo de configuracion.
|   `-- components/          Widgets reutilizables, uno por archivo
|       |-- product_card.py
|       |-- size_pill.py
|       |-- stock_bar.py
|       |-- stock_badge.py
|       |-- search_bar.py
|       |-- search_suggestion.py
|       |-- money_pill.py
|       |-- trend_chart.py
|       |-- sidebar.py
|       |-- topbar.py
|       |-- empty_state.py
|       `-- toast.py         Aviso temporal no bloqueante.
|
|-- controllers/             Puente
|   |-- catalog_controller.py
|   |-- pos_controller.py
|   |-- dashboard_controller.py
|   |-- report_controller.py
|   `-- settings_controller.py
|
|-- tests/
|   |-- test_product.py
|   |-- test_variant.py
|   |-- test_stock_status.py
|   |-- test_money.py
|   |-- test_sales_service.py
|   |-- test_search.py
|   |-- test_import.py
|   |-- test_backup.py
|   |-- test_rate.py
|   `-- test_acceptance.py   Criterios de aceptacion, end to end.
|
`-- assets/                  Recursos estaticos
    |-- icons/
    |-- fonts/
    `-- templates/
        `-- plantilla_inventario.xlsx
```

### 6.1 La Regla del Archivo Unico

Una clase, un archivo. Si un archivo pasa de 200 lineas, algo tiene mas de una
responsabilidad.

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| Vista de 400 lineas | UI mezclada con datos | Extraer a `views/components/` |
| Metodo de 80 lineas | Hace tres cosas | Partirlo en tres |
| Controller enorme | Tiene reglas de negocio | Mover el negocio a `services/` |

---

## 7. Configuracion Centralizada

`config.py` es la unica fuente de verdad. Todos los valores que se puedan
cambiar sin reescribir logica van alla.

```python
# config.py
APP_NAME = "Faith Store"
APP_VERSION = "1.0.0"

# Paleta
BG_PRIMARY = "#F3F4F8"
BG_SURFACE = "#FFFFFF"
TEXT_PRIMARY = "#1C1C1E"
TEXT_MUTED = "#6E6E73"
ACCENT_BLUE = "#0066FF"
STOCK_GREEN = "#34C759"
STOCK_RED = "#FF3B30"
STOCK_YELLOW = "#FF9500"

# Umbrales del semaforo
STOCK_MULTIPLIER_MEDIUM = 1.0
STOCK_MULTIPLIER_HIGH = 2.0
DEFAULT_STOCK_MINIMUM = 5

# Temporales
SEARCH_DEBOUNCE_MS = 300

# Rutas
DATA_DIR = Path.home() / "FaithStore"
DB_PATH = DATA_DIR / "faith_store.db"
BACKUP_DIR = DATA_DIR / "backups"
```

**Prohibido** escribir `#34C759` dentro de una vista. Se importa de `config.py`.

---

## 8. Manejo de Errores

### 8.1 Jerarquia

```
FaithStoreError              Base. Todo error de dominio hereda de aqui.
|
|-- ValidationError          Dato invalido. Se muestra al usuario.
|-- NotFoundError            No existe. Se muestra al usuario.
|-- InsufficientStockError   No hay stock. Se muestra al usuario con la talla.
|-- DuplicateCodeError       Codigo repetido. Se muestra al usuario.
|-- ImportValidationError    Importacion fallida. Lista de errores por fila.
|-- DatabaseError            Fallo de SQLite. Se registra, no se muestra crudo.
|-- FileOperationError       Fallo de disco. Se registra y se explica.
```

### 8.2 Principio

- **Errores de dominio:** excepciones tipadas, mensaje en espanol, pensados
  para mostrarse.
- **Errores inesperados:** se registran con detalle tecnico y se muestra un
  mensaje generico. El usuario nunca ve un traceback.
- **En la vista:** se captura en el borde, nunca en medio de un metodo. El
  usuario no debe ver una excepcion en un click.

```python
# En la vista: un unico manejador en el borde
def on_save_click(self) -> None:
    """Guarda el producto y comunica el resultado al usuario."""
    try:
        self.controller.save_product(self._collect_form_data())
    except DuplicateCodeError as error:
        self._show_field_error("codigo", str(error))
    except ValidationError as error:
        self._show_dialog("Datos invalidos", str(error))
    except Exception as error:
        logger.exception("Fallo inesperado al guardar el producto")
        self._show_dialog("Error inesperado", "Ocurrio un problema. Intente de nuevo.")
    else:
        self._show_toast("Producto guardado")
```

---

## 9. Ciclo de Vida de la Aplicacion

```
Arranque
  |
  +-- Crear directorio de datos si no existe
  +-- Abrir base de datos
  +-- Crear esquema si es la primera vez
  +-- Insertar configuracion por defecto
  +-- Cargar tasa BCV vigente
  +-- Construir capas con dependencias inyectadas
  +-- Mostrar ventana principal
  |
Cierre
  +-- Cerrar conexiones
  +-- Confirmar backup si hay cambios sin respaldar (opcional)
  +-- Liberar recursos
```

**El arranque debe ser rapido.** Mostrar la ventana antes de cargar datos
pesados. La base con 5000 productos debe abrir en menos de 2 segundos.

---

**Siguiente:** `03_convenciones.md`
