from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "enrollment.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection(database_path: str | Path = DATABASE_PATH) -> sqlite3.Connection:
    """Create a SQLite connection with foreign keys enabled."""
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: str | Path = DATABASE_PATH) -> None:
    """Create database tables from the SQL schema file."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection(database_path) as connection:
        connection.executescript(schema_sql)
