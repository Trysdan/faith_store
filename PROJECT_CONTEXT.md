# PROJECT_CONTEXT.md - Faith Store

> **Que es este archivo:** Contexto del proyecto. Explica QUE vamos a construir y
> POR QUE. Leer PRIMERO, antes de `AGENTS.md`.

---

## 1. Vision del Negocio

**Faith Store** es un sistema de control de inventario para una tienda de ropa y
calzado, reemplaza el control manual en libreta.

El problema real que resuelve:

- El dueno pierde plata porque no sabe cuanto vendo de cada talla.
- Buscar un producto en una libreta toma minutos; el cliente se va.
- No hay forma de saber si una prenda esta por agotarse antes de perder la venta.
- No se sabe la ganancia real porque las tasas de cambio cambian todos los dias.

## 2. Definicion de Producto

Un **producto** tiene muchas **variantes** (tallas). Cada variante lleva su propio
inventario. Esto es lo central del sistema.

Ejemplo real:

```
Producto:  Camiseta Polo Azul
├── Variante S   -> 3 unidades   -> vendible
├── Variante M   -> 12 unidades  -> vendible
├── Variante L   -> 1 unidad     -> ALERTA CRITICA
└── Variante XL  -> 0 unidades   -> AGOTADA
```

Ropa usa tallas de letra (S, M, L, XL). Calzado usa numeros (38, 39, 40, 41).
Un producto de calzado con talla 40 y uno de ropa con talla M se gestionan igual
de forma estructural: son variantes con stock independiente.

## 3. Multimoneda (Core del Negocio)

El negocio opera en Venezuela. Las ventas se pactan en **dolares (USD)** pero el
proveedor cobra en **bolivares (Bs.)**. Ademas el cliente puede pagar en **USDT**.

Reglas del dominio:

- El precio del producto se define en **USD**.
- La **tasa BCV** se consulta y se actualiza a diario.
- Al hacer una venta, la tasa usada queda **congelada** en el registro.
  Si manana la tasa subio, las ventas de ayer no se recalculan.
- Todo importe se muestra simultaneamente en USD, Bs. y USDT.

Ejemplo del calculo que hay que implementar:

```
Venta:        2 x Camiseta @ 25.00 USD  =  50.00 USD
Tasa BCV:     36.50 Bs. por USD
Importe Bs.:  50.00 x 36.50             =  1825.00 Bs.
Referencia:   50.00 USD x 1.00           =   50.00 USDT
```

> Este calculo es logica de negocio pura. Va en `models/` o `services/`.
> **Prohibido** hacerlo dentro de una vista.

## 4. Stack Tecnologico (Fijo, ya decidido)

El cliente aprobo este stack. No cambiarlo sin justificacion escrita.

| Capa | Tecnologia | Razon |
|------|------------|-------|
| Lenguaje | Python 3.11+ | Pedido del cliente |
| GUI | CustomTkinter | Estilo Windows 11, temas claro/oscuro, DPI |
| BD | SQLite 3 | Embebida, sin servidor, sin internet |
| Excel | pandas + openpyxl | Carga masiva y exportacion |
| Graficos | matplotlib + FigureCanvasTkAgg | Graficas vectoriales dentro de la GUI |
| PDF | ReportLab | Tickets y reportes imprimibles |
| Empaquetado | PyInstaller + Inno Setup | Instalador .exe para Win 10/11 |

**Restriccion critica: la aplicacion debe funcionar 100% offline.**
Ninguna dependencia de red en tiempo de ejecucion. La tasa BCV la ingressa el
usuario a mano.

## 5. Modulos Funcionales

### Modulo 1 - Catalogo y Matriz de Tallas
Alta, edicion y baja de productos. Cada producto con sus tallas y stock
independiente. Calculo automatico de margen bruto por unidad.

### Modulo 2 - Buscador Inteligente
Busqueda mientras se escribe. Ignora tildes, acentos y mayusculas.
"pantalon" debe encontrar "Pantalón". Desplegable flotante con imagen, tallas
disponibles y precio.

### Modulo 3 - Alertas de Stock
Semforo de tres estados evaluado por talla contra un minimo deseado.

| Estado | Color | Significado |
|--------|-------|-------------|
| Verde | `#34C759` | Stock saludable |
| Amarillo | `#FF9500` | Proximo al limite de reserva |
| Rojo | `#FF3B30` | Reabastecer ya |

### Modulo 4 - Importacion Excel y Backup
Carga masiva del inventario desde una plantilla `.xlsx` estandarizada.
Backup de un clic que clona la base de datos a USB o carpeta, con fecha y hora.

### Modulo 5 - Punto de Venta y Multimoneda
Caja para registrar salidas seleccionando prenda y talla, con descuento automatico
de existencias. Conversion a las tres divisas. Emision de ticket en PDF.

### Modulo 6 - Dashboard y Reportes
Graficas de rendimiento. Reportes de ingresos y ganancias netas por rango
(diario, semanal, mensual). Exportacion a Excel con un boton.

## 6. Modelo de Datos (SQLite)

```sql
productos          (id, codigo UNIQUE, nombre, categoria,
                    costo, precio_venta, activo, creado_en, actualizado_en)

variantes          (id, producto_id FK, codigo_talla,
                    stock_actual, stock_minimo, precio_ajuste, activo)

ventas             (id, variante_id FK, cantidad, precio_unitario_usd,
                    tasa_bcv_congelada, total_usd, total_bs, total_usdt,
                    medio_pago, vendido_en)

config_sistema     (clave PK, valor, actualizado_en)
```

Decisiones de diseno ya tomadas:

- `codigo` es UNIQUE porque es el codigo de barras / ID que se escanea.
- `tasa_bcv_congelada` vive **en la venta**, no se lee de config al mostrar
  reportes. Es el historico inalterable.
- `ON DELETE RESTRICT` en `ventas.variante_id`: no se puede borrar una variante
  que ya tiene ventas. Se desactiva con `activo = 0`.
- Indices en `productos(codigo)`, `productos(nombre)`, `ventas(vendido_en)`.

## 7. Criterios de Aceptacion

- Arranca en Windows 10 y 11 haciendo doble click en un `.exe`.
- Funciona con el cable de red desconectado.
- Importa 1000 productos desde Excel en menos de 10 segundos.
- La busqueda responde en menos de 100 ms con 5000 productos cargados.
- La venta descuenta stock y congela la tasa en la misma operacion atomica.
- Ninguna consulta SQL o regla de negocio dentro de las vistas.
- Ninguna operacion de I/O bloquea la interfaz grafica.

## 8. Entregables Finales

1. `FaithStore_Setup.exe` - instalador para Windows 10/11
2. Plantilla `.xlsx` para carga de inventario inicial
3. Guia de usuario en PDF

---

**Siguiente archivo a leer:** `AGENTS.md` (como trabajar en el codigo).
