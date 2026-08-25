# Faith Store - Sistema de Control de Inventario

**Faith Store** es una aplicación de escritorio nativa para Windows 10/11 diseñada para la gestión completa de inventario, ventas y catálogo de productos multitalla.

## Visión General

Sistema offline completo que elimina la gestión manual en libreta, previene pérdidas por descontrol de inventario y acelera la atención al cliente en punto de venta. El programa funciona completamente sin conexión a internet y se distribuye como ejecutable .exe instalable.

## Características Principales

- **Catálogo multitalla:** Organización unificada de ropa y calzado con inventario, ventas y conteo independiente por cada talla.
- **Buscador inteligente:** Búsqueda en tiempo real con autocompletado, insensible a acentos, tildes y mayúsculas/minúsculas.
- **Alertas visuales de stock:** Indicador semáforo (Verde = Alto, Amarillo = Medio, Rojo = Crítico) que avisa cuando una prenda está por agotarse.
- **Importación masiva:** Carga de inventarios completos desde hojas de cálculo Excel en pocos segundos.
- **Control preventivo de pérdidas:** Alertas automáticas cuando una venta deja un producto en nivel crítico de stock.
- **Multimoneda:** Conversión automática de importes en Bolívares (Bs.), Dólares (USD) y USDT con tasa BCV histórica congelada por venta.
- **Dashboard analítico:** Panel visual con gráficos de rendimiento e historial de ventas por períodos (diarios, semanales, mensuales).
- **Sistema de respaldos:** Copia de seguridad completa de la base de datos a un clic, hacia memoria USB o carpeta segura con marca de tiempo.

## Tecnología

- **Lenguaje:** Python 3.11+
- **Interfaz:** CustomTkinter (estilo Windows 11, temas claro/oscuro, alta resolución DPI)
- **Base de datos:** SQLite 3 embebido (sin servidores ni conexión internet requerida)
- **Empaquetado:** PyInstaller e Inno Setup para instalador .exe autocontenido

## Entregables

1. Instalador ejecutable FaithStore_Setup.exe para Windows 10/11
2. Plantilla de importación de Excel para inventario inicial
3. Guía de usuario en PDF paso a paso

## Arquitectura

Aplicación diseñada bajo patrones MVC/MVP estrictos con separación absoluta de:
- **Modelo:** Lógica de datos pura, validaciones y cálculos
- **Vista:** Presentación UI con CustomTkinter, layouts grid/pack
- **Controlador:** Puente entre modelo y vista, inyección de dependencias