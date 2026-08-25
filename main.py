# main.py - Punto de entrada Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Bootstrap/Dependency Injector que inicializa y arranca
# la aplicación completa. Conecta modelos, controladores y vistas.
# Cumple regla: punto de entrada limpio, solo inicializa e inicia mainloop.
# -------------------------------------------------------------------------
from __future__ import annotations

import sys
import tkinter as tk
import customtkinter as ctk

from models.product_model import ProductModel
from models.variant_model import VariantModel
from controllers.catalog_controller import CatalogController
from views.catalog_view import CatalogView


def main() -> None:
    """Punto de entrada principal de la aplicación Faith Store.

    Inicializa la ventana principal, crea las instancias de modelos,
    controladores y vistas, inyecta dependencias y arranca el mainloop.

    Flujo:
        1. Crear ventana raíz CustomTkinter
        2. Instanciar modelos de datos (ProductModel, VariantModel)
        3. Crear vista (CatalogView)
        4. Crear controlador con inyección de dependencias
        5. Cargar datos iniciales
        6. Arrancar mainloop

    Example:
        >>> if __name__ == "__main__":
        ...     main()
    """
    # Configuración ventana principal
    root = ctk.CTk()
    root.title("Faith Store - Control de Inventario")
    root.geometry("1200x800")
    root.minsize(width=1000, height=700)

    # Instanciar modelos de datos (pure logic, no UI)
    product_model = ProductModel()
    variant_model = VariantModel()

    # Crear vista (UI layer - CustomTkinter only, no business logic)
    view = CatalogView(root=root)

    # Crear controlador con inyección de dependencias estricta (DIP)
    # El controlador recibe las dependencias por parámetro, nunca las crea aquí
    controller = CatalogController(
        product_model=product_model,
        variant_model=variant_model,
        view=view,
    )

    # Cargar productos de ejemplo/demo para mostrar en la UI
    # En producción esto vendría de la base de datos o archivo
    sample_products = [
        {
            "id": 1,
            "codigo": "PN-001",
            "nombre": "Polo",
            "categoria": "Ropa",
            "precio_venta": 25.0,
            "margen_pct": 40.0,
        },
        {
            "id": 2,
            "codigo": "PN-002",
            "nombre": "Camiseta",
            "categoria": "Ropa",
            "precio_venta": 15.0,
            "margen_pct": 50.0,
        },
        {
            "id": 3,
            "codigo": "PN-003",
            "nombre": "Pantalón",
            "categoria": "Ropa",
            "precio_venta": 40.0,
            "margen_pct": 30.0,
        },
        {
            "id": 4,
            "codigo": "PN-004",
            "nombre": "Gorra",
            "categoria": "Accesorios",
            "precio_venta": 12.0,
            "margen_pct": 60.0,
        },
    ]

    # Actualizar vista con los productos (vía controller o directamente)
    view.update_products(sample_products)

    # Centrar ventana en pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1200
    window_height = 800
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Iniciar loop principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()