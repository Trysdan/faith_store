# UI_SPEC.md - Especificacion Visual de Faith Store

> **Que es este archivo:** Como se ve la aplicacion. Leer antes de tocar
> cualquier archivo en `views/`.
>
> Todos los valores de esta tabla van en `config.py`. **Prohibido** escribir un
> hex o un radio como literal dentro de una vista.

---

## 1. Estilo

**Windows 11 Fluent UI Light.** Bordes redondeados, paleta clara con contrastes
suaves, tarjetas independientes, indicadores visuales de estado.

## 2. Paleta

| Elemento | Hex | Constante en `config.py` |
|----------|-----|--------------------------|
| Fondo principal | `#F3F4F8` | `BG_PRIMARY` |
| Fondo tarjetas y sidebar | `#FFFFFF` | `BG_SURFACE` |
| Texto principal | `#1C1C1E` | `TEXT_PRIMARY` |
| Texto secundario | `#6E6E73` | `TEXT_MUTED` |
| Acento azul | `#0066FF` | `ACCENT_BLUE` |
| Acento azul hover | `#1D63ED` | `ACCENT_BLUE_HOVER` |
| Estado optimo (verde) | `#34C759` | `STOCK_GREEN` |
| Fondo estado optimo | `#DCFCE7` | `STOCK_GREEN_BG` |
| Alerta stock bajo (rojo) | `#FF3B30` | `STOCK_RED` |
| Fondo alerta stock bajo | `#FEE2E2` | `STOCK_RED_BG` |
| Alerta media (amarillo) | `#FF9500` | `STOCK_YELLOW` |
| Fondo alerta media | `#FEF3C7` | `STOCK_YELLOW_BG` |
| Navegacion activa | `#E5E7EB` | `NAV_ACTIVE_BG` |
| Pildoras y tags | `#F3F4F6` | `BG_PILL` |
| Bordes sutiles | `#E5E7EB` | `BORDER_SUBTLE` |

Limite de la paleta: 3 colores primarios (azul de acento, verde de estado
optimo, rojo de alerta). Los neutros son parte del tema, no lo cuentan.

## 3. Radios y Tipografia

| Elemento | Valor | Constante |
|----------|-------|-----------|
| Botones y barra de busqueda | `corner_radius=20` | `RADIUS_PILL` |
| Tarjetas de producto | `corner_radius=14` | `RADIUS_CARD` |
| Paneles y sidebar | `corner_radius=16` | `RADIUS_PANEL` |
| Badges y pildoras | `corner_radius=8` | `RADIUS_BADGE` |
| Pildoras de talla | `corner_radius=6` | `RADIUS_SIZE` |
| Padding interno de tarjeta | `15` | `CARD_PADDING` |

Fuente: `("Segoe UI", tamano)`. Pesos: `normal` para texto, `"bold"` para titulos.

## 4. Estructura de la Ventana

```
┌──────────────┬────────────────────────────────────────────────┐
│              │  TopBar:  [ 🔍 Buscar producto... ]  ↑  🔒    │
│  Sidebar     ├────────────────────────────────────────────────┤
│  width=220   │                                                │
│              │  CTkScrollableFrame  (fg_color=BG_PRIMARY)     │
│  ☰           │  ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│              │  │  Card 1    │ │  Card 2    │ │  Card 3    │  │
│  Dashboard   │  └────────────┘ └────────────┘ └────────────┘  │
│  Inventario  │  ┌────────────┐ ┌────────────┐                │
│  Ventas      │  │  Card 4    │ │  Card 5    │                │
│  Reportes    │  └────────────┘ └────────────┘                │
│  Config      │                                                │
└──────────────┴────────────────────────────────────────────────┘
```

### 4.1 Sidebar

- Ancho fijo `220`.
- Boton `☰` arriba.
- Items de navegacion como `CTkButton` con `fg_color="transparent"`.
- Item activo: `fg_color=NAV_ACTIVE_BG`, texto en `TEXT_PRIMARY` y `"bold"`.
- Indicador lateral azul de 3 px sobre el item activo.

```python
# config.py
SIDEBAR_WIDTH = 220
NAV_ACTIVE_INDICATOR_WIDTH = 3
```

### 4.2 TopBar

- `CTkEntry` central, `corner_radius=20`, `border_width=1`,
  `fg_color=BG_SURFACE`, placeholder
  `"Buscar producto por nombre o ID..."`.
- Botones circulares transparentes a la derecha: backup (`↑`) y bloqueo (`🔒`).

### 4.3 Area de Contenido

- Un solo `CTkScrollableFrame` con `fg_color=BG_PRIMARY`.
- Las tarjetas se colocan en un grid de 3 columnas.
- Cada columna con `weight=1` para que el grid sea elastico al redimensionar.
- El alto del canvas se recalcula con `<Configure>` para que el scroll mida bien.

```python
# Importante: sin esto el scrollbar no mide el alto del contenido
def _on_frame_configure(self, event: tk.Event) -> None:
    """Sincroniza el alto del canvas con el del frame interior."""
    self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all"))
```

## 5. Tarjeta de Producto

Es el componente mas importante. Se implementa en
`views/components/product_card.py`.

```
┌──────────────────────────────────────────────────────────────────┐
│ ┌──────────┐   Faith Store                    [ 70%   ]  ┌────┐ │
│ │          │   Camiseta Polo                     Stock   │████│ │
│ │  FOTO    │                                    Alto     │████│ │
│ │ 110x110  │   [S] [M] [L] [XL]   ← pildoras               │████│ │
│ │          │        ⚠ L: 1 unidad                             └────┘ │
│ │          │                                                 Stock│
│ └──────────┘                                                 Bajo │
│                                                                  │
│  ┌────────┐   ╭──────────────────────╮                       ⚠   │
│  │Tendencia│   │  Cost   Venta   Margen│                     [ ⚠ ]  │
│  │ ╱╲__╱   │   │  $15    $25     40%   │                          │
│  └────────┘   ╰──────────────────────╯                           │
│                                                                  │
│  [ Bs. 25.00 ]  [ BCV 36.50 ]  [ USDT 1.00 ]  ← multivisa        │
└──────────────────────────────────────────────────────────────────┘
```

