from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Depth 1

DATA = ROOT / "data"
LOG = ROOT / "log"
SRC = ROOT / "src"
CONFIG = ROOT / "config"

# Depth 2

CHECKLIST = LOG / "checklist"
DATABASE = SRC / "database"
VOCABULARY = SRC / "vocabulary"
SQLITE_DATABASE = DATA / "german.db"

# Depth 3

DATABASE_SOURCE_CODE = DATABASE / "database.py"
DATABASE_SCHEM = DATABASE / "schema.sql"