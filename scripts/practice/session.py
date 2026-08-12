import random
import time

from src.vocabulary.repository import VocabularyRepository

from scripts.practice.history import (
    record_word_result,
    save_session,
)

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
    show_plural_question,
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

    if mode == "plural":
        return show_plural_question

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


def practice(
    repo: VocabularyRepository,
    levels: list[str] | None,
    word_count: int | None,
    mode: str,
    require_article: bool = False,
) -> None:
    """Run a practice session."""

    session_type = "practice"

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
        if mode == "german":
            answer, answer_time = question_function(
                row,
                question_number,
                total_questions,
                require_article=require_article,
            )
        else:
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

        is_correct = check_answer(
            row,
            answer,
            mode,
            require_article=require_article,
        )

        record_word_result(
            word_id=row["id"],
            mode=mode,
            correct=is_correct,
        )

        if is_correct:
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

    save_session(
        session_type=session_type,
        mode=mode,
        levels=levels,
        questions=total_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
    )

    print_practice_summary(
        total_questions=total_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
    )