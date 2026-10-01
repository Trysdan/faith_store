# AGENTS.md - Reglas de Trabajo para Faith Store

> **Que es este archivo:** Como debe trabajar cualquier agente o persona en este
> codigo. Leer DESPUES de `PROJECT_CONTEXT.md`.
>
> Si una regla aqui contradice a una costumbre personal, estas ganan.

---

## 1. Regla #1 - Un Archivo Por Clase

Cada clase vive en su propio archivo `.py`.

```
Bien:  models/product_model.py   -> class ProductModel
Mal:   models/models.py          -> class ProductModel, class VariantModel, ...
```

**Limite de tamano: 150 a 200 lineas por archivo.** Si un archivo se pasa, esta
mal diseñado. Las causas mas comunes y su solucion:

| Sintoma | Causa real | Solucion |
|---------|-----------|----------|
| La vista tiene 400 lineas | Logica de UI mezclada con datos | Extraer a `views/components/` |
| El metodo tiene 80 lineas | Hace 3 cosas | Partir en 3 metodos |
| El controlador crece mucho | Tiene reglas de negocio | Mover a `services/` |

## 2. Regla #2 - Estructura de Capas (MVC)

```
models/       Logica de datos pura. Cero imports de tkinter o customtkinter.
services/     Reglas de negocio, ETL, hilos, integraciones externas.
views/        Solo UI. Cero SQL. Cero reglas de negocio.
controllers/  Puente Model <-> View. Inyecta dependencias, no las crea.
```

**Prohibiciones absolutas (no negociables):**

- SQL o llamadas a BD dentro de `views/`. Jamas.
- `import tkinter` o `import customtkinter` dentro de `models/` o `services/`.
- Instanciar dependencias dentro de un consumidor. Se inyectan por `__init__`.
- `from modulo import *`. Siempre imports explicitos.

**Flujo de datos permitido:**

```
View  --evento-->  Controller  --llama-->  Model/Service  --consulta-->  SQLite
View  <--render--  Controller  <--datos--  Model/Service  <--filas---  SQLite
```

## 3. Regla #3 - Estilo de Codigo

### Identificadores en INGLES. Comentarios en ESPANOL.

```python
# Correcto
def calculate_gross_margin(self, sale_price: float) -> float:
    """Calcula el margen bruto en porcentaje.

    Args:
        sale_price: Precio de venta unitario.

    Returns:
        float: Margen bruto expresado en porcentaje.
    """
    # Se evita la division por cero cuando no hay precio de venta
    if sale_price <= 0:
        return 0.0
    return round(((sale_price - self.cost_price) / sale_price) * 100, 2)
```

```python
# Incorrecto
def calcular_margen_bruto(self, precio_venta: float) -> float:
    """Calcula el margen bruto en porcentaje.  # Docstring en espanol
    if precio_venta <= 0:
        return 0.0
```

| Elemento | Convencion | Ejemplo |
|----------|-----------|---------|
| Clases | `PascalCase` | `ProductModel`, `CatalogController` |
| Funciones, variables | `snake_case` | `calculate_margin`, `stock_quantity` |
| Constantes | `UPPER_SNAKE_CASE` | `STOCK_GREEN`, `DEFAULT_BCV_RATE` |
| Metodos privados | `_prefijo_underscore` | `_on_search_keypress` |
| Docstrings | PEP 257, en ingles | Ver ejemplo arriba |
| Comentarios inline | Espanol, sin tildes | `# Verifica el stock minimo` |

**Reglas adicionales:**

- **Tipado explicito obligatorio** en todo parametro y retorno.
- **Lineas de 79 caracteres maximo.** Usa hanging indent para argumentos largos.
- **Imports en 3 bloques**, separados por linea en blanco, en este orden:
  1. Libreria estandar
  2. Libreria de terceros
  3. Modulos locales
- Docstrings obligatorios en toda clase publica y todo metodo publico.
- Sin emojis ni acentos en los identificadores del codigo.

## 4. Regla #4 - UI Resiliente

### Prohibido `.place()`. Solo `grid` y `pack`.

```python
# Prohibido
label.place(x=10, y=20, width=300)

# Correcto - grid con pesos para que sea elastico
self.frame.grid_columnconfigure(1, weight=1)
label.grid(row=0, column=1, sticky="ew", padx=8)
```

Motivo: `.place()` con coordenadas absolutas se rompe al redimensionar la
ventana y no soporta el escalado DPI de pantallas HD/FHD.

### Todo I/O va en hilo secundario

Consultas SQLite pesadas, lectura/escritura de Excel, backups y generacion de PDF
**nunca** pueden correr en el hilo principal. Congelan la interfaz.

```python
from threading import Thread

def on_click_export(self) -> None:
    """Dispara la exportacion en segundo plano."""
    worker = Thread(target=self._export_worker, daemon=True)
    worker.start()
    self.status_label.configure(text="Exportando...")

def _export_worker(self) -> None:
    """Ejecuta la exportacion. Corre fuera del hilo de la GUI."""
    rows = self.excel_service.export_sales()   # I/O pesada
    self.root.after(0, self._on_export_done, rows)  # Vuelta al hilo GUI
```

**Invariante:** nunca se toca un widget de Tkinter desde un hilo secundario.
Solo mediante `root.after(0, callback)`.

## 5. Regla #5 - Constantes Centralizadas

`config.py` es la unica fuente de verdad para:

- Paleta de colores
- Rutas de archivos y recursos
- Umbrales de stock
- Nombres de columnas de la BD
- Parametros de la aplicacion

**Prohibido** escribir un color hex o una ruta como literal dentro de `views/`.

## 6. Regla #6 - Git

### Ramas

| Rama | Uso | Regla |
|------|-----|-------|
| `main` | Produccion | Solo codigo verificado y testeado. Es la default. |
| `develop` | Trabajo activo | Aqui se construye modulo a modulo. |

### Flujo de trabajo

```bash
# 1. Antes de empezar, confirmar que estas en develop
git checkout develop
git pull origin develop

# 2. Trabajar en un modulo, con tests pasando

# 3. Commit y push
git add .
git commit -m "feat(catalog): Add size matrix with independent stock per variant"
git push origin develop

# 4. Al cerrar un modulo completo, integrar a produccion
git checkout main
git merge develop
git tag -a v1.0.0 -m "Catalogo y matriz de tallas completo"
git push origin main --tags
git checkout develop
```

### Formato de commits (Conventional Commits)

```
<tipo>(<modulo>): <descripcion en imperativo y en ingles>

tipos:  feat | fix | refactor | test | docs | chore | perf
```

Ejemplos validos:

```
feat(catalog): Add product card with stock semaphore
fix(search): Normalize accents before comparing queries
refactor(db): Extract schema into dedicated migrations module
test(sales): Cover frozen exchange rate on sale creation
```

### Reglas de commit

- Un commit = una unidad logica de cambio.
- **Nunca** se hace commit con tests fallando.
- **Nunca** se hace commit de secretos, tokens ni claves.
- No mezclar refactor con funcionalidad en el mismo commit.

## 7. Regla #7 - Testing

Cada archivo de teste sigue la misma regla de 150-200 lineas.

```bash
# Suite completa
python -m pytest tests/ -v

# Un archivo
python -m pytest tests/test_product_model.py -v

# Un caso especifico
python -m pytest tests/test_product_model.py::TestProductModel::test_margin -v
```

**Cobertura minima obligatoria por modulo:**

- Camino feliz del caso principal
- Al menos un caso limite (0, negativo, vacio, None)
- Al menos un caso de error (dato invalido, FK violada)

**Patron para datos de prueba:** `tmp_path` de pytest o `:memory:` de SQLite.
Nunca tocar la base de datos real de desarrollo en un test.

```python
def test_connection_uses_memory_db(tmp_path: Path) -> None:
    """Verifica que la conexion de prueba no toque la BD real."""
    db_file = tmp_path / "test.db"
    with DatabaseConnection(str(db_file)) as conn:
        ...
    assert db_file.exists()
```

## 8. Checklist Antes de Commit

Antes de cada commit, verificar:

- [ ] Cada clase esta en su propio archivo
- [ ] Ningun archivo supera 200 lineas
- [ ] No hay SQL en `views/`
- [ ] No hay imports de tkinter en `models/` o `services/`
- [ ] No hay `.place()` en ninguna vista
- [ ] No hay `import *`
- [ ] Todo parametro y retorno tiene type hint
- [ ] Docstrings en clases y metodos publicos
- [ ] Identificadores en ingles, comentarios en espanol
- [ ] Colores y rutas vienen de `config.py`
- [ ] Las operaciones de I/O estan en hilo secundario
- [ ] `python -m pytest tests/ -v` pasa completo
- [ ] El mensaje de commit sigue Conventional Commits

## 9. Definition of Done por Modulo

Un modulo esta terminado cuando:

1. Todos los archivosrespectan las reglas de este documento.
2. Hay tests que pasan y cubren los casos principais.
3. La funcionalidad se puede ejecutar y verificar desde `main.py`.
4. Hay commit en `develop` con mensaje claro.
5. El avance esta marcado en `ROADMAP.md`.

---

**Siguiente archivo:** `ROADMAP.md` (que falta construir y en que orden).
