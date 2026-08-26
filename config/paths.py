from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


# Depth 1

DATA = ROOT / "data"
LOG = ROOT / "log"
SRC = ROOT / "src"
CONFIG = ROOT / "config"
HISTORY = ROOT / "history"
TEMPLATES = DATA / "templates"
PROGRESS_DIR = ROOT / "progress"
EXPORTS = ROOT / "exports"

# Depth 2

CHECKLIST = LOG / "checklist"
DATABASE = SRC / "database"
VOCABULARY = SRC / "vocabulary"

SQLITE_DATABASE = DATA / "german.db"

SESSIONS_HISTORY = HISTORY / "sessions.json"
ARTICLE_HISTORY = HISTORY / "article_practice_history.json"
ENGLISH_HISTORY = HISTORY / "english_practice_history.json"
GERMAN_HISTORY = HISTORY / "german_practice_history.json"
PLURAL_HISTORY = HISTORY / "plural_practice_history.json"

QUIZ_TEMPLATES = TEMPLATES / "quiz_templates.json"


# Depth 3

DATABASE_SOURCE_CODE = DATABASE / "database.py"
DATABASE_SCHEMA = DATABASE / "schema.sql"