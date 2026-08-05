import sqlite3
from pathlib import Path
from config.paths import (
    DATABASE_SCHEMA,
    SQLITE_DATABASE,
)

def get_connection():
    return sqlite3.connect(SQLITE_DATABASE)


def initialize_database():
    connection = get_connection()

    with open(DATABASE_SCHEMA, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")