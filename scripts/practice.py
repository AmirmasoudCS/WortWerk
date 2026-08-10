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
    print_question,
    print_correct_answer,
    print_wrong_answer,
    print_practice_summary,
    prompt_article,
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
                print_error("Please enter a positive number.")
                continue

            return count

        except ValueError:
            print_error("Please enter a number or 'all'.")


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
            print_error("Please enter at least one level.")
            continue

        invalid_levels = [
            level
            for level in levels
            if level not in VALID_LEVELS
        ]

        if invalid_levels:
            print_error(
                f"Invalid level(s): {', '.join(invalid_levels)}. "
                f"Choose from: {', '.join(sorted(VALID_LEVELS))}."
            )
            continue

        return list(dict.fromkeys(levels))


def show_question(
    row,
    question_number: int,
    total_questions: int,
) -> tuple[str | None, float]:
    """Display a practice question and return the answer and response time."""

    clear_screen()

    print_question(
        german=row["german"],
        question_number=question_number,
        total_questions=total_questions,
    )

    # Start timing immediately before the user starts answering.
    start_time = time.perf_counter()

    answer = prompt_article()

    # Stop timing immediately after the user submits the answer.
    elapsed_time = time.perf_counter() - start_time

    return answer, elapsed_time


def practice(
    repo: VocabularyRepository,
    levels: list[str] | None,
    word_count: int | None,
) -> None:
    """Run a practice session."""

    rows = repo.get_practice_words(levels)

    if not rows:
        print_error("No words found for the selected levels.")
        return

    random.shuffle(rows)

    if word_count is not None and word_count < len(rows):
        rows = rows[:word_count]

    total_questions = len(rows)
    correct = 0
    incorrect = 0
    total_answer_time = 0.0

    clear_screen()

    print_info(
        f"Starting practice with {total_questions} word(s)."
    )
    print()

    input("Press Enter to begin...")

    for question_number, row in enumerate(rows, start=1):
        answer, answer_time = show_question(
            row,
            question_number,
            total_questions,
        )

        total_answer_time += answer_time

        if answer is None:
            clear_screen()
            print_info("Practice session ended.")
            return

        if answer == row["article"]:
            correct += 1

            print_correct_answer(
                article=row["article"],
                german=row["german"],
            )

            time.sleep(2)

        else:
            incorrect += 1

            print_wrong_answer(
                article=row["article"],
                german=row["german"],
            )

            input("Press Enter to continue...")

    accuracy = (correct / total_questions) * 100

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

        word_count = ask_word_count()
        levels = ask_levels()

        practice(
            repo=repo,
            levels=levels,
            word_count=word_count,
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()