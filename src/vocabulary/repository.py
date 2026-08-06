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