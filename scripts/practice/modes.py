from scripts.utils.formatter import (
    print_correct_answer,
    print_wrong_answer,
    print_correct_english_answer,
    print_wrong_english_answer,
)


def get_practice_name(mode: str) -> str:
    """Return the display name for a practice mode."""

    if mode == "article":
        return "German → Article"

    if mode == "english":
        return "German → English"

    if mode == "german":
        return "English → German"

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


def check_answer(
    row,
    answer: str,
    mode: str,
) -> bool:
    """Check whether the user's answer is correct."""

    if mode == "article":
        return answer == row["article"]

    if mode == "english":
        return (
            answer.strip().lower()
            == row["english"].strip().lower()
        )

    if mode == "german":
        return (
            answer.strip().lower()
            == row["german"].strip().lower()
        )

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


def show_correct_answer(
    row,
    mode: str,
) -> None:
    """Display the correct-answer feedback."""

    if mode == "article":
        print_correct_answer(
            article=row["article"],
            german=row["german"],
        )
        return

    if mode == "english":
        print_correct_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )
        return

    if mode == "german":
        print_correct_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )
        return

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


def show_wrong_answer(
    row,
    mode: str,
) -> None:
    """Display the incorrect-answer feedback."""

    if mode == "article":
        print_wrong_answer(
            article=row["article"],
            german=row["german"],
        )
        return

    if mode == "english":
        print_wrong_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )
        return

    if mode == "german":
        print_wrong_english_answer(
            article=row["article"],
            german=row["german"],
            english=row["english"],
        )
        return

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )