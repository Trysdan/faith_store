# 03 - Convenciones de Codigo

> Como se escribe el codigo en este proyecto. Estas reglas son obligatorias.
> Define el estilo, no el comportamiento. El comportamiento esta en
> `01_requisitos.md`.

---

## 1. Idioma

Esta es la convencion mas importante y la que mas se olvida.

| Elemento | Idioma | Ejemplo |
|----------|--------|---------|
| Clases, funciones, variables, constantes | **Ingles** | `ProductModel`, `stock_quantity`, `calculate_margin` |
| Nombres de archivo | **Ingles** | `product_model.py`, `stock_status.py` |
| Docstrings | **Ingles** | `"""Calcula el margen bruto en porcentaje."""` |
| Comentarios | **Espanol** | `# Verifica el stock minimo` |
| Texto de la interfaz | **Espanol** | `"Buscar producto por nombre o ID..."` |
| Mensajes de error al usuario | **Espanol** | `"No hay stock suficiente en la talla M"` |

### 1.1 Por que esta mezcla

El codigo se lee en ingles porque es el idioma estandar de la industria y
porque las librerias y la documentacion estan en ingles. Los comentarios van en
espanol porque quien los va a leer en el futuro, seis meses despues, es el
equipo local.

### 1.2 Ejemplo completo, correcto

```python
class ProductModel:
    """Product entity for the Faith Store inventory.

    Holds the descriptive and financial data of a product. Stock lives in
    the variants, not here, because each size is tracked independently.

    Attributes:
        product_id: Database identifier. None until persisted.
        code: Unique scannable code (e.g., 'PN-001').
        name: Product display name.
        cost_usd: Unit acquisition cost in US dollars.
        sale_price_usd: Unit selling price in US dollars.
    """

    def __init__(
        self,
        code: str,
        name: str,
        cost_usd: float = 0.0,
        sale_price_usd: float = 0.0,
        product_id: int | None = None,
    ) -> None:
        """Initialize a product with its financial data.

        Args:
            code: Unique scannable product code.
            name: Product display name.
            cost_usd: Unit acquisition cost. Non-negative.
            sale_price_usd: Unit selling price. Non-negative.
            product_id: Database identifier, or None for a new product.

        Raises:
            ValidationError: If code is empty or any price is negative.
        """
        # Se valida el codigo porque es la clave de busqueda por escaner
        if not code or not code.strip():
            raise ValidationError("El codigo del producto es obligatorio")

        self.product_id = product_id
        self.code = code.strip().upper()
        self.name = name.strip()
        self.cost_usd = max(0.0, cost_usd)
        self.sale_price_usd = max(0.0, sale_price_usd)

    @property
    def gross_margin_pct(self) -> float:
        """Calculate the gross profit margin as a percentage.

        Uses the standard retail formula. Returns 0.0 when the selling price
        is zero, to avoid a division by zero. A negative result means the
        product sells at a loss and must be highlighted in the interface.

        Returns:
            float: Gross margin percentage. 40.0 means 40 percent.

        Examples:
            >>> product = ProductModel("PN-001", "Polo", 15.0, 25.0)
            >>> product.gross_margin_pct
            40.0
        """
        if self.sale_price_usd <= 0:
            return 0.0
        margin = (self.sale_price_usd - self.cost_usd) / self.sale_price_usd
        return round(margin * 100, 2)
```

### 1.3 Ejemplo completo, incorrecto

```python
# MAL: identificadores en espanol
class ProductoModelo:
    def calcular_margen_bruto(self, precio_venta: float) -> float:
        """Calcula el margen.  # MAL: docstring en espanol
        if precio_venta <= 0:  # MAL: variable en espanol
            return 0.0

# BIEN: identificadores en ingles, docstring en ingles, comentario en espanol
class ProductModel:
    def calculate_gross_margin(self, sale_price: float) -> float:
        """Calculates the gross profit margin percentage."""
        # Se devuelve cero cuando no hay precio de venta
        if sale_price <= 0:
            return 0.0
```

---

## 2. Formato de Docstrings

