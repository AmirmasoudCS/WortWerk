from config.colors import (
    RESET,
    BOLD,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    CYAN,
    BRIGHT_RED,
)
from scripts.utils.helper import clear_screen


def colorize(text: str, color: str) -> str:
    """Apply a color to text."""
    return f"{color}{text}{RESET}"


def colorize_padded(text: str, color: str, width: int) -> str:
    """Apply a color while preserving the requested visible width."""
    return f"{color}{text:<{width}}{RESET}"


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{GREEN}[OK]{RESET} {message}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{RED}[ERROR]{RESET} {message}")


def print_info(message: str) -> None:
    """Print an informational message in yellow."""
    print(f"{YELLOW}[INFO]{RESET} {message}")


def prompt(label: str, required: bool = True) -> str:
    """Prompt the user for input. Re-prompts if required and left blank."""
    while True:
        value = input(f"{CYAN}{label}{RESET}: ").strip()

        if value or not required:
            return value

        print_error(f"{label} cannot be empty.")


def format_article(article: str) -> str:
    """Apply a color based on the German article."""
    article_colors = {
        "der": BLUE,
        "die": BRIGHT_RED,
        "das": GREEN,
    }

    color = article_colors.get(article.lower())

    if color is None:
        return article

    return colorize(article, color)


def format_level(level: str) -> str:
    """Format a CEFR level in yellow."""
    if level == "-":
        return level

    return colorize(level, YELLOW)


def format_word_table(rows) -> str:
    """Format vocabulary rows as a colored table."""

    headers = [
        "ID",
        "ART",
        "GERMAN",
        "ENGLISH",
        "PLURAL",
        "LEVEL",
    ]

    data = []

    for row in rows:
        data.append([
            str(row["id"]),
            row["article"],
            row["german"],
            row["english"],
            row["plural"] or "-",
            row["level"] or "-",
        ])

    widths = []

    for index, header in enumerate(headers):
        column_width = max(
            len(header),
            max(len(row[index]) for row in data),
        )
        widths.append(column_width)

    def format_cell(value: str, column_index: int) -> str:
        """Format and color an individual table cell."""

        if column_index == 1:
            return format_article(value)

        if column_index == 2:
            return colorize(value, BOLD)

        if column_index == 5:
            return format_level(value)

        return value

    def format_row(row) -> str:
        """Format a single table row."""

        cells = []

        for index, (value, width) in enumerate(zip(row, widths)):
            formatted_value = format_cell(value, index)

            if index == 1:
                formatted_value = (
                    formatted_value
                    + " " * (width - len(value))
                )
            elif index == 2:
                formatted_value = (
                    formatted_value
                    + " " * (width - len(value))
                )
            elif index == 5:
                formatted_value = (
                    formatted_value
                    + " " * (width - len(value))
                )
            else:
                formatted_value = f"{value:<{width}}"

            cells.append(formatted_value)

        return "│ " + " │ ".join(cells) + " │"

    top = (
        "┌─"
        + "─┬─".join("─" * width for width in widths)
        + "─┐"
    )

    separator = (
        "├─"
        + "─┼─".join("─" * width for width in widths)
        + "─┤"
    )

    bottom = (
        "└─"
        + "─┴─".join("─" * width for width in widths)
        + "─┘"
    )

    header = (
        "│ "
        + " │ ".join(
            colorize_padded(
                header,
                f"{CYAN}{BOLD}",
                width,
            )
            for header, width in zip(headers, widths)
        )
        + " │"
    )

    table_rows = [
        format_row(row)
        for row in data
    ]

    return "\n".join([
        top,
        header,
        separator,
        *table_rows,
        bottom,
    ])

def prompt_article() -> str | None:
    """Prompt the user for an article answer.

    Accepts either the article itself or its corresponding number.
    Returns None when the user chooses to quit.
    """

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
            f"(1-3, der/die/das, or q to quit){RESET}: "
        ).strip().lower()

        if value == "q":
            return None

        if value in article_choices:
            return article_choices[value]

        print_error(
            "Please enter 1, 2, 3, der, die, das, or q."
        )


def print_practice_header() -> None:
    """Print the WortWerk practice header."""

    print()
    print("╭──────────────────────────────╮")
    print("│       WortWerk Practice      │")
    print("╰──────────────────────────────╯")


def print_question(
    german: str,
    question_number: int,
    total_questions: int,
) -> None:
    """Print a practice question."""

    print(f"{CYAN}Question {question_number}/{total_questions}{RESET}")
    print()
    print(f"{BOLD}                    {german}{RESET}")
    print()
    print("What is the correct article?")
    print()
    print(f"  {BLUE}1. der{RESET}")
    print(f"  {BRIGHT_RED}2. die{RESET}")
    print(f"  {GREEN}3. das{RESET}")
    print()


def print_correct_answer(
    article: str,
    german: str,
) -> None:
    """Print feedback for a correct answer."""

    print()
    print_success("Correct!")
    print()
    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )


def print_wrong_answer(
    article: str,
    german: str,
) -> None:
    """Print feedback for an incorrect answer."""

    print()
    print_error("Incorrect!")
    print()
    print("The correct form is:")
    print()
    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )
    print()


def print_practice_summary(
    total_questions: int,
    correct: int,
    incorrect: int,
) -> None:
    """Print the practice session summary."""

    clear_screen()

    print("╭──────────────────────────────╮")
    print("│      Practice Complete       │")
    print("├──────────────────────────────┤")

    questions_label = colorize_padded(
        "Questions:",
        CYAN,
        10,
    )

    correct_label = colorize_padded(
        "Correct:",
        GREEN,
        10,
    )

    incorrect_label = colorize_padded(
        "Incorrect:",
        BRIGHT_RED,
        10,
    )

    print(
        f"│ {questions_label} "
        f"{total_questions:<17} │"
    )

    print(
        f"│ {correct_label} "
        f"{correct:<17} │"
    )

    print(
        f"│ {incorrect_label} "
        f"{incorrect:<17} │"
    )

    print("╰──────────────────────────────╯")
    print()

    input("Press Enter to exit...")