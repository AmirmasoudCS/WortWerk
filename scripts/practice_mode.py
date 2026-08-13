import argparse

from config.paths import SQLITE_DATABASE

from src.database.database import Database
from src.vocabulary.repository import VocabularyRepository

from scripts.practice.prompts import (
    ask_levels,
    ask_practice_mode,
    ask_word_count,
)

from scripts.practice.session import practice

from scripts.quiz.prompts import ask_quiz_template
from scripts.quiz.quiz import quiz

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


def run_practice(
    repo: VocabularyRepository,
) -> None:
    """Launch a standard practice session."""

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

    if levels is None:
        # None means "all levels", so this is not
        # a cancellation. The practice session
        # should continue normally.
        pass

    practice(
        repo=repo,
        levels=levels,
        word_count=word_count,
        mode=mode,
    )


def run_quiz(
    repo: VocabularyRepository,
) -> None:
    """Launch quiz mode."""

    template = ask_quiz_template()

    if template is None:
        print_info(
            "Quiz session cancelled."
        )
        return

    print()

    levels = ask_levels()

    quiz(
        repo=repo,
        template=template,
        levels=levels,
    )


def main() -> None:
    """Start the WortWerk practice CLI."""

    parser = build_parser()
    args = parser.parse_args()

    db = Database(
        SQLITE_DATABASE
    )

    repo = VocabularyRepository(
        db
    )

    try:
        if not db.table_exists(
            "vocabulary"
        ):
            print_error(
                "Database not initialized. "
                "Run 'wortwerk init' first."
            )
            return

        if args.quiz:
            run_quiz(repo)
        else:
            run_practice(repo)

    finally:
        db.close()


if __name__ == "__main__":
    main()