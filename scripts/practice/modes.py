from scripts.utils.formatter import (
    print_correct_answer,
    print_wrong_answer,
    print_correct_english_answer,
    print_wrong_english_answer,
    print_correct_german_answer,
    print_wrong_german_answer,
    print_correct_plural_answer,
    print_wrong_plural_answer,
)


def get_practice_name(mode: str) -> str:
    """Return the display name for a practice mode."""

    if mode == "article":
        return "German → Article"

    if mode == "english":
        return "German → English"

    if mode == "german":
        return "English → German"

    if mode == "plural":
        return "German → Plural"

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )


def check_german_answer(
    row,
    answer: str,
    require_article: bool,
) -> bool:
    """Check an English-to-German answer.

    Accepts the German word alone when articles are optional.

    When require_article is True, the answer must include
    the correct German article.
    """

    user_answer = " ".join(
        answer.strip().lower().split()
    )

    german = row["german"].strip().lower()
    article = row["article"].strip().lower()

    if require_article:
        return user_answer == f"{article} {german}"

    if user_answer == german:
        return True

    return user_answer == f"{article} {german}"


def check_plural_answer(
    row,
    answer: str,
) -> bool:
    """Check a German-to-Plural answer."""

    if not row["plural"]:
        return False

    user_answer = " ".join(
        answer.strip().lower().split()
    )

    plural = row["plural"].strip().lower()

    articles = {
        "der",
        "die",
        "das",
    }

    parts = user_answer.split(maxsplit=1)

    if parts and parts[0] in articles:
        user_answer = (
            parts[1]
            if len(parts) > 1
            else ""
        )

    return user_answer == plural


def check_answer(
    row,
    answer: str,
    mode: str,
    require_article: bool = False,
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
        return check_german_answer(
            row,
            answer,
            require_article,
        )

    if mode == "plural":
        return check_plural_answer(
            row,
            answer,
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
        print_correct_german_answer(
            english=row["english"],
            article=row["article"],
            german=row["german"],
        )
        return

    if mode == "plural":
        print_correct_plural_answer(
            article=row["article"],
            german=row["german"],
            plural=row["plural"],
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
        print_wrong_german_answer(
            english=row["english"],
            article=row["article"],
            german=row["german"],
        )
        return

    if mode == "plural":
        print_wrong_plural_answer(
            article=row["article"],
            german=row["german"],
            plural=row["plural"],
        )
        return

    raise ValueError(
        f"Invalid practice mode: {mode}"
    )