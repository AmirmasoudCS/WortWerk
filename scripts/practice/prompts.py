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
            "Choose a practice mode (1-2, or q to quit): "
        ).strip().lower()

        if value == "q":
            return None

        if value == "1":
            return "article"

        if value == "2":
            return "english"

        print_error(
            "Please choose 1, 2, or q."
        )