PEP 257. Obligatorio en toda clase publica y todo metodo publico.

### 2.1 Plantilla

```python
def method_name(
    first_arg: Type,
    second_arg: Type,
) -> ReturnType:
    """One-line summary in English, ending with a period.

    Optional longer description. Explain the reasoning behind non-obvious
    decisions, not the mechanics of the code.

    Args:
        first_arg: What it is, expected format, and constraints.
        second_arg: Same detail. Mark optional values.

    Returns:
        ReturnType: What comes back and under which conditions.

    Raises:
        SpecificErrorName: The condition that triggers it.

    Examples:
        >>> example_call()
        expected_result
    """
```

### 2.2 Reglas

| Regla | Bien | Mal |
|-------|------|-----|
| Una linea en el resumen | `"""Sets the active variant."""` | `"""Este metodo establece la variante activa que se ha seleccionado en el catalogo de productos."""` |
| Termina en punto | `"""Calcula el total."""` | `"""Calcula el total"""` |
| Empieza con verbo | `"""Returns the stock status."""` | `"""The stock status is returned."""` |
| `Args:` alineado y con tipo | `price: Unit price in USD.` | `price: el precio` |
| `Returns:` siempre en funciones que devuelven | - | omitir el `Returns:` |
| Sin lineas en blanco dentro | ver 1.2 | doble linea en blanco |

---

## 3. Comentarios

**Idioma:** espanol, solo caracteres ASCII, sin tildes ni enie.

```python
# MAL
# Verifica que el precio de venta sea mayor que el costo minimo

# BIEN
# Verifica que el precio de venta sea mayor que el costo minimo
```

**Que comentar:**

| Comentar | No comentar |
|----------|-------------|
| El **por que**, no el **que** | `# i = i + 1` |
| Decisiones no obvias | `# Llama al metodo` |
| Workarounds y sus motivos | `# Asigna la variable` |
| Numeros magicos | `# Incrementa el contador` |

```python
# MAL: el codigo ya lo dice
# Calcula el margen
margin = (sale_price - cost) / sale_price * 100

# BIEN: explica la decision
# Se usa el costo promedio ponderado para que el margen refleje el stock real
margin = (sale_price - weighted_average_cost) / sale_price * 100
```

---

## 4. Nombres

### 4.1 Convenciones

| Elemento | Convencion | Ejemplo |
|----------|------------|---------|
| Clase | `PascalCase` | `ProductModel`, `CatalogController` |
| Funcion, metodo, variable | `snake_case` | `calculate_margin`, `stock_quantity` |
| Constante | `UPPER_SNAKE_CASE` | `STOCK_GREEN`, `DEFAULT_BCV_RATE` |
| Metodo privado | `_prefijo` | `_on_search_keypress` |
| Atributo de clase / instancia | `snake_case` | `self.db_path` |
| Modulo | `snake_case` | `search_service.py` |
| Evento de tkinter | `_on_` + evento | `_on_button_click` |
| Query method | Verbo en imperativo | `find_by_code`, `list_active` |

### 4.2 Nombres que dicen mas

| Mal | Bien | Por que |
|-----|------|---------|
| `data` | `products`, `sales_rows` | Que datos son |
| `result` | `margin_pct`, `total_usd` | Que representa |
| `flag` | `is_active`, `has_stock` | Que condicion |
| `temp` | `accumulated_margin` | Para que sirve |
| `handler` | `on_delete_clicked` | Que evento maneja |
| `process` | `import_excel_file` | Que hace |
| `i`, `j` | `row_index`, `column_index` | Que recorre |

### 5. Tipado

Obligatorio en **todos** los parametros y **todos** los retornos.

```python
from __future__ import annotations

def calculate_margin(cost: float, price: float) -> float:
    """Calcula el margen bruto en porcentaje."""
    ...

def find_by_code(self, code: str) -> ProductModel | None:
    """Busca un producto por su codigo unico."""
    ...

def get_stock_status(self) -> StockStatus:
    """Determina el estado del semaforo de stock."""
    ...
```

