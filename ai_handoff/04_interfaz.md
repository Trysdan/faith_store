# 04 - Especificacion de Interfaz

> Como se ve y se siente la aplicacion. Leer **antes** de escribir la primera
> vista.

---

## 1. Estilo

**Windows 11 Fluent UI Light.**

Bordes redondeados generosos, paleta clara con contrastes suaves, tarjetas
independientes flotando sobre el fondo, indicadores de estado visibles sin
gritar.

La sensacion objetivo: una app nativa de Windows 11, no una web app ni un
formulario de los 90.

---

## 2. Paleta

Todos estos valores van en `config.py`. **Ningun hex literal en `views/`.**

### 2.1 Color

| Rol | Hex | Constante |
|-----|-----|-----------|
| Fondo principal | `#F3F4F8` | `BG_PRIMARY` |
| Fondo superficie, sidebar, tarjetas | `#FFFFFF` | `BG_SURFACE` |
| Texto principal | `#1C1C1E` | `TEXT_PRIMARY` |
| Texto secundario, etiquetas | `#6E6E73` | `TEXT_MUTED` |
| Acento azul | `#0066FF` | `ACCENT_BLUE` |
| Acento azul hover | `#1D63ED` | `ACCENT_BLUE_HOVER` |
| Optimo, stock alto | `#34C759` | `STOCK_GREEN` |
| Fondo optimo | `#DCFCE7` | `STOCK_GREEN_BG` |
| Medio, stock por agotarse | `#FF9500` | `STOCK_YELLOW` |
| Fondo medio | `#FEF3C7` | `STOCK_YELLOW_BG` |
| Critico, stock bajo | `#FF3B30` | `STOCK_RED` |
| Fondo critico | `#FEE2E2` | `STOCK_RED_BG` |
| Navegacion activa | `#E5E7EB` | `NAV_ACTIVE_BG` |
| Pildoras y tags | `#F3F4F6` | `BG_PILL` |
| Bordes sutiles | `#E5E7EB` | `BORDER_SUBTLE` |
| Texto de error | `#D70015` | `TEXT_ERROR` |

**Regla de la paleta:** tres colores primarios, azul de acento, verde de
estado optimo, rojo de alerta. Los neutros son parte del tema y no cuentan.

**Regla de contraste:** texto oscuro sobre fondo claro, nunca al reves. Un
badge de estado usa fondo suave y texto oscuro, no fondo saturado con texto
blanco.

### 2.2 Radios

| Elemento | Valor | Constante |
|----------|-------|-----------|
| Botones, barra de busqueda | `20` | `RADIUS_PILL` |
| Tarjetas de producto | `14` | `RADIUS_CARD` |
| Paneles, sidebar | `16` | `RADIUS_PANEL` |
| Badges, pildoras de estado | `8` | `RADIUS_BADGE` |
| Pildoras de talla | `6` | `RADIUS_SIZE` |

### 2.3 Tipografia

Fuente del sistema: `Segoe UI`.

| Rol | Tamano | Peso | Constante |
|-----|--------|------|-----------|
| Titulo de pagina | 24 | bold | `FONT_TITLE` |
| Titulo de tarjeta | 16 | bold | `FONT_CARD_TITLE` |
| Valor, precio | 14 | normal | `FONT_VALUE` |
| Etiqueta, subtitulo | 11 | normal | `FONT_LABEL` |
| Texto pequeno, badge | 10 | normal | `FONT_BADGE` |

`Segoe UI` viene con Windows. Si el proyecto corre en otro sistema durante el
desarrollo, la fuente cae al default del sistema sin romper el layout.

### 2.4 Espaciado

| Concepto | Valor |
|----------|-------|
| Padding de tarjeta | `15` px |
| Gap entre tarjetas | `15` px |
| Padding de panel | `20` px |
| Gap entre pildoras | `6` px |

---

## 3. Estructura de la Ventana

