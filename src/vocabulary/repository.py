from src.database.database import Database
from config.constants import VALID_ARTICLES, VALID_LEVELS


class DuplicateWordError(Exception):
    """Raised when a German word already exists in the vocabulary table."""


class InvalidArticleError(Exception):
    """Raised when an article is not one of der/die/das."""


class InvalidLevelError(Exception):
    """Raised when a CEFR level is invalid."""


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
        """Insert a new noun into the vocabulary table."""

        german = german.strip()
        english = english.strip()
        article = article.strip().lower()
        plural = self._normalize(plural)
        level = self._normalize_level(level)

        self._validate_article(article)
        self._validate_level(level)

        if self._word_exists(german):
            raise DuplicateWordError(
                f"'{german}' already exists in the vocabulary."
            )

        cursor = self.db.execute(
            """
            INSERT INTO vocabulary (
                german,
                english,
                article,
                plural,
                level
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                german,
                english,
                article,
                plural,
                level,
            ),
        )

        return cursor.lastrowid

    def _word_exists(self, german: str) -> bool:
        """Check whether a German word already exists."""

        row = self.db.fetch_one(
            "SELECT 1 FROM vocabulary WHERE german = ?",
            (german,),
        )

        return row is not None

    @staticmethod
    def _normalize(value: str | None) -> str | None:
        """Trim whitespace and convert empty values to None."""

        if value is None:
            return None

        value = value.strip()

        return value or None

    @staticmethod
    def _normalize_level(level: str | None) -> str | None:
        """Normalize a CEFR level to uppercase."""

        level = VocabularyRepository._normalize(level)

        if level is None:
            return None

        return level.upper()

    @staticmethod
    def _validate_article(article: str) -> None:
        """Validate a German article."""

        if article not in VALID_ARTICLES:
            raise InvalidArticleError(
                f"'{article}' is not a valid article. "
                f"Must be one of: "
                f"{', '.join(sorted(VALID_ARTICLES))}"
            )

    @staticmethod
    def _validate_level(level: str | None) -> None:
        """Validate a CEFR level."""

        if level is None:
            return

        if level not in VALID_LEVELS:
            raise InvalidLevelError(
                f"'{level}' is not a valid CEFR level. "
                f"Must be one of: "
                f"{', '.join(sorted(VALID_LEVELS))}"
            )

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
            article = article.strip().lower()
            self._validate_article(article)

            query += " AND article = ?"
            params.append(article)

        if level:
            level = self._normalize_level(level)
            self._validate_level(level)

            query += " AND level = ?"
            params.append(level)

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
            raise ValueError(
                f"Invalid sort option: {sort_by}"
            )

        direction = "DESC" if reverse else "ASC"

        query += (
            f" ORDER BY {sort_columns[sort_by]} "
            f"{direction}"
        )

        return self.db.fetch_all(
            query,
            tuple(params),
        )

    def get_word(self, word_id: int):
        """Return a vocabulary word by its ID."""

        return self.db.fetch_one(
            "SELECT * FROM vocabulary WHERE id = ?",
            (word_id,),
        )

    def delete_word(self, word_id: int) -> bool:
        """Delete a word by ID.

        Returns True if a row was deleted,
        False if no such ID exists.
        """

        if self.get_word(word_id) is None:
            return False

        self.db.execute(
            "DELETE FROM vocabulary WHERE id = ?",
            (word_id,),
        )

        return True

    def get_practice_words(
        self,
        levels: list[str] | None = None,
    ) -> list:
        """Return vocabulary words available for practice."""

        query = "SELECT * FROM vocabulary WHERE 1=1"
        params: list = []

        if levels:
            normalized_levels = []

            for level in levels:
                normalized_level = self._normalize_level(level)
                self._validate_level(normalized_level)
                normalized_levels.append(normalized_level)

            placeholders = ", ".join(
                "?" for _ in normalized_levels
            )

            query += (
                f" AND level IN ({placeholders})"
            )

            params.extend(normalized_levels)

        return self.db.fetch_all(
            query,
            tuple(params),
        )

    def update_word(
        self,
        word_id: int,
        german: str,
        english: str,
        article: str,
        plural: str | None = None,
        level: str | None = None,
    ) -> bool:
        """Update an existing vocabulary word.

        Returns True if the word was updated,
        False if the ID does not exist.
        """

        german = german.strip()
        english = english.strip()
        article = article.strip().lower()
        plural = self._normalize(plural)
        level = self._normalize_level(level)

        self._validate_article(article)
        self._validate_level(level)

        existing_word = self.get_word(word_id)

        if existing_word is None:
            return False

        duplicate = self.db.fetch_one(
            """
            SELECT 1
            FROM vocabulary
            WHERE german = ?
            AND id != ?
            """,
            (
                german,
                word_id,
            ),
        )

        if duplicate is not None:
            raise DuplicateWordError(
                f"'{german}' already exists in the vocabulary."
            )

        self.db.execute(
            """
            UPDATE vocabulary
            SET german = ?,
                english = ?,
                article = ?,
                plural = ?,
                level = ?
            WHERE id = ?
            """,
            (
                german,
                english,
                article,
                plural,
                level,
                word_id,
            ),
        )

        return True