import random
import time

from src.vocabulary.repository import VocabularyRepository

from scripts.practice.history import (
    record_word_result,
    save_session,
)

from scripts.practice.modes import (
    check_answer,
    show_correct_answer,
    show_wrong_answer,
)

from scripts.practice.questions import (
    show_article_question,
    show_english_question,
    show_german_question,
    show_plural_question,
)

from scripts.quiz.templates import (
    QuizTemplate,
)

from scripts.utils.formatter import (
    print_error,
    print_info,
    print_practice_summary,
)

from scripts.utils.helper import clear_screen


def get_question_function(mode: str):
    """Return the question function for a quiz mode."""

    if mode == "article":
        return show_article_question

    if mode == "english":
        return show_english_question

    if mode == "german":
        return show_german_question

    if mode == "plural":
        return show_plural_question

    raise ValueError(
        f"Invalid quiz mode: {mode}"
    )


def get_quiz_questions(
    rows,
    question_counts: dict[str, int],
) -> list[tuple[str, object]]:
    """Build and shuffle the questions for a quiz."""

    questions = []

    for mode, count in question_counts.items():
        if count <= 0:
            continue

        if not rows:
            break

        available_rows = rows.copy()
        random.shuffle(available_rows)

        selected_rows = available_rows[:count]

        for row in selected_rows:
            questions.append(
                (mode, row)
            )

    random.shuffle(questions)

    return questions


def quiz(
    repo: VocabularyRepository,
    template: QuizTemplate,
    levels: list[str] | None,
    require_article: bool = False,
) -> None:
    """Run a quiz session."""

    session_type = "quiz"

    template.validate()

    rows = repo.get_practice_words(levels)

    if not rows:
        print_error(
            "No words found for the selected levels."
        )
        return

    questions = get_quiz_questions(
        rows=rows,
        question_counts=template.question_counts,
    )

    if not questions:
        print_error(
            "Unable to generate quiz questions."
        )
        return

    total_questions = len(questions)
    attempted_questions = 0
    correct = 0
    incorrect = 0
    total_answer_time = 0.0

    clear_screen()

    print_info(
        f"Starting {template.name} quiz "
        f"with {total_questions} question(s)."
    )
    print()

    input("Press Enter to begin...")

    for question_number, (mode, row) in enumerate(
        questions,
        start=1,
    ):
        question_function = get_question_function(
            mode
        )

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
            if attempted_questions > 0:
                accuracy = (
                    correct / attempted_questions
                ) * 100
            else:
                accuracy = 0.0

            save_session(
                session_type=session_type,
                mode=template.name.lower(),
                levels=levels,
                questions=attempted_questions,
                correct=correct,
                incorrect=incorrect,
                accuracy=accuracy,
                elapsed_time=total_answer_time,
                completed=False,
            )

            clear_screen()

            print_info(
                "Quiz session ended."
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
            session_type=session_type,
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
        correct / attempted_questions
    ) * 100

    save_session(
        session_type=session_type,
        mode=template.name.lower(),
        levels=levels,
        questions=attempted_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
        completed=True,
    )

    print_practice_summary(
        total_questions=attempted_questions,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
        elapsed_time=total_answer_time,
    )