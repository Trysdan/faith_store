# models/variant_model.py - VariantModel para Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Definición y validación de variantes de producto (tallas).
# Cumple SRP: solo maneja datos de variante (stock, precio por talla).
# -------------------------------------------------------------------------
from __future__ import annotations

from typing import Dict, List, Optional, Any


class VariantModel:
    """Modelo de datos para una variante de producto (talla/color).

    Atributos:
        id: Identificador único de la variante.
        producto_id: FK al Producto al que pertenece.
        codigo_talla: Código de la talla (ej. 'S', 'M', 'L' o '39', '40').
        stock_actual: Unidades disponibles en inventario.
        stock_minimo: Nivel mínimo que dispara alerta de reabastecimiento.
        precio_venta: Precio de venta específico de esta variante (puede variar por talla).
        activo: Si la variante está activa para ventas.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        producto_id: Optional[int] = None,
        codigo_talla: Optional[str] = None,
        stock_actual: int = 0,
        stock_minimo: int = 5,
        precio_venta: float = 0.0,
        activo: bool = True,
    ) -> None:
        self.id: Optional[int] = id
        self.producto_id: Optional[int] = producto_id
        self.codigo_talla: Optional[str] = codigo_talla
        self.stock_actual: int = max(0, stock_actual)
        self.stock_minimo: int = max(0, stock_minimo)
        self.precio_venta: float = max(0.0, precio_venta)
        self.activo: bool = bool(activo)

    @property
    def stock_suficiente(self) -> bool:
        """Retorna True si el stock actual está por encima del mínimo."""
        return self.stock_actual >= self.stock_minimo

    @property
    def alerta_stock(self) -> str:
        """Retorna el nivel de alerta de stock: 'verde', 'amarillo' o 'rojo'."""
        if self.stock_actual <= 0:
            return "rojo"
        if self.stock_actual <= self.stock_minimo * 2:
            return "amarillo"
        return "verde"

    def vender_unidad(self) -> bool:
        """Descuenta una unidad del stock. Retorna True si成功了."""
        if not self.activo:
            return False
        if self.stock_actual > 0:
            self.stock_actual -= 1
            return True
        return False

    def reabastecer(self, cantidad: int) -> None:
        """Añade cantidad al stock actual."""
        if cantidad > 0:
            self.stock_actual += cantidad

    def __repr__(self) -> str:
        return (
            f"VariantModel(id={self.id}, talla={self.codigo_talla}, "
            f"stock={self.stock_actual}, min={self.stock_minimo})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, VariantModel):
            return NotImplemented
        return (
            self.codigo_talla == other.codigo_talla
            and self.producto_id == other.producto_id
        )


# --- Funciones auxiliares de validación (módulo puro, sin UI) ---

def validar_codigo_talla(codigo: str) -> bool:
    """Valida códigos de talla: letras (S,M,L,XL) o números (39,40,41...)."""
    if not codigo or not isinstance(codigo, str):
        return False
    codigo = codigo.strip()
    if not codigo:
        return False
    # Tallas alfabéticas: S, M, L, XL, XXL
    tallas_alfabeticas = {"S", "M", "L", "XL", "XXL", "xs", "sm", "lg", "xL"}
    if codigo.upper() in tallas_alfabeticas:
        return True
    # Tallas numéricas: deben ser enteros > 0
    if codigo.isdigit():
        return int(codigo) > 0
    return False


def validar_stock(valor: int) -> bool:
    """Valida que un valor de stock sea entero no negativo."""
    try:
        v = int(valor)
        return v >= 0
    except (ValueError, TypeError):
        return False


def calcular_descuento_stocks(variantes: List[VariantModel]) -> Dict[str, int]:
    """Servicio puro: calcula cuántas unidades faltan para llegar al mínimo.

    Retorna un dict {codigo_talla: unidades_faltantes}.
    """
    faltantes: Dict[str, int] = {}
    for v in variantes:
        if v.stock_actual < v.stock_minimo:
            faltantes[v.codigo_talla] = v.stock_minimo - v.stock_actual
    return faltantes