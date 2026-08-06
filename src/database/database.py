import sqlite3
from pathlib import Path

from config.paths import DATABASE, DATABASE_SCHEMA


class Database:
    """Handles all raw SQLite operations for WortWerk."""

    def __init__(self, db_path: Path = DATABASE):
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Open a connection (and reuse it if already open)."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def initialize_schema(self, schema_path: Path = DATABASE_SCHEMA) -> None:
        """Create tables from the .sql schema file if they don't exist."""
        conn = self.connect()
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Run an INSERT/UPDATE/DELETE and commit."""
        conn = self.connect()
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor

    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        conn = self.connect()
        return conn.execute(query, params).fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        conn = self.connect()
        return conn.execute(query, params).fetchone()
    
    def table_exists(self, table_name: str) -> bool:
        row = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return row is not None