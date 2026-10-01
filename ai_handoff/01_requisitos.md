# 01 - Requerimientos Funcionales

> Que debe hacer Faith Store y por que. Este archivo define el alcance completo.
> No contiene decisiones de implementacion.

---

## 1. Contexto del Negocio

Faith Store es una tienda de ropa y calzado. Hoy controla su inventario en una
libreta. Eso genera cuatro problemas concretos:

| Problema | Consecuencia |
|----------|--------------|
| No sabe cuanto hay de cada talla | Compra de mas o se queda sin stock en la talla que se vende |
| Busca en la libreta mientras el cliente espera | Pierde la venta por lentitud |
| No avisa cuando algo se esta agotando | Se entera cuando ya no hay |
| No sabe la ganancia real | La tasa de cambio cambia diario y no lleva las cuentas |

El sistema resuelve esos cuatro. Todo lo de abajo se deriva de eso.

---

## 2. Concepto Central: Producto y Variantes

Esta es la pieza que define todo el modelo de datos.

Un **producto** tiene muchas **variantes**. Cada variante lleva su propio
inventario y su propio precio. La unidad de venta siempre es una variante,
nunca un producto suelto.

```
Producto:  Camiseta Polo Azul     (codigo PN-001, precio USD 25.00)
├── Variante S    ->  3 unidades   ->  vendible
├── Variante M    -> 12 unidades   ->  vendible
├── Variante L    ->  1 unidad     ->  ALERTA CRITICA
└── Variante XL   ->  0 unidades   ->  AGOTADA
```

### 2.1 Tipos de Talla

Un producto es de **ropa** o de **calzado**, y cada tipo admite tallas
distintas:

| Tipo | Formato de talla | Ejemplos |
|------|------------------|----------|
| Ropa | Letras | S, M, L, XL, XXL |
| Calzado | Numeros | 38, 39, 40, 41, 42 |

El sistema debe soportar ambos con el mismo tratamiento interno. La validacion
debe rechazar la entrada invalida: la letra `Q` no es una talla valida de ropa,
el `7` no es una talla valida de calzado.

### 2.2 Reglas de Negocio

1. Todo producto tiene **al menos una variante**. Un producto sin tallas no es
   vendible.
2. Cada variante tiene un **stock minimo** deseado, propio de cada talla. No es
   un valor global.
3. El stock de una variante **solo** baja cuando se registra una venta.
4. Editar el stock manualmente esta permitido, pero la venta es la unica via
   que lo descuenta de forma automatica.
5. Un producto se **desactiva** en lugar de eliminarse cuando ya tiene ventas
   asociadas, para no romper el historico.

---

## 3. Multimoneda

El negocio pacta en dolares, cobra en bolivares y acepta pagos en USDT.

### 3.1 Reglas

1. El **precio del producto se define en USD**. Es la moneda de referencia.
2. La **tasa BCV** se actualiza a diario. La ingresa el usuario, no se consulta
   por internet.
3. Cada venta **congela** la tasa del momento. Si manana la tasa subio, las
   ventas de ayer no se recalculan.
4. Todo importe se muestra en las tres divisas a la vez.
5. La tasa tiene fecha. El sistema guarda el historial para poder auditar.

### 3.2 Ejemplo de Calculo

```
Venta:       2 x Camiseta Polo @ 25.00 USD   =  50.00 USD
Tasa BCV:    36.50 Bs. por USD
Importe Bs.: 50.00 x 36.50                   =  1825.00 Bs.
Referencia:  50.00 USD x 1.00                =   50.00 USDT
```

### 3.3 Visibilidad

En la barra superior de la aplicacion, siempre visible, la tasa BCV actual y la
tasa USDT actual. Consulta rapida sin abrir un modulo.

---

## 4. Modulo 1 - Catalogo y Matriz de Tallas

### 4.1 Funciones

- Registrar producto con codigo, nombre, categoria, costo y precio de venta.
- El codigo es unico y funciona como ID o codigo de barras escaneable.
- Asignar tallas al producto, con stock inicial por talla.
- Editar cualquier dato de un producto o de una talla.
- Dar de baja productos y tallas.
- Calcular el margen bruto de cada unidad automaticamente.

### 4.2 Margen Bruto

```
margen_bruto_pct = ((precio_venta - costo) / precio_venta) * 100
```

Casos limite obligatorios:

| Caso | Resultado esperado |
|------|-------------------|
| `precio_venta = 0` | `0.0` (evitar division por cero) |
| `costo > precio_venta` | Negativo, se muestra en rojo |
| `costo = precio_venta` | `0.0` |

### 4.3 Interfaz

- Tarjeta por producto con: imagen, nombre, codigo, categoria.
- Badge del margen bruto con color: verde sobre 30, ambar entre 15 y 30, rojo
  bajo 15.
