from config.paths import SQLITE_DATABASE
from src.database.database import Database
from src.vocabulary.repository import VocabularyRepository

from scripts.practice.prompts import (
    ask_practice_mode,
    ask_word_count,
    ask_levels,
)
from scripts.practice.session import practice
from scripts.utils.formatter import (
    print_error,
    print_info,
    print_practice_header,
)


def main() -> None:
    """Start the WortWerk practice CLI."""

    db = Database(SQLITE_DATABASE)
    repo = VocabularyRepository(db)

    try:
        if not db.table_exists("vocabulary"):
            print_error(
                "Database not initialized. "
                "Run 'wortwerk init' first."
            )
            return

        print_practice_header()
        print()

        mode = ask_practice_mode()

        if mode is None:
            print_info(
                "Practice session cancelled."
            )
            return

        print()

        word_count = ask_word_count()
        levels = ask_levels()

        practice(
            repo=repo,
            levels=levels,
            word_count=word_count,
            mode=mode,
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()