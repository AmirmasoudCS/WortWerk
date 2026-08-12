import argparse

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


def build_parser() -> argparse.ArgumentParser:
    """Build the practice CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="python -m scripts.practice_mode",
        description="WortWerk German vocabulary practice",
    )

    parser.add_argument(
        "-q",
        "--quiz",
        action="store_true",
        help="Launch quiz mode",
    )

    return parser


def main() -> None:
    """Start the WortWerk practice CLI."""

    parser = build_parser()
    args = parser.parse_args()

    db = Database(SQLITE_DATABASE)
    repo = VocabularyRepository(db)

    try:
        if not db.table_exists("vocabulary"):
            print_error(
                "Database not initialized. "
                "Run 'wortwerk init' first."
            )
            return

        if args.quiz:
            print_info(
                "Quiz mode is not implemented yet."
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