- Pildoras de talla con el stock de cada una.
- Matriz de tallas visible sin abrir un detalle.

---

## 5. Modulo 2 - Buscador Inteligente

### 5.1 Funciones

- Busqueda mientras el usuario escribe, sin pulsar un boton.
- Busca por **codigo** y por **nombre**.
- Desplegable flotante con los resultados: imagen, tallas disponibles y precio.

### 5.2 Tolerancia de Entrada

Este es el detalle que define la experiencia del cliente:

| El usuario escribe | El sistema encuentra |
|---------------------|----------------------|
| `pantalon` | `Pantalon` |
| `pantalon` | `Pantalón` |
| `PANTALON` | `Pantalón` |
| `Polo` | `polo azul` |
| `PN-001` | el producto con ese codigo |

La comparacion debe ignorar acentos, tildes y mayusculas. El mecanismo estandar
es normalizar a Unicode NFD, quitar los diacriticos y pasar a minusculas, tanto
en la entrada como en el dato almacenado.

### 5.3 Rendimiento

- **Debounce**: la consulta no se dispara en cada tecla. Se espera a que el
  usuario deje de escribir. 250 a 400 ms es el rango razonable.
- La respuesta debe ser imperceptible con el volumen real del negocio.
- Criterio: bajo 100 ms con 5000 productos cargados.

### 5.4 Interfaz

- Barra de busqueda prominente y centrada en la barra superior.
- Icono de lupa.
- Sugerencias que aparecen debajo mientras escribe.
- Cada sugerencia muestra foto, nombre, codigo, precio y tallas disponibles.
- Resaltar visualmente la parte que coincide con lo escrito.

---

## 6. Modulo 3 - Alertas de Stock

### 6.1 Semaforo de Tres Estados

El estado se evalua **por talla**, contra el stock minimo de esa talla.

| Estado | Condicion | Color | Significado |
|--------|-----------|-------|-------------|
| Optimo | `stock > minimo x 2` | Verde `#34C759` | Inventario saludable |
| Medio | `stock > minimo` | Ambar `#FF9500` | Proximo al limite de reserva |
| Critico | `stock <= minimo` | Rojo `#FF3B30` | Reabastecer ya |
| Agotado | `stock = 0` | Rojo `#FF3B30` | Sin existencias |

Los umbrales exactos son configurables. Los valores de arriba son el default
sugerido.

### 6.2 Avisos

- Cada tarjeta de producto muestra su estado de forma visible sin color de
  fondo: la barra lateral y el badge lo indican.
- Cuando una venta deja una talla en estado critico, se emite un aviso en
  pantalla. El aviso debe poder descartarse.
- El usuario necesita saber **que talla** se esta agotando, no solo que el
  producto se agota.

### 6.3 Reabastecimiento

- Poder cargar stock a una talla concreta.
- Poder ver el reporte de cuantas unidades faltan para llegar al minimo en cada
  talla, ordenado por urgencia.

---

## 7. Modulo 4 - Importacion Excel y Backup

### 7.1 Importacion desde Excel

- Carga masiva del inventario desde una plantilla `.xlsx` estandarizada.
- El usuario completa la plantilla y la sube. Sin tipeo producto por producto.

**La plantilla debe incluir:** codigo, nombre, categoria, tipo de producto,
talla, cantidad, stock minimo, costo, precio de venta.

**Reglas de la importacion:**

1. **Transaccional.** Si una fila es invalida, no se importa nada. Todo o nada.
2. **Validar antes de escribir.** Codigo duplicado, talla invalida, precio
   negativo, cantidad no numerica.
3. **Reportar el resultado.** Cuantas filas se importaron, cuantas se
   rechazaron y **por que** se rechazo cada una. Con el numero de fila.
4. **Cifras y separadores.** El archivo puede traer `1.234,56` o `1,234.56`.
   Detectar el formato.

Criterio: 1000 productos en menos de 10 segundos.

### 7.2 Exportacion a Excel

- Exportar cualquier listado a `.xlsx`: catalogo, ventas, reporte de stock.
- Con boton, sin pedirle al usuario que arme el archivo a mano.

### 7.3 Backup

- Copia de la base de datos completa con **un clic**.
- Destino elegible: memoria USB, carpeta local, unidad de red.
- El archivo lleva **fecha y hora** en el nombre.
- Debe funcionar aunque el sistema este abierto, sin corromper la base.
- Debe indicar al usuario donde se guardo y cuanto pesa.

Criterio: un backup restaurado debe ser identico a la base original.

---

## 8. Modulo 5 - Punto de Venta

### 8.1 Funciones

- Registrar una salida seleccionando **producto** y **talla**. La talla es
  obligatoria. No se puede vender una talla que no se eligio.
