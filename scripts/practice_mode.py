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
from scripts.practice.history import (
    get_recent_sessions,
)

from scripts.quiz.prompts import ask_quiz_template
from scripts.quiz.quiz import quiz

from scripts.utils.formatter import (
    print_error,
    print_info,
    print_practice_header,
    print_history_header,
    format_session_history_table,
    print_session_details,
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

    parser.add_argument(
        "-H",
        "--history",
        action="store_true",
        help="Show practice history",
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


def run_history() -> None:
    """Display recent practice and quiz history."""

    print_history_header()

    sessions = get_recent_sessions(
        limit=10
    )

    print(
        format_session_history_table(
            sessions
        )
    )

    print()

    if not sessions:
        input(
            "Press Enter to return..."
        )
        return

    while True:
        value = input(
            "Enter a session number for details "
            "or press Enter to return: "
        ).strip()

        if not value:
            return

        try:
            session_number = int(value)
        except ValueError:
            print_error(
                "Please enter a valid session number."
            )
            continue

        if (
            session_number < 1
            or session_number > len(sessions)
        ):
            print_error(
                "Invalid session number."
            )
            continue

        session = sessions[
            session_number - 1
        ]

        print_session_details(
            session
        )

        input(
            "Press Enter to return..."
        )

        return


def main() -> None:
    """Start the WortWerk practice CLI."""

    parser = build_parser()
    args = parser.parse_args()

    if args.quiz and args.history:
        parser.error(
            "The --quiz and --history options "
            "cannot be used together."
        )

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

        if args.history:
            run_history()
        elif args.quiz:
            run_quiz(repo)
        else:
            run_practice(repo)

    finally:
        db.close()


if __name__ == "__main__":
    main()