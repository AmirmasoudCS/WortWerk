import random
import time

from config.paths import SQLITE_DATABASE
from src.database.database import Database
from src.vocabulary.repository import VocabularyRepository
from scripts.utils.formatter import (
    print_error,
    print_info,
    print_success,
)
from scripts.utils.helper import clear_screen


VALID_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


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
    print("A1  A2  B1  B2  C1  C2")
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
                f"Choose from: {', '.join(VALID_LEVELS)}."
            )
            continue

        return list(dict.fromkeys(levels))


def ask_article() -> str | None:
    """Ask the user for an article answer."""

    while True:
        value = input(
            "Your answer (der/die/das, or 'q' to quit): "
        ).strip().lower()

        if value == "q":
            return None

        if value in {"der", "die", "das"}:
            return value

        print_error("Please enter der, die, das, or q.")


def show_question(
    row,
    question_number: int,
    total_questions: int,
) -> str | None:
    """Display a practice question and return the user's answer."""

    clear_screen()

    print(f"Question {question_number}/{total_questions}")
    print()
    print(f"                    {row['german']}")
    print()
    print("What is the correct article?")
    print()
    print("  1. der")
    print("  2. die")
    print("  3. das")
    print()

    return ask_article()


def show_correct_answer(row) -> None:
    """Display feedback for a correct answer."""

    print()
    print_success("Correct!")
    print()
    print(f"    {row['article']} {row['german']}")


def show_wrong_answer(row) -> None:
    """Display feedback for an incorrect answer."""

    print()
    print_error("Incorrect!")
    print()
    print("The correct form is:")
    print()
    print(f"    {row['article']} {row['german']}")
    print()

    input("Press Enter to continue...")


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

    clear_screen()

    print_info(
        f"Starting practice with {total_questions} word(s)."
    )
    print()
    input("Press Enter to begin...")

    for question_number, row in enumerate(rows, start=1):
        answer = show_question(
            row,
            question_number,
            total_questions,
        )

        if answer is None:
            clear_screen()
            print_info("Practice session ended.")
            return

        if answer == row["article"]:
            correct += 1

            show_correct_answer(row)

            time.sleep(2)

        else:
            incorrect += 1

            show_wrong_answer(row)

    show_summary(
        total_questions,
        correct,
        incorrect,
    )


def show_summary(
    total_questions: int,
    correct: int,
    incorrect: int,
) -> None:
    """Display the practice session summary."""

    clear_screen()

    print("╭──────────────────────────────╮")
    print("│      Practice Complete       │")
    print("├──────────────────────────────┤")
    print(f"│ Questions: {total_questions:<17} │")
    print(f"│ Correct:   {correct:<17} │")
    print(f"│ Incorrect: {incorrect:<17} │")
    print("╰──────────────────────────────╯")
    print()

    input("Press Enter to exit...")


def main() -> None:
    db = Database(SQLITE_DATABASE)
    repo = VocabularyRepository(db)

    if not db.table_exists("vocabulary"):
        print_error(
            "Database not initialized. "
            "Run 'wortwerk init' first."
        )
        db.close()
        return

    print("╭──────────────────────────────╮")
    print("│       WortWerk Practice      │")
    print("╰──────────────────────────────╯")
    print()

    word_count = ask_word_count()
    levels = ask_levels()

    practice(
        repo=repo,
        levels=levels,
        word_count=word_count,
    )

    db.close()


if __name__ == "__main__":
    main()