**Reglas de tipado:**
- `from __future__ import annotations` al inicio de cada archivo, si usas
  anotaciones modernas.
- Evita `Any` salvo que sea inevitable. Prefiere `object` o un tipo concreto.
- Las variables de clase se anotan: `stock_quantity: int = 0`.
- `None` se escribe `Optional[X]` o `X | None`.

---

## 6. Layout

| Regla | Valor |
|-------|-------|
| Longitud maxima de linea | 79 caracteres |
| Indentacion | 4 espacios, nunca tabs |
| Lineas en blanco entre metodos | 1 |
| Continuacion de argumentos | Hanging indent, alineado al parentesis |
| Strings largos | Concatenacion explicita o parentesis, nunca implicit |

```python
# MAL: linea larga
def registrar_producto(codigo: str, nombre: str, categoria: str, costo: float) -> bool:

# BIEN: hanging indent
def registrar_producto(
    codigo: str,
    nombre: str,
    categoria: str,
    costo: float,
) -> bool:
```

---

## 7. Imports

Tres bloques, separados por una linea en blanco, siempre en este orden:

```python
# 1. Libreria estandar
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# 2. Librerias de terceros
import customtkinter
import pandas

# 3. Modulos locales
from config import APP_NAME
from models.product import ProductModel
from services.catalog_service import CatalogService
```

**Prohibido** `from modulo import *`. Siempre explicito.

**Orden alfabetico** dentro de cada bloque. El IDE lo ordena automaticamente.

---

## 8. Limites de Archivo

| Elemento | Limite | Si se excede |
|----------|--------|--------------|
| Archivo | 200 lineas | Partir. Likely mas de una responsabilidad. |
| Metodo | 30 lineas | Hace mas de una cosa. Partirlo. |
| Clase | 200 lineas | Demasiadas responsabilidades. |

Como partir:

| Sintoma | Solucion |
|---------|----------|
| Vista de 400 lineas | Extraer componentes a `views/components/` |
| Metodo de 80 lineas | Partir en 2 o 3 metodos |
| Service con 10 metodos publicos | Dividir por caso de uso |
| Repository con SQL de 5 tablas | Un repository por entidad |

---

## 9. Prohibiciones

Estas no se negocian. Un revisor debe rechazar el cambio.

| Prohibido | Por que |
|-----------|---------|
| `from x import *` | Ensucia el namespace, oculta de donde viene cada nombre |
| SQL en `views/` | Rompe la separacion de capas |
| `import tkinter` en `models/` o `services/` | La logica no debe depender de la GUI |
| `.place()` | Se rompe al redimensionar y no escala con DPI |
| Color hex literal en `views/` | La paleta vive en `config.py` |
| Numero magico sin nombre | Usa constantes |
| `except:` sin tipo | Oculta errores reales |
| `except Exception: pass` | Traga el error sin dejar rastro |
| Capturar excepcion y no hacer nada | O se maneja o se propaga |
| I/O en el hilo de la GUI | Congela la interfaz |
| `time.sleep` en hilo principal | Congela la interfaz |
| Commit con tests fallando | Rompe la promesa de `main` |
| Un commit que hace refactor y funcionalidad | Dificil de revisar y de revertir |

---

## 10. Git

### 10.1 Ramas

| Rama | Contenido |
|------|-----------|
| `main` | Solo codigo verificado y testeado. Es la rama por defecto del repo. |
| `develop` | Trabajo activo. Aqui se construye modulo a modulo. |

### 10.2 Ciclo de trabajo

```bash
git checkout develop
git pull origin develop

# ... trabajar, con tests pasando ...

git add .
git commit -m "feat(catalog): Add size matrix with independent stock per variant"
git push origin develop
```

Al cerrar un modulo completo:

```bash
git checkout main
git merge develop
git tag -a v0.1.0 -m "Catalogo y matriz de tallas completo"
git push origin main --tags
git checkout develop
```

### 10.3 Formato de Commits

Conventional Commits:

```
<tipo>(<modulo>): <descripcion en imperativo, en ingles, en_minusculas>
```

