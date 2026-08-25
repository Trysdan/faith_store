# database/connection.py - Database Connection Manager for Faith Store
# -------------------------------------------------------------------------
# Responsabilidad: Singleton context manager para conexiones SQLite.
# Proporciona acceso controlado a la base de datos con foreign keys activado.
# -------------------------------------------------------------------------
from __future__ import annotations

import sqlite3
from typing import ContextManager


class DatabaseConnection:
    """Singleton context manager for Faith Store SQLite database.

    Ensures foreign keys are enabled and provides automatic connection closing.
    Use via: `with DatabaseConnection() as conn: ...`

    Attributes:
        db_path: Path to the SQLite database file.
        _instance: Class-level instance to enforce singleton behavior.
    """

    _instance = None

    def __init__(self, db_path: str = "database/faith_store.db") -> None:
        """Initialize DatabaseConnection with specified database path.

        Args:
            db_path: File path where the SQLite database will be stored.
                     Defaults to "database/faith_store.db" relative to project root.

        Raises:
            ValueError: If db_path is empty or not a string.
        """
        if not db_path or not isinstance(db_path, str):
            raise ValueError("db_path must be a non-empty string.")
        self.db_path: str = db_path

    def __enter__(self) -> sqlite3.Connection:
        """Open SQLite connection with foreign keys enabled.

        Returns:
            sqlite3.Connection: Active connection with foreign keys ON.

        Example:
            >>> with DatabaseConnection() as conn:
            ...     cursor = conn.execute("SELECT 1")
            ...     print("Connection established")
        """
        connection: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        connection.commit()
        return connection

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """Close the SQLite connection automatically.

        Ensures the connection is properly closed when exiting the context,
        even if an exception occurred inside the `with` block.

        Args:
            exc_type: Exception type if an error occurred (None otherwise).
            exc_val: Exception value if an error occurred (None otherwise).
            exc_tb: Traceback if an error occurred (None otherwise).

        Example:
            >>> with DatabaseConnection() as conn:
            ...     # Operations happen here
            ...     pass  # Connection auto-closes after this block
        """
        connection: sqlite3.Connection = sqlite3.connect(self.db_path)
        if connection:
            connection.close()

    @classmethod
    def get_instance(cls, db_path: str = "database/faith_store.db") -> DatabaseConnection:
        """Get or create the singleton instance of DatabaseConnection.

        Args:
            db_path: Database file path (used only on first call).

        Returns:
            DatabaseConnection: The singleton instance.

        Example:
            >>> conn_manager = DatabaseConnection.get_instance()
            >>> with conn_manager as db:
            ...     # Use database
            ...     pass
        """
        if cls._instance is None:
            cls._instance = DatabaseConnection(db_path)
        return cls._instance


def test_connection() -> bool:
    """Test that the database connection manager works correctly.

    Creates an in-memory database, verifies foreign keys are enabled,
    and returns True if the connection is successful.

    Returns:
        bool: True if connection test passes, False otherwise.

    Example:
        >>> from database.connection import test_connection
        >>> result = test_connection()
        >>> print(f"Connection test: {result}")
        Connection test: True
    """
    try:
        with DatabaseConnection(":memory:") as conn:
            cursor = conn.execute("SELECT 1")
            result = cursor.fetchone()
            return result is not None and result[0] == 1
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False