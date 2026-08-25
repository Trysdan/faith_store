# database/migrations.py - Database Schema Migrations for Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Data Definition Language (DDL) para crear tablas,
# índices y triggers de la base de datos SQLite.
# SQL puro aislado en este módulo para cumplir separación de capas MVC.
# -------------------------------------------------------------------------
from __future__ import annotations

import sqlite3


class DatabaseMigrations:
    """Handles database schema migrations for Faith Store application.

    Contains all table creation statements, indexes, and triggers
    required for the application to function correctly.

    Tables created:
        - productos: Producto base (ID, código, nombre, precios)
        - variantes: Tallas/ variantes por producto (stock, precio por talla)
        - ventas: Historial de ventas realizadas
        - config_sistema: Configuración global (tasas BCV, USDT, umbrales)

    Indexes created:
        - idx_productos_codigo: Búsqueda por código de producto
        - idx_variantes_producto: Búsqueda por producto en variantes
        - idx_ventas_fecha: Ordenamiento de ventas por fecha

    Triggers:
        - trigger_stock_minimo: Actualiza alerta cuando stock baja del mínimo
    """

    # Database schema constants (SQL strings)
    # -------------------------------------------------------------------------

    #: SQL statement to create the productos table
    PRODUCTOS_TABLE: str = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT,
            costo_precio REAL NOT NULL DEFAULT 0.0,
            precio_venta REAL NOT NULL DEFAULT 0.0,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    #: SQL statement to create the variantes table
    VARIANTES_TABLE: str = """
        CREATE TABLE IF NOT EXISTS variantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            codigo_talla TEXT NOT NULL,
            stock_actual INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER NOT NULL DEFAULT 5,
            precio_venta_talla REAL NOT NULL DEFAULT 0.0,
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
        );
    """

    #: SQL statement to create the ventas table
    VENTAS_TABLE: str = """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variante_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            precio_total REAL NOT NULL DEFAULT 0.0,
            moneda VARCHAR(3) NOT NULL DEFAULT 'Bs',
            fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (variante_id) REFERENCES variantes (id) ON DELETE RESTRICT
        );
    """

    #: SQL statement to create the config_sistema table
    CONFIG_TABLE: str = """
        CREATE TABLE IF NOT EXISTS config_sistema (
            clave VARCHAR(50) PRIMARY KEY,
            valor TEXT NOT NULL,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    #: SQL statement to create index on productos.codigo
    INDEX_PRODUCTOS_CODIGO: str = """
        CREATE INDEX IF NOT EXISTS idx_productos_codigo ON productos (codigo);
    """

    #: SQL statement to create index on variantes.producto_id
    INDEX_VARIANTES_PRODUCTO: str = """
        CREATE INDEX IF NOT EXISTS idx_variantes_producto ON variantes (producto_id);
    """

    #: SQL statement to create index on ventas.fecha
    INDEX_VENTAS_FECHA: str = """
        CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas (fecha_venta DESC);
    """

    #: SQL statement to create trigger for stock minimum alert
    TRIGGER_STOCK_MINIMO: str = """
        CREATE TRIGGER IF NOT EXISTS trigger_stock_minimo
        AFTER UPDATE ON variantes
        WHEN NEW.stock_actual < NEW.stock_minimo
        BEGIN
            SELECT 1;
        END;
    """

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------

    @classmethod
    def crear_todas_las_tablas(cls, connection: sqlite3.Connection) -> None:
        """Create all database tables if they do not exist.

        Executes all CREATE TABLE statements in logical order
        (productos -> variantes -> ventas -> config_sistema)
        to respect foreign key dependencies.

        Args:
            connection: Active SQLite connection with foreign keys enabled.

        Raises:
            sqlite3.Error: If any table creation fails due to syntax or
                           constraint violations.

        Example:
            >>> from database.connection import DatabaseConnection
            >>> from database.migrations import DatabaseMigrations
            >>> with DatabaseConnection() as conn:
            ...     DatabaseMigrations.crear_todas_las_tablas(conn)
            ...     print("All tables created successfully")
        """
        cursor = connection.cursor()
        try:
            cursor.execute(cls.PRODUCTOS_TABLE)
            cursor.execute(cls.VARIANTES_TABLE)
            cursor.execute(cls.VENTAS_TABLE)
            cursor.execute(cls.CONFIG_TABLE)
            cursor.execute(cls.INDEX_PRODUCTOS_CODIGO)
            cursor.execute(cls.INDEX_VARIANTES_PRODUCTO)
            cursor.execute(cls.INDEX_VENTAS_FECHA)
            # Trigger requires autoincrement tables first, create after indexes
            cursor.execute(cls.TRIGGER_STOCK_MINIMO)
            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            raise sqlite3.Error(f"Error creating database tables: {e}")

    @classmethod
    def insertar_config_inicial(cls, connection: sqlite3.Connection) -> None:
        """Insert initial system configuration rows.

        Populates config_sistema with default values for
        BCV rate, USDT rate, and stock minimum thresholds.

        Args:
            connection: Active SQLite connection.

        Example:
            >>> from database.connection import DatabaseConnection
            >>> from database.migrations import DatabaseMigrations
            >>> with DatabaseConnection() as conn:
            ...     DatabaseMigrations.crear_todas_las_tablas(conn)
            ...     DatabaseMigrations.insertar_config_inicial(conn)
            ...     print("Initial config inserted")
        """
        cursor = connection.cursor()
        config_data = [
            ("bcv_rate", "35.0", "Tasa oficial Bolívares por Dólar"),
            ("usdt_rate", "1.0", "Tasa referencial USDT"),
            ("stock_minimo_default", "5", "Stock mínimo por defecto por talla"),
            ("empresa_nombre", "Faith Store", "Nombre de la empresa"),
        ]
        for clave, valor, descripcion in config_data:
            cursor.execute(
                "INSERT OR IGNORE INTO config_sistema (clave, valor) VALUES (?, ?)",
                (clave, valor),
            )
        connection.commit()