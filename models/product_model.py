# models/product_model.py - ProductModel para Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Definición y validación de atributes de producto puro.
# Cumple SRP: solo maneja datos del producto, no lógica de negocio ni UI.
# -------------------------------------------------------------------------

from __future__ import annotations

from typing import Dict, List, Optional


class ProductModel:
    """Modelo de datos para un producto en el catálogo Faith Store.

    Atributos:
        id: Identificador único auto-generado.
        codigo: Código/ID del producto (ej. 'PN-001').
        nombre: Nombre del producto (ej. 'Polo Camiseta').
        categoria: Categoría del producto (ej. 'Ropa', 'Calzado').
        costo: Precio de costo unitario en Bolívares (Bs.).
        precio_venta: Precio de venta unitario en Bolívares (Bs.).
        margen_bruto_pct: Margen de ganancia en porcentaje (float, calculado).
    """

    def __init__(
        self,
        id: Optional[int] = None,
        codigo: Optional[str] = None,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        costo: float = 0.0,
        precio_venta: float = 0.0,
    ) -> None:
        self.id: Optional[int] = id
        self.codigo: Optional[str] = codigo
        self.nombre: Optional[str] = nombre
        self.categoria: Optional[str] = categoria
        self.costo: float = max(0.0, costo)
        self.precio_venta: float = max(0.0, precio_venta)
        self._margin_cache: Optional[float] = None

    @property
    def margen_bruto_pct(self) -> float:
        """Calcula y retorna el margen bruto en porcentaje.

        Fórmula: ((precio_venta - costo) / precio_venta) * 100
        Retorna 0.0 si precio_venta es 0 para evitar división por cero.
        """
        if self.precio_venta == 0:
            return 0.0
        m = ((self.precio_venta - self.costo) / self.precio_venta) * 100
        self._margin_cache = round(m, 2)
        return self._margin_cache

    @margen_bruto_pct.setter
    def margen_bruto_pct(self, value: float) -> None:
        self._margin_cache = value

    def actualizar_precios(self, costo: float, precio_venta: float) -> None:
        """Actualiza los precios del producto con validación."""
        self.costo = max(0.0, costo)
        self.precio_venta = max(0.0, precio_venta)
        self._margin_cache = None  # Invalida el cache

    def __repr__(self) -> str:
        return f"ProductModel(id={self.id}, codigo={self.codigo}, nombre={self.nombre})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductModel):
            return NotImplemented
        return (self.codigo == other.codigo
                and self.nombre == other.nombre
                and self.categoria == other.categoria)


# --- Funciones auxiliares de validación (módulo puro) ---

def validar_codigo(codigo: str) -> bool:
    """Valida que el código del producto tenga formato esperado."""
    if not codigo or not isinstance(codigo, str):
        return False
    codigo = codigo.strip()
    if len(codigo) < 3:
        return False
    # Formato esperado: prefijo-guión-número (ej. PN-001, ZS-45)
    parts = codigo.split("-")
    if len(parts) != 2:
        return False
    prefix, num = parts
    if not prefix.isalpha():
        return False
    if not num.isdigit():
        return False
    return True


def validar_precio(valor: float) -> bool:
    """Valida que un valor de precio sea positivo y razonable."""
    try:
        v = float(valor)
        return v >= 0 and v < 1_000_000
    except (ValueError, TypeError):
        return False