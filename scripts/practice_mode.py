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

from scripts.practice.weak import list_weak_words


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

    parser.add_argument(
        "-w",
        "--weak",
        action="store_true",
        help="Practice your weakest words",
    )

    parser.add_argument(
        "-sw",
        "--show-weak",
        action="store_true",
        help="Show your lowest-accuracy words",
    )

    return parser


def run_practice(
    repo: VocabularyRepository,
    weak: bool = False,
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
        weak=weak,
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

def run_show_weak(
    repo: VocabularyRepository,
) -> None:
    """Display the user's weakest words for a chosen practice mode."""

    mode = ask_practice_mode()

    if mode is None:
        print_info(
            "Cancelled."
        )
        return

    print()

    rows = repo.get_practice_words(None)

    weak_words = list_weak_words(
        rows,
        mode,
    )

    if not weak_words:
        print_info(
            "No weak words found yet. Keep practicing!"
        )
        return

    print(
        format_weak_words_table(
            weak_words
        )
    )

def main() -> None:
    """Start the WortWerk practice CLI."""

    parser = build_parser()
    args = parser.parse_args()

    if sum([args.quiz, args.history, args.weak, args.show_weak]) > 1:
        parser.error(
            "The --quiz, --history, --weak, and --show-weak options "
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
        elif args.show_weak:
            run_show_weak(repo)
        else:
            run_practice(repo, weak=args.weak)

    finally:
        db.close()


if __name__ == "__main__":
    main()