| Tipo | Cuando |
|------|--------|
| `feat` | Funcionalidad nueva |
| `fix` | Correccion de bug |
| `refactor` | Reestructuracion sin cambio de comportamiento |
| `test` | Solo tests |
| `docs` | Solo documentacion |
| `chore` | Mantenimiento, dependencias, configuracion |
| `perf` | Mejora de rendimiento |

Ejemplos:

```
feat(catalog): Add size matrix with independent stock per variant
fix(search): Normalize accents before comparing queries
refactor(db): Extract schema into dedicated module
test(sales): Cover frozen exchange rate on sale creation
docs(readme): Add offline install instructions
chore(deps): Pin matplotlib to 3.9
```

### 10.4 Reglas

- Un commit, una unidad logica de cambio.
- Nunca con tests fallando.
- Nunca secretos, tokens ni claves.
- No mezclar refactor con funcionalidad.
- El mensaje dice **que** cambio y **por que** si no es obvio.

---

## 11. Testing

### 11.1 Que exige la regla de aceptacion

Cada modulo necesita cobertura de tres casos minimos:

| Tipo de caso | Ejemplo |
|--------------|---------|
| Camino feliz | Venta normal de 2 unidades con stock suficiente |
| Limite | Venta de 0 unidades, stock en 0, precio en 0, lista vacia |
| Error | Stock insuficiente, codigo duplicado, FK violada |

### 11.2 Reglas

- Una funcion de test, un comportamiento.
- El nombre describe el comportamiento, no la funcion.
- **Los datos de prueba son english.** El usuario ve espanol, el codigo
  ingles.
- Nunca tocar la base de datos real en un test. Usar `:memory:` de SQLite o
  `tmp_path` de pytest.
- Un test debe fallar por una sola razon. Si falla por varias, dividelo.
- Sin dependencias entre tests. Cada test monta su propio escenario.
- Sin `sleep`. Si hay concurrencia, probar la logica sin ella.

### 11.3 Nombres de Test

```python
# El nombre describe el comportamiento esperado
def test_margin_returns_zero_when_sale_price_is_zero() -> None:
    """Verifica que el margen sea cero sin precio de venta."""
    ...

def test_sale_rejects_when_stock_is_insufficient() -> None:
    """Verifica que la venta falle si no hay stock suficiente."""
    ...

def test_search_finds_accented_word_from_unaccented_query() -> None:
    """Verifica que 'pantalon' encuentre 'Pantalón'."""
    ...
```

### 11.4 Documentacion de Tests

Docstrings de test: **en ingles**, consistentes con el resto del codigo.

```python
def test_search_finds_accented_word_from_unaccented_query() -> None:
    """Verify the search matches 'Pantalón' when the user types 'pantalon'.

    Covers the accent-insensitivity requirement from the functional spec.
    """
    # Se guarda con tilde y se busca sin tilde
    repository.save(ProductModel(code="PN-001", name="Pantalón"))
    results = service.search("pantalon")
    assert len(results) == 1
```

### 11.5 Ejecutar

```bash
python -m pytest tests/ -v                          # Todo
python -m pytest tests/test_sales.py -v             # Un archivo
python -m pytest tests/test_sales.py::test_x -v     # Un caso
python -m pytest tests/ --cov=models --cov=services # Con cobertura
```

---

## 12. Checklist Antes de Commit

- [ ] Una clase por archivo, ninguno pasa de 200 lineas
- [ ] No hay SQL en `views/`
- [ ] No hay `import tkinter` en `models/` ni `services/`
- [ ] No hay `.place()` en ninguna vista
- [ ] No hay `from x import *`
- [ ] Todos los parametros y retornos tienen type hint
- [ ] Docstrings en clases y metodos publicos
- [ ] Identificadores en ingles, comentarios en espanol sin tildes
- [ ] Colores y rutas vienen de `config.py`
- [ ] La I/O pesada esta en hilo secundario
- [ ] Los tests pasan: `python -m pytest tests/ -v`
- [ ] El mensaje de commit sigue Conventional Commits

---

**Siguiente:** `04_interfaz.md`