### 5.1 Columna Izquierda - Informacion

| Elemento | Componente | Notas |
|----------|------------|-------|
| Foto | `CTkLabel` con `CTkImage` | `110x110`, esquina izquierda redondeada. Si no hay imagen, placeholder con iniciales. |
| Encabezado | `CTkLabel` | "Faith Store" pequeno + ID del producto, en `TEXT_MUTED`. |
| Titulo | `CTkLabel` | `("Segoe UI", 16, "bold")`, color `TEXT_PRIMARY`. |
| Tallas | `CTkFrame` horizontal | Pildoras `corner_radius=6`, `fg_color=BG_PILL`. |
| Badge de alerta | `CTkLabel` | Encima de la talla afectada: "Bajo" en `STOCK_RED` sobre `STOCK_RED_BG`. |
| Precios | 3 columnas | Cost / Venta / Margen. Etiquetas en `TEXT_MUTED` 11px, valores en 14px. |
| Margen | `CTkLabel` | "40% Bruto". Verde si > 30, ambar si 15-30, rojo si < 15. |
| Multivisa | 3 pildoras | `Bs.`, `BCV`, `USDT` con los valores actuales. |

### 5.2 Columna Central - Grafica de Tendencia

Grafica de linea spline de las ultimas ventas de esa producto.

```python
# config.py
TREND_FIGURE_SIZE = (3, 1.5)
TREND_FIGURE_DPI = 100
TREND_LINE_COLOR = "#0066FF"
TREND_FILL_ALPHA = 0.2
```

```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def build_trend_canvas(self, master: tk.Misc, ventas: list[int]) -> None:
    """Dibuja la mini-grafica de tendencia dentro de la tarjeta."""
    figure = Figure(figsize=TREND_FIGURE_SIZE, dpi=TREND_FIGURE_DPI)
    axes = figure.add_subplot(111)
    axes.plot(ventas, color=TREND_LINE_COLOR, linewidth=1.5)
    axes.fill_between(range(len(ventas)), ventas, alpha=TREND_FILL_ALPHA,
                       color=TREND_LINE_COLOR)
    axes.axis("off")           # sin ejes: es una sparkline, no un grafico
    figure.tight_layout(pad=0.1)
    canvas = FigureCanvasTkAgg(figure, master)
    canvas.draw()
    canvas.get_tk_widget().pack()
```

Requisitos: ejes ocultos, sin titulo, sin grid, sin ticks. Es una sparkline.
Si la variante no tiene ventas, mostrar un placeholder "Sin ventas aun".

### 5.3 Columna Derecha - Indicador de Stock

- Texto de porcentaje arriba: `70%`, `15%`.
- Barra vertical de `width=24`, `height=120`, esquinas redondeadas.
- `CTkProgressBar` no soporta vertical: usar `CTkCanvas` con `create_rectangle`
  o un `CTkFrame` whose `height` se calcula segun el porcentaje.
- Color de la barra segun el semaforo.
- Badge de estado abajo:
  - "Stock Alto" → `STOCK_GREEN_BG` / texto oscuro
  - "Stock Medio" → `STOCK_YELLOW_BG` / texto oscuro
  - "Stock Bajo - Reabastecer" → `STOCK_RED_BG` / texto oscuro
- Icono `⚠` a los lados de la barra en estado critico.

## 6. Reglas de la Interfaz

1. **Nunca `.place()`.** Solo `grid` y `pack`.
2. **Nunca un hex literal en `views/`.** Todo sale de `config.py`.
3. **Toda consulta a BD en hilo secundario.** Nunca en el hilo de la GUI.
4. **Respuesta visual inmediata.** Al hacer clic, la UI reacciona ya; los datos
   llegan despues.
5. **Tamanos minimos legibles.** 11 px para etiquetas, 14 px para valores,
   16 px para titulos.
6. **Contraste suficiente.** Texto principal sobre superficie, nunca al reves.

## 7. Mapeo Rapido de Componentes

| Necesito | Usar |
|----------|------|
| Contenedor con scroll | `CTkScrollableFrame(master, fg_color=BG_PRIMARY)` |
| Tarjeta | `CTkFrame(master, fg_color=BG_SURFACE, corner_radius=RADIUS_CARD)` |
| Barra de busqueda | `CTkEntry(master, corner_radius=RADIUS_PILL, border_width=1, fg_color=BG_SURFACE)` |
| Boton | `CTkButton(master, corner_radius=RADIUS_PILL)` |
| Pildora / tag | `CTkLabel(master, corner_radius=RADIUS_BADGE, fg_color=BG_PILL)` |
| Badge de estado | `CTkLabel(master, corner_radius=RADIUS_BADGE, fg_color=STOCK_GREEN_BG)` |
| Sidebar | `CTkFrame(master, width=SIDEBAR_WIDTH, corner_radius=0, fg_color=BG_SURFACE)` |
| Imagen | `CTkLabel` + `CTkImage(Image.open(path), size=(110, 110))` |
| Barra vertical | `CTkCanvas` con `create_rectangle` y esquinas redondeadas |
| Grafica | `Figure` + `FigureCanvasTkAgg` dentro de un `CTkFrame` |

---

**Volver a:** `ROADMAP.md`