- Descuento automatico del stock de esa talla.
- Conversion automatica a USD, Bs. y USDT.
- Emision de ticket en PDF.
- Opcion de imprimir el ticket.

### 8.2 Atomicidad

El descuento de stock y el registro de la venta son **una sola operacion**. Si
el registro de la venta falla, el stock no se toca. Si el descuento falla, no
hay venta.

### 8.3 Carrito

- Varias lineas antes de confirmar.
- Cantidad por linea.
- Total por linea y total general, en las tres divisas.
- Feedback inmediato de stock insuficiente.

### 8.4 Ticket PDF

- Datos del negocio.
- Fecha, hora, numero de ticket.
- Lineas con producto, talla, cantidad, precio.
- Totales en las tres divisas.
- Tasa BCV aplicada, impresa explicitamente.

---

## 9. Modulo 6 - Dashboard y Reportes

### 9.1 Dashboard

- Graficas de rendimiento en la pantalla principal.
- Evolucion de ventas por periodo.
- Distribucion de ventas por producto o categoria.
- Indicadores clave: ingresos del periodo, ticket promedio, producto mas
  vendido.

### 9.2 Reportes

- Ingresos y ganancias netas por rango: **diario, semanal, mensual**.
- Filtros por rango de fechas.
- Detalle por producto.
- Exportar a Excel con un boton.

### 9.3 Graficas

- Vectoriales, integradas dentro de la aplicacion, no imagenes externas.
- Coherentes con la paleta de la interfaz.
- Etiquetas y ejes legibles, no con decimales de mas.

---

## 10. Requisitos No Funcionales

### 10.1 Plataforma

| Requisito | Valor |
|-----------|-------|
| Sistema operativo | Windows 10 y Windows 11, 64 bits |
| Formato de entrega | Instalador `.exe` |
| Instalacion | Doble clic, sin pasos tecnicos para el usuario final |
| Requiere Python instalado | **No** |
| Requiere internet | **No** |

### 10.2 Rendimiento

| Operacion | Objetivo |
|-----------|----------|
| Importar 1000 productos desde Excel | < 10 s |
| Busqueda con 5000 productos | < 100 ms |
| Abrir el catalogo con 5000 productos | < 2 s |
| Registrar una venta | < 200 ms |
| Generar backup | < 5 s |

### 10.3 Resiliencia

- La interfaz **nunca** se congela. Ninguna operacion de disco, base de datos o
  red puede ejecutarse en el hilo de la interfaz.
- Si una operacion falla, el usuario ve un mensaje util, no una excepcion.
- Los datos del usuario no se pierden por un cierre inesperado.

### 10.4 Usabilidad

- Interfaz en espanol.
- Navegacion por teclado donde tenga sentido.
- Interfaz que se adapta a pantallas HD y FHD.
- Tiempos de respuesta perceptibles como inmediatos.

---

## 11. Criterios de Aceptacion

Checklist verificable. El proyecto no se considera terminado sin esto.

**Catalogo**
- [ ] Se puede crear un producto con sus tallas y stock inicial.
- [ ] El margen bruto se calcula y se muestra con color.
- [ ] El codigo es unico y se puede buscar por el.
- [ ] Un producto con ventas no se puede borrar, solo desactivar.

**Buscador**
- [ ] Escribir `pantalon` encuentra `Pantalón`.
- [ ] Los resultados aparecen sin pulsar Enter.
- [ ] Las sugerencias muestran foto, precio y tallas disponibles.

**Alertas**
- [ ] Cada talla muestra su estado de stock.
- [ ] Al bajar de stock minimo, aparece un aviso.
- [ ] El reporte de faltantes indica cuantas unidades faltan por talla.

**Excel y backup**
- [ ] Importar la plantilla crea los productos con sus tallas.
- [ ] Una fila invalida impide toda la importacion y reporta el motivo.
- [ ] El backup genera un archivo con fecha y hora.
- [ ] El backup restaurado es identico a la base original.

**Ventas**
- [ ] No se puede vender sin elegir talla.
- [ ] Vender descuenta el stock de esa talla.
- [ ] La venta congela la tasa BCV del momento.
- [ ] El ticket PDF sale con los totales en tres divisas.

**Reportes**
- [ ] Los totales por dia, semana y mes coinciden con las ventas registradas.
- [ ] El reporte se exporta a Excel.

**Aplicacion**
- [ ] Arranca en Windows 10 y 11 con doble clic.
- [ ] Funciona con el cable de red desconectado.
- [ ] La interfaz no se congela durante operaciones largas.

---

## 12. Fuera de Alcance

No construir en esta version:

- Sincronizacion en la nube.
- Multiusuario con concurrencia. Es una app de un solo puesto.
- Aplicacion movil.
- Integracion con pasarelas de pago.
- Programa de escritorio para Mac o Linux.

---

**Siguiente:** `02_arquitectura.md`
