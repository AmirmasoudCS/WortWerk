import random
import time

from config.constants import PRACTICE_SESSION_TYPE

from src.vocabulary.repository import VocabularyRepository

from scripts.practice.weak import get_weak_words

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

    question_functions = {
        "article": show_article_question,
        "english": show_english_question,
        "german": show_german_question,
        "plural": show_plural_question,
    }

    if mode not in question_functions:
        raise ValueError(
            f"Invalid practice mode: {mode}"
        )

    return question_functions[mode]


def calculate_accuracy(
    correct: int,
    attempted: int,
) -> float:
    """Calculate accuracy as a percentage."""

    if attempted == 0:
        return 0.0

    return (
        correct / attempted
    ) * 100


def save_practice_session(
    mode: str,
    levels: list[str] | None,
    questions: int,
    correct: int,
    incorrect: int,
    elapsed_time: float,
    completed: bool,
) -> None:
    """Save the results of a practice session."""

    accuracy = calculate_accuracy(
        correct,
        questions,
    )

    save_session(
        session_type=PRACTICE_SESSION_TYPE,
        mode=mode,
        levels=levels,
        questions=questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=elapsed_time,
        completed=completed,
    )


def practice(
    repo: VocabularyRepository,
    levels: list[str] | None,
    word_count: int | None,
    mode: str,
    require_article: bool = False,
    weak: bool = False,
) -> None:
    
    """Run a vocabulary practice session."""

    rows = repo.get_practice_words(
        levels
    )

    if not rows:
        print_error(
            "No words found for the selected levels."
        )
        return

    random.shuffle(rows)

    if weak:
        rows = get_weak_words(
            rows,
            mode,
            word_count if word_count is not None else len(rows),
        )
    elif (
        word_count is not None
        and word_count < len(rows)
    ):
        rows = rows[:word_count]

    total_questions = len(rows)
    attempted_questions = 0
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
            save_practice_session(
                mode=mode,
                levels=levels,
                questions=attempted_questions,
                correct=correct,
                incorrect=incorrect,
                elapsed_time=total_answer_time,
                completed=False,
            )

            clear_screen()

            print_info(
                "Practice session ended."
            )

            return

        attempted_questions += 1

        is_correct = check_answer(
            row,
            answer,
            mode,
            require_article=require_article,
        )

        record_word_result(
            word_id=row["id"],
            mode=mode,
            session_type=PRACTICE_SESSION_TYPE,
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

    save_practice_session(
        mode=mode,
        levels=levels,
        questions=attempted_questions,
        correct=correct,
        incorrect=incorrect,
        elapsed_time=total_answer_time,
        completed=True,
    )

    accuracy = calculate_accuracy(
        correct,
        attempted_questions,
    )

    print_practice_summary(
        total_questions=attempted_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
    )