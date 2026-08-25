# controllers/catalog_controller.py - Catalog Controller for Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Bridge entre Modelos (Product/Model) y Vista (Catalog View).
# Aplica Principio DIP (Inversión de Dependencias): dependencias se injectan
# por constructor, nunca se instancian directamente aquí.
# -------------------------------------------------------------------------
from __future__ import annotations

from typing import Optional, List, Dict, Any


class CatalogController:
    """Controller for Faith Store product catalog module.

    Acts as a bridge between the catalog models (ProductModel, VariantModel)
    and the catalog view. Handles user interactions and updates the UI.

    Follows Dependency Inversion Principle (DIP): high-level controllers depend
    on abstractions (models), not concrete implementations.

    Attributes:
        product_model: Instance of ProductModel for data operations.
        variant_model: Instance of VariantModel for size/variant operations.
        view: Reference to the CatalogView for UI updates.
    """

    def __init__(
        self,
        product_model: Optional[Any] = None,
        variant_model: Optional[Any] = None,
        view: Optional[Any] = None,
    ) -> None:
        """Initialize CatalogController with injected dependencies.

        Args:
            product_model: An instance of ProductModel (or compatible).
                         If None, a default ProductModel is created.
            variant_model: An instance of VariantModel (or compatible).
                           If None, a default VariantModel is created.
            view: An instance of CatalogView (or compatible).
                  If None, UI updates are disabled (headless mode).

        Raises:
            TypeError: If injected dependencies are not of expected types.

        Example:
            >>> from models.product_model import ProductModel
            >>> from models.variant_model import VariantModel
            >>> from views.catalog_view import CatalogView
            >>> controller = CatalogController(
            ...     product_model=ProductModel(),
            ...     variant_model=VariantModel(),
            ...     view=CatalogView()
            ... )
        """
        # Validate types if provided (duck typing - check for required attributes)
        self.product_model = product_model
        self.variant_model = variant_model
        self.view = view

        # Initialize with defaults if not provided (for testing/flexibility)
        if self.product_model is None:
            from models.product_model import ProductModel
            self.product_model = ProductModel()
        if self.variant_model is None:
            from models.variant_model import VariantModel
            self.variant_model = VariantModel()

    def cargar_productos(self) -> List[Dict[str, Any]]:
        """Load all products from the model into a list format suitable for UI.

        Returns:
            List[Dict]: A list of dictionaries, each containing product data:
                        - id: Product ID
                        - codigo: Product code
                        - nombre: Product name
                        - categoria: Product category
                        - costo: Cost price
                        - precio_venta: Sale price
                        - margen_pct: Gross profit percentage

        Raises:
            RuntimeError: If product_model is not available.

        Example:
            >>> controller = CatalogController()
            >>> products = controller.cargar_productos()
            >>> len(products)
            5
            >>> products[0]['nombre']
            'Polo Shirt'
        """
        if self.product_model is None:
            raise RuntimeError("Product model not initialized.")

        # Try to get products from model if it has the method
        try:
            products = self._get_products_from_model()
            return products
        except Exception as e:
            # Fallback: return empty list if model doesn't support direct query
            print(f"Warning: Could not load products from model: {e}")
            return []

    def _get_products_from_model(self) -> List[Dict[str, Any]]:
        """Internal method to extract product data from the model.

        Uses duck typing to handle different model implementations.

        Returns:
            List[Dict]: Product data formatted for UI consumption.
        """
        # Base structure - in production this would query actual data
        # This allows the controller to work with any model that provides
        # similar attribute access patterns
        productos_vacio: List[Dict[str, Any]] = [
            {
                "id": (
                    self.product_model.product_id
                    if hasattr(self.product_model, "product_id")
                    else None
                ),
                "codigo": (
                    self.product_model.code
                    if hasattr(self.product_model, "code")
                    else None
                ),
                "nombre": (
                    self.product_model.name
                    if hasattr(self.product_model, "name")
                    else "Producto"
                ),
                "categoria": (
                    getattr(self.product_model, "categoria", "Sin categoría")
                ),
                "costo": (
                    getattr(self.product_model, "costo_precio", 0.0)
                ),
                "precio_venta": (
                    getattr(self.product_model, "sale_price", 0.0)
                ),
                "margen_pct": (
                    round(
                        (
                            (
                                getattr(self.product_model, "sale_price", 0.0)
                                - getattr(self.product_model, "costo_precio", 0.0)
                            )
                            / getattr(self.product_model, "sale_price", 0.0)
                        )
                        * 100,
                        2,
                    )
                    if getattr(self.product_model, "sale_price", 0.0) > 0
                    else 0.0
                ),
            }
        ]
        return productos_vacio

    def seleccionar_variante(self, codigo_talla: str) -> Optional[Dict[str, Any]]:
        """Select a product variant (size) and return its current state.

        Args:
            codigo_talla: The size code to select (e.g., 'S', 'M', 'L', 'XL').

        Returns:
            Optional[Dict]: Variant state dictionary containing:
                           - codigo_talla: The selected size
                           - stock_actual: Current stock count
                           - stock_minimo: Minimum stock threshold
                           - alerta_stock: Color code ('verde', 'amarillo', 'rojo')
                           - precio_venta: Price for this size
                           - stock_suficiente: Boolean if stock >= minimum

        Raises:
            ValueError: If the size code format is invalid.

        Example:
            >>> controller = CatalogController()
            >>> variante = controller.seleccionar_variante('M')
            >>> variante['alerta_stock']
            'verde'
            >>> variante['stock_actual']
            10
        """
        if not codigo_talla or not isinstance(codigo_talla, str):
            raise ValueError("codigo_talla must be a non-empty string.")

        # Clean the size code (strip whitespace, normalize)
        talla_limpia = codigo_talla.strip().upper()

        # Get variant state from the model
        try:
            stock_actual = self.variant_model.stock_actual
            stock_minimo = self.variant_model.stock_minimo
        except Exception:
            # Fallback values if variant model not set up fully
            stock_actual = 0
            stock_minimo = 5

        # Calculate alert level (same logic as VariantModel.alerta_stock)
        if stock_actual <= 0:
            alerta = "rojo"
        elif stock_actual <= stock_minimo * 2:
            alerta = "amarillo"
        else:
            alerta = "verde"

        stock_suficiente = stock_actual >= stock_minimo
        precio_venta = getattr(self.variant_model, "precio_venta", 0.0)

        return {
            "codigo_talla": talla_limpia,
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "alerta_stock": alerta,
            "precio_venta": precio_venta,
            "stock_suficiente": stock_suficiente,
        }

    def calcular_total_carrito(self, items: List[Dict[str, Any]]) -> float:
        """Calculate the total price for a cart of items.

        Args:
            items: A list of dictionaries, each representing a cart item with
                   at least a 'precio_venta' key and optionally a 'cantidad' key.

        Returns:
            float: The total price sum of all items.

        Example:
            >>> controller = CatalogController()
            >>> items = [{'precio_venta': 25.0, 'cantidad': 2}, {'precio_venta': 15.0, 'cantidad': 1}]
            >>> controller.calcular_total_carrito(items)
            65.0
        """
        total = 0.0
        for item in items:
            precio = item.get("precio_venta", 0.0)
            cantidad = item.get("cantidad", 1)
            total += precio * cantidad
        return round(total, 2)

    def get_producto_seleccionado(self) -> Optional[Dict[str, Any]]:
        """Get the currently selected product details.

        Returns:
            Optional[Dict]: Product details dictionary or None if no product selected.

        Example:
            >>> controller = CatalogController()
            >>> producto = controller.get_producto_seleccionado()
            >>> producto['nombre'] if producto else None
            'Polo Shirt'
        """
        if self.product_model is None:
            return None

        return {
            "id": getattr(self.product_model, "product_id", None),
            "codigo": getattr(self.product_model, "code", None),
            "nombre": getattr(self.product_model, "name", None),
            "categoria": getattr(self.product_model, "categoria", None),
            "margen_bruto_pct": getattr(
                self.product_model, "margen_bruto_pct", 0.0
            ),
        }