from config.colors import CYAN, RESET
from config.constants import VALID_LEVELS
from scripts.utils.formatter import (
    print_error,
    print_practice_mode_menu,
)


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
            "Choose a practice mode (1-4, or q to quit): "
        ).strip().lower()

        if value == "q":
            return None

        if value == "1":
            return "article"

        if value == "2":
            return "english"

        if value == "3":
            return "german"

        if value == "4":
            return "plural"

        print_error(
            "Please choose 1, 2, 3, 4, or q."
        )


def ask_require_article() -> bool:
    """Ask whether the article is required in German answers."""

    while True:
        value = input(
            "Require the article? (y/n): "
        ).strip().lower()

        if value in {"y", "yes"}:
            return True

        if value in {"n", "no"}:
            return False

        print_error(
            "Please enter y or n."
        )


def prompt_article() -> str | None:
    """Prompt the user for a German article."""

    article_choices = {
        "1": "der",
        "2": "die",
        "3": "das",
        "der": "der",
        "die": "die",
        "das": "das",
    }

    while True:
        value = input(
            f"{CYAN}Your answer "
            f"(1-3, der/die/das, or q to quit)"
            f"{RESET}: "
        ).strip().lower()

        if value == "q":
            return None

        if value in article_choices:
            return article_choices[value]

        print_error(
            "Please enter 1, 2, 3, der, die, das, or q."
        )


def prompt_english() -> str | None:
    """Prompt the user for an English translation."""

    while True:
        value = input(
            f"{CYAN}Your answer "
            f"(or q to quit)"
            f"{RESET}: "
        ).strip()

        if value.lower() == "q":
            return None

        if value:
            return value

        print_error(
            "Please enter an answer or q to quit."
        )


def prompt_german() -> str | None:
    """Prompt the user for a German translation.

    Accepts either the German word alone or the word
    together with its article.

    Examples:
        Tisch
        der Tisch
    """

    while True:
        value = input(
            f"{CYAN}Your answer "
            f"(word or article + word, or q to quit)"
            f"{RESET}: "
        ).strip()

        if value.lower() == "q":
            return None

        if value:
            return value

        print_error(
            "Please enter an answer or q to quit."
        )


def prompt_plural() -> str | None:
    """Prompt the user for a German plural."""

    while True:
        value = input(
            f"{CYAN}Your answer "
            f"(or q to quit)"
            f"{RESET}: "
        ).strip()

        if value.lower() == "q":
            return None

        if value:
            return value

        print_error(
            "Please enter an answer or q to quit."
        )