```
┌─────────────┬──────────────────────────────────────────────────────┐
│             │  TopBar                                               │
│  Sidebar    │  ┌──────────────────────────────────┐  ↑    🔒      │
│  220 px     │  │ 🔍 Buscar producto por nombre o ID │                │
│             │  └──────────────────────────────────┘                 │
│  ☰          ├──────────────────────────────────────────────────────┤
│             │                                                       │
│  Dashboard  │  CTkScrollableFrame                                   │
│  Inventario │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  Ventas     │  │            │  │            │  │            │       │
│  Reportes   │  │  Tarjeta   │  │  Tarjeta   │  │  Tarjeta   │       │
│  Ajustes    │  │            │  │            │  │            │       │
│             │  └────────────┘  └────────────┘  └────────────┘       │
│             │  ┌────────────┐  ┌────────────┐                       │
│             │  │            │  │            │                       │
│             │  │  Tarjeta   │  │  Tarjeta   │                       │
│  ─────────  │  └────────────┘  └────────────┘                       │
│  BCV 36.50  │                                                       │
│  USDT 38.00 │                                                       │
└─────────────┴──────────────────────────────────────────────────────┘
```

### 3.1 Sidebar

- Ancho fijo `220`.
- Boton hamburguesa `☰` arriba, colapsa el menu en pantallas angostas.
- Items de navegacion como botones de fondo transparente.
- Item activo: fondo gris claro, texto en negrita, indicador lateral azul de
  3 px pegado al borde izquierdo.
- Al pie, las tasas activas: BCV y USDT, siempre visibles.

**Items de navegacion:**

| Item | Modulo | Icono |
|------|--------|-------|
| Dashboard | Panel principal | `▦` |
| Inventario | Catalogo y producto | `▤` |
| Punto de Venta | Caja | `🛒` |
| Reportes | Ventas y ganancias | `▥` |
| Ajustes | Configuracion y tasas | `⚙` |

**Indicador de item activo:** franja azul de 3 px de ancho, alineada a la
izquierda del boton, de alto completo del item. No un icono cambia de color: un
elemento de fondo.

### 3.2 TopBar

- `CTkEntry` centrado, `corner_radius=20`, `border_width=1`, fondo blanco.
- Placeholder: `"Buscar producto por nombre o ID..."`.
- Icono de lupa a la izquierda, dentro del campo.
- Boton de backup a la derecha, circular y transparente.
- Boton de bloqueo a la derecha de ese, circular y transparente.
- **A la izquierda del buscador, las tasas activas visibles:** `BCV 36.50` y
  `USDT 38.00`, en texto secundario.

### 3.3 Area de Contenido

- Un `CTkScrollableFrame` con `fg_color=BG_PRIMARY`.
- Grid de **3 columnas** de tarjetas.
- Cada columna con peso `1` para que sea elastico al redimensionar.
- Gap de 15 px entre tarjetas.
- El alto del canvas se recalcula al redimensionar el frame interior, si no el
  scrollbar mide mal.

```python
def _sync_scrollregion(self, event: tk.Event) -> None:
    """Keep the scrollable region in sync with the inner frame height."""
    self.inner_canvas.configure(
        scrollregion=self.inner_canvas.bbox("all")
    )
```

---

## 4. Tarjeta de Producto

El componente mas importante de la aplicacion. Va en
`views/components/product_card.py`.

### 4.1 Anatomia

```
┌────────────────────────────────────────────────────────────────────┐
│ ┌──────────┐   Faith Store                       70%    ┌───┐     │
│ │          │   Camiseta Polo                       Stock  │███│     │
│ │  IMAGEN  │                                        Alto  │███│     │
│ │ 110x110  │   [S] [M] [L] [XL]  ← pildoras                 │░░░│     │
│ │          │       ⚠ L: 1 unidad                           └───┘     │
│ └──────────┘                                                Stock  │
│                                                              Bajo  │
│  ┌────────┐    ┌─────────┬─────────┬─────────┐                   │
│  │TENDENCIA│    │  COST   │  VENTA  │  MARGEN │                   │
│  │  ╱╲__╱  │    │  $15.00 │  $25.00 │ 40%     │              ⚠   │
│  └────────┘    └─────────┴─────────┴─────────┘            [ ⚠ ]   │
│                                                                    │
│  ┌ Bs. 25.00 ┐  ┌ BCV 36.50 ┐  ┌ USDT 38.00 ┐                       │
└────────────────────────────────────────────────────────────────────┘
```

