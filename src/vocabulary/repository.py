from src.database.database import Database

VALID_ARTICLES = {"der", "die", "das"}


class DuplicateWordError(Exception):
    """Raised when a german word already exists in the vocabulary table."""


class InvalidArticleError(Exception):
    """Raised when an article is not one of der/die/das."""


class VocabularyRepository:
    """Handles vocabulary-specific database operations."""

    def __init__(self, db: Database):
        self.db = db

    def add_word(
        self,
        german: str,
        english: str,
        article: str,
        plural: str | None = None,
        level: str | None = None,
    ) -> int:
        """Insert a new noun into the vocabulary table. Returns the new row id."""
        german = german.strip()
        english = english.strip()
        article = article.strip().lower()
        plural = self._normalize(plural)
        level = self._normalize(level)

        if article not in VALID_ARTICLES:
            raise InvalidArticleError(
                f"'{article}' is not a valid article. Must be one of: {', '.join(sorted(VALID_ARTICLES))}"
            )

        if self._word_exists(german):
            raise DuplicateWordError(f"'{german}' already exists in the vocabulary.")

        cursor = self.db.execute(
            """
            INSERT INTO vocabulary (german, english, article, plural, level)
            VALUES (?, ?, ?, ?, ?)
            """,
            (german, english, article, plural, level),
        )
        return cursor.lastrowid

    def _word_exists(self, german: str) -> bool:
        row = self.db.fetch_one(
            "SELECT 1 FROM vocabulary WHERE german = ?", (german,)
        )
        return row is not None

    @staticmethod
    def _normalize(value: str | None) -> str | None:
        """Trim whitespace and convert empty/whitespace-only strings to None."""
        if value is None:
            return None
        value = value.strip()
        return value or None

    def list_words(
        self,
        article: str | None = None,
        level: str | None = None,
        sort_by: str = "id",
        reverse: bool = False,
    ):
        """Return vocabulary rows, optionally filtered and sorted."""
        query = "SELECT * FROM vocabulary WHERE 1=1"
        params: list = []

        if article:
            query += " AND article = ?"
            params.append(article.strip().lower())

        if level:
            query += " AND level = ?"
            params.append(level.strip())

        sort_columns = {
            "id": "id",
            "alphabetical": "german COLLATE NOCASE",
            "level": """
                CASE level
                    WHEN 'A1' THEN 1
                    WHEN 'A2' THEN 2
                    WHEN 'B1' THEN 3
                    WHEN 'B2' THEN 4
                    WHEN 'C1' THEN 5
                    WHEN 'C2' THEN 6
                    ELSE 99
                END
            """,
        }

        if sort_by not in sort_columns:
            raise ValueError(f"Invalid sort option: {sort_by}")

        direction = "DESC" if reverse else "ASC"

        query += f" ORDER BY {sort_columns[sort_by]} {direction}"

        return self.db.fetch_all(query, tuple(params))

    def get_word(self, word_id: int):
        return self.db.fetch_one("SELECT * FROM vocabulary WHERE id = ?", (word_id,))

    def delete_word(self, word_id: int) -> bool:
        """Delete a word by id. Returns True if a row was deleted, False if no such id."""
        if self.get_word(word_id) is None:
            return False
        self.db.execute("DELETE FROM vocabulary WHERE id = ?", (word_id,))
        return True