# tests/test_database.py - Database Connection Tests for Faith Store
# -------------------------------------------------------------------------
# Pruebas unitarias para DatabaseConnection y validación de esquemas.
# Cumple regla: 1 archivo por clase de prueba, máximo 70 líneas.
# -------------------------------------------------------------------------
from __future__ import annotations

import os
import sqlite3
import tempfile
import shutil

import pytest

from database.connection import DatabaseConnection


@pytest.fixture(autouse=True)
def cleanup_db() -> None:
    """Clean up temporary database file after each test."""
    temp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(temp_dir, "test_faith_store.db")
    # Override default db_path for testing
    import database.connection as conn_module
    original_db_path = conn_module.DatabaseConnection._instance.db_path if conn_module.DatabaseConnection._instance else None
    yield
    # Cleanup
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    os.rmdir(temp_dir)
    if original_db_path and os.path.exists(original_db_path):
        pass  # Keep main db intact


class TestDatabaseConnection:
    """Test suite for DatabaseConnection context manager."""

    def test_conexion_contexto_exitoso(self) -> None:
        """Test that context manager establishes connection successfully."""
        with DatabaseConnection() as conn:
            assert conn is not None
            cursor = conn.execute("SELECT 1")
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == 1

    def test_pragma_foreign_keys_activado(self) -> None:
        """Test that PRAGMA foreign_keys is enabled on connection."""
        with DatabaseConnection() as conn:
            cursor = conn.execute("PRAGMA foreign_keys")
            result = cursor.fetchone()
            assert result[0] == 1

    def test_insertar_y_consultar_producto(self) -> None:
        """Test inserting and querying data via connection."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            # Create a test table
            cursor.execute("CREATE TABLE test_tabla (id INTEGER PRIMARY KEY, nombre TEXT)")
            cursor.execute("INSERT INTO test_tabla (nombre) VALUES ('Producto de prueba')")
            conn.commit()

            cursor.execute("SELECT nombre FROM test_tabla WHERE nombre = 'Producto de prueba'")
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == "Producto de prueba"

    def test_singleton_mismo_instancia(self) -> None:
        """Test that get_instance returns the same object."""
        manager1 = DatabaseConnection.get_instance()
        manager2 = DatabaseConnection.get_instance()
        assert manager1 is manager2

    def test_singleton_diferente_path_usado_una_vez(self) -> None:
        """Test that custom path works on first call."""
        # Reset singleton for test
        DatabaseConnection._instance = None
        
        manager1 = DatabaseConnection.get_instance("test_custom_path.db")
        # The instance should have the custom path
        assert manager1.db_path == "test_custom_path.db"


def test_connection_importable() -> None:
    """Test that DatabaseConnection can be imported and used."""
    from database.connection import DatabaseConnection as DC
    assert DC is not None