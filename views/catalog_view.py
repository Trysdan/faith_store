# views/catalog_view.py - Catalog View for Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Presentación UI del catálogo de productos usando CustomTkinter.
# Cumple regla estricta: layouts grid/pack, NUNCA .place().
# -------------------------------------------------------------------------
from __future__ import annotations

import tkinter as tk
from typing import Optional, List, Dict, Any, Callable


class CatalogView:
    """View for Faith Store product catalog module.

    Displays the product catalog with search functionality,
    product cards with size matrices, and stock status indicators.

    Uses grid layout manager for all widgets.
    Prohibited: .place() geometry manager.

    Attributes:
        root: The parent Tkinter/CustomTkinter window.
        frame: Main frame containing all catalog components.
        search_frame: Frame containing search bar and controls.
        products_frame: Frame containing product cards grid.
    """

    def __init__(
        self,
        root: tk.Tk,
        on_product_select: Optional[Callable] = None,
        on_search: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Initialize the CatalogView with the given root window.

        Sets up the main layout structure consisting of:
        - Top search bar frame
        - Left/center product display area
        - Status bar at bottom

        Args:
            root: The parent Tk window (CustomTkinter CTkWindow expected).
            on_product_select: Callback function when a product is selected.
                               Receives product dictionary as argument.
            on_search: Callback function when user types in search bar.
                       Receives the search query string.

        Raises:
            TypeError: If root is not a valid Tk window instance.

        Example:
            >>> import customtkinter as ctk
            >>> root = ctk.CTk()
            >>> view = CatalogView(root, on_product_select=lambda p: print(p['nombre']))
            >>> view.frame.pack(fill="both", expand=True)
        """
        if not isinstance(root, tk.Tk):
            raise TypeError("root must be a tk.Tk instance.")

        self.root = root
        self.on_product_select = on_product_select
        self.on_search = on_search

        # Configure root window minimum size
        self.root.minsize(width=800, height=600)

        # Create main frame
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create UI components
        self._create_search_frame()
        self._create_products_frame()
        self._create_status_bar()

        # Bind Enter key in search entry
        self.search_entry.bind("<Return>", self._on_search_keypress)

    def _create_search_frame(self) -> None:
        """Create the top search bar frame.

        Contains the main search entry and filter controls.
        Uses grid layout with proportional column weights.
        """
        self.search_frame = tk.Frame(self.frame, bg="#f0f0f0", height=50)
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.search_frame.grid_columnconfigure(0, weight=1)

        # Search label
        self.search_label = tk.Label(
            self.search_frame,
            text="Buscar producto (código o nombre):",
            bg="#f0f0f0",
            font=("Helvetica", 10, "bold"),
        )
        self.search_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Search entry
        self.search_entry = tk.Entry(self.search_frame, font=("Helvetica", 10))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_keyrelease)

        # Search button
        self.search_button = tk.Button(
            self.search_frame,
            text="Buscar",
            font=("Helvetica", 10, "bold"),
            command=self._on_search_click,
        )
        self.search_button.grid(row=0, column=2, sticky="e")

    def _on_search_click(self) -> None:
        """Handle search button click event."""
        query = self.search_entry.get().strip()
        if query and self.on_search:
            self.on_search(query)

    def _on_search_keypress(self, event: tk.Event) -> None:
        """Handle search entry key press event (Enter key).

        Args:
            event: The Tkinter key press event.
        """
        if event.keysym == "Return":
            self._on_search_click()

    def _on_keyrelease(self, event: tk.Event) -> None:
        """Handle key release in search entry (debounce support).

        Args:
            event: The Tkinter key release event.
        """
        query = self.search_entry.get().strip()
        if query and self.on_search:
            # Simple debounce: call after 300ms
            self.root.after(300, lambda: self.on_search(query))

    def _create_products_frame(self) -> None:
        """Create the main product display frame.

        Contains a grid of product cards with size matrices
        and stock status indicators.
        """
        self.products_frame = tk.Frame(self.frame, bg="#ffffff")
        self.products_frame.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=(0, 10)
        )
        # Configure grid to expand with window resizing
        # We'll add product cards dynamically, so configure enough columns
        for i in range(3):
            self.products_frame.grid_columnconfigure(i, weight=1)
        self.products_frame.grid_rowconfigure(0, weight=1)

        # Title label
        self.title_label = tk.Label(
            self.products_frame,
            text="Catálogo de Productos",
            bg="#ffffff",
            font=("Helvetica", 14, "bold"),
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    def _create_status_bar(self) -> None:
        """Create the bottom status bar.

        Displays overall application status information.
        """
        self.status_frame = tk.Frame(self.frame, bg="#e0e0e0", height=30)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = tk.Label(
            self.status_frame,
            text="Listo - Seleccione un producto para comenzar",
            bg="#e0e0e0",
            font=("Helvetica", 9),
            fg="#666666",
        )
        self.status_label.grid(row=0, column=0, sticky="w")

    def update_products(self, products: List[Dict[str, Any]]) -> None:
        """Update the product display with new data.

        Clears existing product cards and renders the new product list.
        Each product is displayed as a card with its details and size matrix.

        Args:
            products: A list of dictionaries, each containing product data:
                      - id: Product ID
                      - codigo: Product code
                      - nombre: Product name
                      - categoria: Product category
                      - costo: Cost price
                      - precio_venta: Sale price
                      - margen_pct: Gross profit percentage

        Raises:
            TypeError: If products is not a list.
            ValueError: If products list is empty or contains invalid data.

        Example:
            >>> view = CatalogView(root)
            >>> products = [
            ...     {"id": 1, "codigo": "PN-001", "nombre": "Polo", "categoria": "Ropa",
            ...      "costo": 15.0, "precio_venta": 25.0, "margen_pct": 40.0}
            ... ]
            >>> view.update_products(products)
        """
        if not isinstance(products, list):
            raise TypeError("products must be a list.")
        if not products:
            self._show_empty_state()
            return

        # Clear existing widgets in the products frame
        # Keep the title label, remove all other widgets
        for widget in self.products_frame.winfo_children():
            if widget != self.title_label:
                widget.destroy()

        # Render product cards in a grid (3 columns max)
        for index, product in enumerate(products):
            row = (index // 3) + 1  # +1 to skip title row
            col = index % 3

            # Make sure grid columns exist
            if col >= 3:
                col = 0
                row = (index // 3) + 1

            self._create_product_card(product, row, col)

    def _create_product_card(
        self, product: Dict[str, Any], row: int, col: int
    ) -> None:
        """Create a single product card widget.

        Args:
            product: Dictionary with product data (see update_products docstring).
            row: Grid row position.
            col: Grid column position.

        Raises:
            KeyError: If required product keys are missing.

        Example:
            >>> product = {"id": 1, "codigo": "PN-001", "nombre": "Polo",
            ...            "categoria": "Ropa", "precio_venta": 25.0, "margen_pct": 40.0}
            >>> card = view._create_product_card(product, 1, 0)
        """
        # Required keys check
        required_keys = ["nombre", "codigo", "precio_venta", "margen_pct"]
        missing = [k for k in required_keys if k not in product]
        if missing:
            raise KeyError(f"Missing product keys: {missing}")

        # Card frame
        card = tk.Frame(
            self.products_frame,
            bg="white",
            relief="raised",
            borderwidth=1,
        )
        card.grid(
            row=row, column=col, padx=(0, 5), pady=5, sticky="ew"
        )
        card.grid_columnconfigure(0, weight=1)

        # Product name
        name_label = tk.Label(
            card,
            text=product["nombre"],
            bg="white",
            font=("Helvetica", 11, "bold"),
            anchor="w",
        )
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))

        # Product code
        code_label = tk.Label(
            card,
            text=f"Código: {product.get('codigo', 'N/A')}",
            bg="white",
            font=("Helvetica", 9),
            anchor="w",
        )
        code_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # Price information
        precio_venta = product.get("precio_venta", 0.0)
        margen_pct = product.get("margen_pct", 0.0)

        price_label = tk.Label(
            card,
            text=f"Bs. {precio_venta:.2f}  |  Margen: {margen_pct}%",
            bg="white",
            font=("Helvetica", 9),
            anchor="w",
        )
        price_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # Stock/status info (using variant model logic concept)
        # In a full implementation, this would connect to VariantModel
        stock_info = tk.Label(
            card,
            text="Stock: -- (consultar)",
            bg="white",
            font=("Helvetica", 8),
            anchor="w",
            fg="#666666",
        )
        stock_info.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        # Color-code margin percentage
        try:
            margen_float = float(margen_pct)
            if margen_float >= 30:
                margen_color = "green"
            elif margen_float >= 15:
                margen_color = "orange"
            else:
                margen_color = "red"
        except (ValueError, TypeError):
            margen_color = "gray"

        margen_color_label = tk.Label(
            card,
            text=f"[{margen_color}]",
            bg="white",
            font=("Helvetica", 8),
            anchor="e",
        )
        margen_color_label.grid(row=3, column=0, sticky="e", padx=10, pady=2)

        # Bind click event to open product details
        card.bind(
            "<Button-1>",
            lambda e, p=product: self._on_product_click(p),
        )
        name_label.bind(
            "<Button-1>",
            lambda e, p=product: self._on_product_click(p),
        )

    def _on_product_click(self, product: Dict[str, Any]) -> None:
        """Handle product card click event.

        Triggers the on_product_select callback if configured.

        Args:
            product: The product dictionary that was clicked.

        Example:
            >>> view = CatalogView(root, on_product_select=lambda p: print(p))
            >>> product = {"id": 1, "nombre": "Polo", "codigo": "PN-001"}
            >>> view._on_product_click(product)
        """
        if self.on_product_select:
            self.on_product_select(product)

    def _show_empty_state(self) -> None:
        """Display a message when no products are available.

        Clears the products frame and shows a message indicating
        that no products are currently loaded.
        """
        # Clear existing product cards
        for widget in self.products_frame.winfo_children():
            if widget != self.title_label:
                widget.destroy()

        # Show empty state message
        empty_label = tk.Label(
            self.products_frame,
            text="No hay productos cargados\nuse la búsqueda para encontrar productos",
            bg="#ffffff",
            font=("Helvetica", 12),
            fg="#999999",
            anchor="center",
        )
        empty_label.grid(
            row=1, column=0, columnspan=3, pady=50, sticky="nsew"
        )

    def set_search_query(self, query: str) -> None:
        """Programmatically set the search query text.

        Args:
            query: The search string to set in the search entry field.

        Example:
            >>> view.set_search_query("Polo")
        """
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, "end")
            self.search_entry.insert(0, query)

    def get_search_query(self) -> str:
        """Get the current search query from the search entry.

        Returns:
            str: The current text in the search entry field,
                 or empty string if no search entry exists.

        Example:
            >>> query = view.get_search_query()
            >>> print(f"Current search: {query}")
        """
        if hasattr(self, "search_entry"):
            return self.search_entry.get().strip()
        return ""

    def set_status_message(self, message: str, color: str = "#666666") -> None:
        """Set the status bar message.

        Args:
            message: The message to display in the status bar.
            color: Text color for the message (supports HTML color names).

        Example:
            >>> view.set_status_message("Presione F10 para ayuda", "#006600")
        """
        if hasattr(self, "status_label"):
            self.status_label.config(text=message, fg=color)

    def clear_search(self) -> None:
        """Clear the search entry field and reset the product display.

        Shows all products by calling update_products with an empty state
        or can be combined with a search filter.
        """
        self.set_search_query("")