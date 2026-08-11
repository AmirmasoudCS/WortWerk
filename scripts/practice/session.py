import random
import time

from src.vocabulary.repository import VocabularyRepository

from scripts.practice.modes import (
    check_answer,
    get_practice_name,
    show_correct_answer,
    show_wrong_answer,
)

from scripts.practice.questions import (
    show_article_question,
    show_english_question,
    show_german_question,
)

from scripts.utils.formatter import (
    print_error,
    print_info,
    print_practice_summary,
)

from scripts.utils.helper import clear_screen


def get_question_function(mode: str):
    """Return the question function for the selected practice mode."""

    if mode == "article":
        return show_article_question

    if mode == "english":
        return show_english_question

    if mode == "german":
        return show_german_question

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


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

    if word_count is not None and word_count < len(rows):
        rows = rows[:word_count]

    total_questions = len(rows)
    correct = 0
    incorrect = 0
    total_answer_time = 0.0

    practice_name = get_practice_name(mode)
    question_function = get_question_function(mode)

    clear_screen()

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
        answer, answer_time = question_function(
            row,
            question_number,
            total_questions,
        )

        total_answer_time += answer_time

        if answer is None:
            clear_screen()
            print_info(
                "Practice session ended."
            )
            return

        if check_answer(
            row,
            answer,
            mode,
        ):
            correct += 1

            show_correct_answer(
                row,
                mode,
            )

            time.sleep(2)

        else:
            incorrect += 1

            show_wrong_answer(
                row,
                mode,
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