### 4.2 Columna Izquierda - Informacion y Producto

| Elemento | Tamano | Estilo |
|----------|--------|--------|
| Imagen | `110x110` | Esquina izquierda redondeada. Placeholder con iniciales si no hay. |
| Marca | 10 px | "Faith Store" mas el ID del producto, en `TEXT_MUTED` |
| Titulo | 16 px bold | `TEXT_PRIMARY`. Maximo 2 lineas, ellipsis |
| Seccion tallas | etiqueta 11 px + pildoras | Ver 4.4 |
| Badge de alerta sobre talla | 10 px | "Bajo" en `STOCK_RED` sobre `STOCK_RED_BG` |
| Seccion precios | 3 columnas | Etiqueta 11 px `TEXT_MUTED`, valor 14 px `TEXT_PRIMARY` |
| Margen | 14 px | Color segun los umbrales: verde sobre 30, ambar 15 a 30, rojo bajo 15 |
| Multivisa | 3 pildoras 10 px | `BG_PILL`, formato `Bs. 25.00` |

### 4.3 Columna Central - Grafica de Tendencia

Sparkline con las ultimas ventas del producto.

```python
TREND_FIGURE_SIZE = (3, 1.5)   # pulgadas
TREND_FIGURE_DPI = 100
TREND_LINE_COLOR = "#0066FF"
TREND_FILL_ALPHA = 0.2
TREND_WINDOW = 14               # ultimos N dias
```

- Linea azul suave.
- Relleno celeste debajo, con 20% de opacidad.
- **Sin ejes, sin titulo, sin grid, sin ticks.** Es una sparkline, no un
  grafico. Su trabajo es dar una sensacion de pendiente, nada mas.
- Si la variante no tiene ventas, mostrar el texto "Sin ventas aun" en
  `TEXT_MUTED`. No un eje vacio.

### 4.4 Pildoras de Talla

- Pildora por talla, con el stock al lado: `M 12`
- `corner_radius=6`, `fg_color=BG_PILL`, 10 px.
- Color del texto segun el estado de esa talla:

| Estado | Texto | Fondo |
|--------|-------|-------|
| Optimo | `TEXT_PRIMARY` | `BG_PILL` |
| Medio | `STOCK_YELLOW` | `STOCK_YELLOW_BG` |
| Critico | `STOCK_RED` | `STOCK_RED_BG` |
| Agotado | `STOCK_RED` | `STOCK_RED_BG` |

- Talla agotada: tachada, con opacidad reducida.
- Al hacer clic en una pildora, se puede vender directamente esa talla. Es el
  atajo del punto de venta.

### 4.5 Columna Derecha - Indicador de Stock

```
   70%        ← porcentaje
 ┌────┐
 │████│       ← barra vertical, 24 x 120
 │████│
 │████│
 │░░░░│
 └────┘
  Stock Alto   ← badge con fondo suave y texto oscuro
```

| Elemento | Detalle |
|----------|---------|
| Porcentaje | 14 px, `TEXT_PRIMARY`. Es el stock sobre un objetivo de referencia. |
| Barra vertical | 24 px de ancho, 120 px de alto, esquinas redondeadas |
| Color de la barra | `STOCK_GREEN`, `STOCK_YELLOW` o `STOCK_RED` segun el semaforo |
| Badge | `corner_radius=8`, fondo suave, texto oscuro |
| Texto del badge | "Stock Alto", "Stock Medio", "Stock Bajo - Reabastecer" |
| Icono de alerta | `⚠` a los lados de la barra en estado critico |

**Progreso vertical:** `CTkProgressBar` no admite orientacion vertical.
Opciones validas, en orden de preferencia:

1. `CTkCanvas` con `create_rectangle` y esquinas redondeadas dibujando
   `create_round_rect`. Totalmente controlable.
