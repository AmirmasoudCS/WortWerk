import time

from scripts.utils.formatter import (
    print_question,
    print_english_question,
    prompt_article,
    prompt_english,
)
from scripts.utils.helper import clear_screen


def show_article_question(
    row,
    question_number: int,
    total_questions: int,
) -> tuple[str | None, float]:
    """Display an article question and return the answer and response time."""

    clear_screen()

    print_question(
        german=row["german"],
        question_number=question_number,
        total_questions=total_questions,
    )

    start_time = time.perf_counter()

    answer = prompt_article()

    elapsed_time = time.perf_counter() - start_time

    return answer, elapsed_time


def show_english_question(
    row,
    question_number: int,
    total_questions: int,
) -> tuple[str | None, float]:
    """Display an English translation question and return the answer and response time."""

    clear_screen()

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