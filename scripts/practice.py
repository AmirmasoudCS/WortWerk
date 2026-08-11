import random
import time

from config.constants import VALID_LEVELS
from config.paths import SQLITE_DATABASE
from src.database.database import Database
from src.vocabulary.repository import VocabularyRepository
from scripts.utils.formatter import (
    print_error,
    print_info,
    print_practice_header,
    print_practice_mode_menu,
    print_question,
    print_english_question,
    print_correct_answer,
    print_wrong_answer,
    print_correct_english_answer,
    print_wrong_english_answer,
    print_practice_summary,
    prompt_article,
    prompt_english,
)
from scripts.utils.helper import clear_screen


def ask_word_count() -> int | None:
    """Ask how many words the user wants to practice."""

    while True:
        value = input(
            "How many words would you like to practice? "
            "(number or 'all'): "
        ).strip().lower()

        if value == "all":
            return None

        try:
            count = int(value)

            if count <= 0:
                print_error(
                    "Please enter a positive number."
                )
                continue

            return count

        except ValueError:
            print_error(
                "Please enter a number or 'all'."
            )


def ask_levels() -> list[str] | None:
    """Ask which CEFR levels the user wants to practice."""

    print()
    print("Available levels:")
    print("  ".join(sorted(VALID_LEVELS)))
    print()

    while True:
        value = input(
            "Which levels would you like to practice? "
            "(e.g. A1 A2, or 'all'): "
        ).strip().upper()

        if value == "ALL":
            return None

        levels = value.split()

        if not levels:
            print_error(
                "Please enter at least one level."
            )
            continue

        invalid_levels = [
            level
            for level in levels
            if level not in VALID_LEVELS
        ]

        if invalid_levels:
            print_error(
                f"Invalid level(s): "
                f"{', '.join(invalid_levels)}. "
                f"Choose from: "
                f"{', '.join(sorted(VALID_LEVELS))}."
            )
            continue

        return list(dict.fromkeys(levels))


def ask_practice_mode() -> str | None:
    """Ask which type of practice the user wants."""

    while True:
        print_practice_mode_menu()

        value = input(
            "Choose a practice mode (1-2, or q to quit): "
        ).strip().lower()

        if value == "q":
            return None

        if value == "1":
            return "article"

        if value == "2":
            return "english"

        print_error(
            "Please choose 1, 2, or q."
        )


def show_question(
    row,
    question_number: int,
    total_questions: int,
    mode: str,
) -> tuple[str | None, float]:
    """Display a question and return the answer and response time."""

    clear_screen()

    if mode == "article":
        print_question(
            german=row["german"],
            question_number=question_number,
            total_questions=total_questions,
        )

        start_time = time.perf_counter()

        answer = prompt_article()

    else:
        print_english_question(
            german=row["german"],
            article=row["article"],
            question_number=question_number,
            total_questions=total_questions,
        )

        start_time = time.perf_counter()

        answer = prompt_english()

    elapsed_time = time.perf_counter() - start_time

    return answer, elapsed_time


def check_answer(
    answer: str,
    row,
    mode: str,
) -> bool:
    """Check whether the user's answer is correct."""

    if mode == "article":
        return answer == row["article"]

    return (
        answer.strip().lower()
        == row["english"].strip().lower()
    )


def show_correct_feedback(
    row,
    mode: str,
) -> None:
    """Display feedback for a correct answer."""

    if mode == "article":
        print_correct_answer(
            article=row["article"],
            german=row["german"],
        )
    else:
        print_correct_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )


def show_wrong_feedback(
    row,
    mode: str,
) -> None:
    """Display feedback for an incorrect answer."""

    if mode == "article":
        print_wrong_answer(
            article=row["article"],
            german=row["german"],
        )
    else:
        print_wrong_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )


def get_practice_name(mode: str) -> str:
    """Return the display name for a practice mode."""

    if mode == "article":
        return "German → Article"

    return "German → English"


def practice(
    repo: VocabularyRepository,
    levels: list[str] | None,
    word_count: int | None,
    mode: str,
) -> None:
    """Run a practice session."""

    rows = repo.get_practice_words(levels)

    if not rows:
        print_error(
            "No words found for the selected levels."
        )
        return

    random.shuffle(rows)

    if word_count is not None:
        rows = rows[:word_count]

    total_questions = len(rows)
    correct = 0
    incorrect = 0
    total_answer_time = 0.0

    clear_screen()

    practice_name = get_practice_name(mode)

    print_info(
        f"Starting {practice_name} practice "
        f"with {total_questions} word(s)."
    )
    print()

    input("Press Enter to begin...")

    for question_number, row in enumerate(
        rows,
        start=1,
    ):
        answer, answer_time = show_question(
            row=row,
            question_number=question_number,
            total_questions=total_questions,
            mode=mode,
        )

        total_answer_time += answer_time

        if answer is None:
            clear_screen()
            print_info(
                "Practice session ended."
            )
            return

        if check_answer(
            answer=answer,
            row=row,
            mode=mode,
        ):
            correct += 1

            show_correct_feedback(
                row=row,
                mode=mode,
            )

            time.sleep(2)

        else:
            incorrect += 1

            show_wrong_feedback(
                row=row,
                mode=mode,
            )

            input(
                "Press Enter to continue..."
            )

    accuracy = (
        correct / total_questions
    ) * 100

    print_practice_summary(
        total_questions=total_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
    )


def main() -> None:
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