2. Un `CTkFrame` cuyo `height` se calcula como
   `TARGET_HEIGHT * percentage / 100` y se empaqueta con `side="bottom"`.

La primera es la correcta. La segunda sirve para un prototipo.

---

## 5. Interacciones

### 5.1 Catalog View

| Interaccion | Resultado |
|-------------|-----------|
| Escribir en el buscador | Sugerencias despues del debounce, sin pulsar Enter |
| Clic en sugerencia | Abre el detalle del producto |
| Clic en tarjeta | Abre el detalle del producto |
| Clic en pildora de talla | Abre el punto de venta con esa talla preseleccionada |
| Boton de backup | Clona la base, con feedback en la barra de estado |
| Redimensionar la ventana | Todo es elastico, nada se corta |

### 5.2 Punto de Venta

- Panel izquierdo: buscador de producto.
- Panel derecho: carrito.
- Al agregar una linea, feedback inmediato si no hay stock.
- Totales siempre visibles, actualizados al instante, en las tres divisas.
- Al confirmar, venta atomica y ticket disponible.

### 5.3 Dashboard

- Fila superior de tarjetas de indicador: ingresos del periodo, ticket
  promedio, productos vendidos, tasa BCV vigente.
- Debajo, graficas: evolucion de ventas, top productos, distribucion por
  categoria.
- Selector de periodo: dia, semana, mes.

---

## 6. Estados de Pantalla

Toda vista de listado tiene que manejar tres estados:

| Estado | Cuando | Que mostrar |
|--------|---------|-------------|
| Con datos | Hay resultados | El listado |
| Vacio | Sin resultados de la busqueda | Icono, "Sin resultados para 'xyz'", boton de limpiar |
| Inicial | Nunca se ha buscado | Sugerencias de como usar la vista |

**Nunca** dejar un panel vacio sin explicacion. El usuario debe saber si no hay
datos, si la busqueda fallo, o si la vista no se ha usado.

### 6.1 Estado Vacio Estandar

```
        ( )
   Sin resultados para "zapatos"

   [ Limpiar busqueda ]
```

---

## 7. Feedback

| Tipo | Cuando | Comportamiento |
|------|--------|----------------|
| Feedback inmediato | Cualquier accion del usuario | Responde en menos de 100 ms |
| Indicador de carga | Operacion de mas de 300 ms | Spinner o barra indeterminada |
| Toast de exito | Operacion completada | Desaparece solo en 3 s |
| Toast de error | Operacion fallida | Requiere cierre manual, muestra causa |
| Bloqueo de control | Operacion en curso | El control se deshabilita, no toda la app |

**Principio:** el usuario nunca se queda mirando una ventana congelada sin
explicacion. Si algo tarda, se dice que esta pasando.

---

## 8. Accesibilidad y Comfort

| Regla | Detalle |
|-------|---------|
| Tamano minimo de texto | 10 px para badges, 11 px para etiquetas, nunca menos |
| Contraste | Texto oscuro sobre fondo claro, siempre |
| Teclado | `Esc` cierra dialogos, `Enter` confirma, `F1` ayuda |
| Foco | Visible en todos los controles |
| Tooltips | En botones que solo tienen icono |
| Clic en la tarjeta | En toda la tarjeta, no solo en el texto |
| Zoom de Windows | No romper entre 100% y 150% |

---

## 9. Checklist de Vista

Antes de dar por terminada una vista:

- [ ] Usa solo `grid` y `pack`, nunca `.place()`
- [ ] Todos los colores vienen de `config.py`
- [ ] No hay SQL ni llamadas de base de datos
- [ ] No hay calculos de negocio
- [ ] La I/O pesada esta en hilo secundario
- [ ] Flujo de datos permitido: vista a controller, controller a service
- [ ] Redimensionar la ventana no rompe nada
- [ ] Maneja los tres estados: con datos, vacio, inicial
- [ ] Cada operacion larga da feedback
- [ ] Los errores se muestran como mensaje, no como traceback
- [ ] Los textos de la interfaz estan en espanol
- [ ] Los identificadores del codigo estan en ingles

---

**Volver a:** `05_plan_trabajo.md`
