import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/german.db")
SCHEMA_PATH = Path("src/database/schema.sql")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")