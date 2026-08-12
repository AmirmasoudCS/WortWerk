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


def colorize_padded(
    text: str,
    color: str,
    width: int,
) -> str:
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


def prompt(
    label: str,
    required: bool = True,
) -> str:
    """Prompt the user for input.

    Re-prompts if the field is required and left blank.
    """

    while True:
        value = input(
            f"{CYAN}{label}{RESET}: "
        ).strip()

        if value or not required:
            return value

        print_error(
            f"{label} cannot be empty."
        )


def format_article(article: str) -> str:
    """Apply a color based on the German article."""

    article_colors = {
        "der": BLUE,
        "die": BRIGHT_RED,
        "das": GREEN,
    }

    color = article_colors.get(
        article.lower()
    )

    if color is None:
        return article

    return colorize(
        article,
        color,
    )


def format_level(level: str) -> str:
    """Format a CEFR level in yellow."""

    if level == "-":
        return level

    return colorize(
        level,
        YELLOW,
    )


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
        data.append(
            [
                str(row["id"]),
                row["article"],
                row["german"],
                row["english"],
                row["plural"] or "-",
                row["level"] or "-",
            ]
        )

    widths = []

    for index, header in enumerate(headers):
        column_width = max(
            len(header),
            max(
                len(row[index])
                for row in data
            ),
        )

        widths.append(column_width)

    def format_cell(
        value: str,
        column_index: int,
    ) -> str:
        """Format and color an individual table cell."""

        if column_index == 1:
            return format_article(value)

        if column_index == 2:
            return colorize(
                value,
                BOLD,
            )

        if column_index == 5:
            return format_level(value)

        return value

    def format_row(row) -> str:
        """Format a single table row."""

        cells = []

        for index, (value, width) in enumerate(
            zip(row, widths)
        ):
            formatted_value = format_cell(
                value,
                index,
            )

            if index in {1, 2, 5}:
                formatted_value += (
                    " " * (width - len(value))
                )
            else:
                formatted_value = (
                    f"{value:<{width}}"
                )

            cells.append(formatted_value)

        return (
            "│ "
            + " │ ".join(cells)
            + " │"
        )

    top = (
        "┌─"
        + "─┬─".join(
            "─" * width
            for width in widths
        )
        + "─┐"
    )

    separator = (
        "├─"
        + "─┼─".join(
            "─" * width
            for width in widths
        )
        + "─┤"
    )

    bottom = (
        "└─"
        + "─┴─".join(
            "─" * width
            for width in widths
        )
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
            for header, width in zip(
                headers,
                widths,
            )
        )
        + " │"
    )

    table_rows = [
        format_row(row)
        for row in data
    ]

    return "\n".join(
        [
            top,
            header,
            separator,
            *table_rows,
            bottom,
        ]
    )


def prompt_article() -> str | None:
    """Prompt the user for an article answer.

    Accepts either the article itself or its
    corresponding number.

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
    """Prompt the user for an English translation.

    Returns None when the user chooses to quit.
    """

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


def print_practice_header() -> None:
    """Print the WortWerk practice header."""

    print()
    print(
        "╭──────────────────────────────╮"
    )
    print(
        "│       WortWerk Practice      │"
    )
    print(
        "╰──────────────────────────────╯"
    )


def print_practice_mode_menu() -> None:
    """Print the available practice modes."""

    print("What would you like to practice?")
    print()

    print("  1. German → Article")
    print("  2. German → English")
    print("  3. English → German")
    print("  4. German → Plural")
    print()


def print_question(
    german: str,
    question_number: int,
    total_questions: int,
) -> None:
    """Print an article practice question."""

    print(
        f"{CYAN}Question "
        f"{question_number}/{total_questions}"
        f"{RESET}"
    )

    print()

    print(
        f"{BOLD}"
        f"                    {german}"
        f"{RESET}"
    )

    print()

    print("What is the correct article?")
    print()

    print(
        f"  {BLUE}1. der{RESET}"
    )

    print(
        f"  {BRIGHT_RED}2. die{RESET}"
    )

    print(
        f"  {GREEN}3. das{RESET}"
    )

    print()


def print_english_question(
    german: str,
    article: str,
    question_number: int,
    total_questions: int,
) -> None:
    """Print a German to English practice question."""

    print(
        f"{CYAN}Question "
        f"{question_number}/{total_questions}"
        f"{RESET}"
    )

    print()

    print(
        f"                    "
        f"{format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )

    print()

    print("What does this word mean in English?")
    print()


def print_correct_answer(
    article: str,
    german: str,
) -> None:
    """Print feedback for a correct article answer."""

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
    """Print feedback for an incorrect article answer."""

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


def print_correct_english_answer(
    article: str,
    german: str,
    english: str,
) -> None:
    """Print feedback for a correct English answer."""

    print()
    print_success("Correct!")
    print()

    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
        f" → "
        f"{english}"
    )


def print_wrong_english_answer(
    article: str,
    german: str,
    english: str,
) -> None:
    """Print feedback for an incorrect English answer."""

    print()
    print_error("Incorrect!")
    print()

    print("The correct translation is:")
    print()

    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
        f" → "
        f"{english}"
    )

    print()


def print_practice_summary(
    total_questions: int,
    correct: int,
    incorrect: int,
    accuracy: float,
    elapsed_time: float,
) -> None:
    """Print the practice session summary."""

    clear_screen()

    print(
        "╭──────────────────────────────╮"
    )

    print(
        "│      Practice Complete       │"
    )

    print(
        "├──────────────────────────────┤"
    )

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

    time_label = colorize_padded(
        "Time:",
        CYAN,
        10,
    )

    formatted_time = format_duration(
        elapsed_time
    )

    if accuracy >= 80:
        accuracy_color = GREEN
    elif accuracy >= 50:
        accuracy_color = YELLOW
    else:
        accuracy_color = BRIGHT_RED

    accuracy_label = colorize_padded(
        "Accuracy:",
        accuracy_color,
        10,
    )

    accuracy_value = colorize_padded(
        f"{accuracy:.1f}%",
        accuracy_color,
        17,
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

    print(
        "├──────────────────────────────┤"
    )

    print(
        f"│ {accuracy_label} "
        f"{accuracy_value} │"
    )

    print(
        f"│ {time_label} "
        f"{formatted_time:<17} │"
    )

    print(
        "╰──────────────────────────────╯"
    )

    print()

    input(
        "Press Enter to exit..."
    )


def format_duration(seconds: float) -> str:
    """Format elapsed seconds as HH:MM:SS or MM:SS."""

    total_seconds = int(seconds)

    hours, remainder = divmod(
        total_seconds,
        3600,
    )

    minutes, seconds = divmod(
        remainder,
        60,
    )

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return f"{minutes:02d}:{seconds:02d}"


def format_stats_table(statistics) -> str:
    """Format vocabulary statistics as a colored table."""

    articles = list(statistics.keys())

    levels = []

    for article in articles:
        for level in statistics[article]:
            if level not in levels:
                levels.append(level)

    headers = ["ARTICLE", *levels, "TOTAL"]

    data = []

    for article in articles:
        row = [article]

        for level in levels:
            row.append(
                str(
                    statistics[article].get(
                        level,
                        0,
                    )
                )
            )

        row.append(
            str(
                sum(
                    statistics[article].get(
                        level,
                        0,
                    )
                    for level in levels
                )
            )
        )

        data.append(row)

    total_row = ["TOTAL"]

    for level in levels:
        total_row.append(
            str(
                sum(
                    statistics[article].get(
                        level,
                        0,
                    )
                    for article in articles
                )
            )
        )

    grand_total = sum(
        int(row[-1])
        for row in data
    )

    total_row.append(
        str(grand_total)
    )

    widths = []

    for index, header in enumerate(headers):
        column_width = max(
            len(header),
            max(
                len(row[index])
                for row in data + [total_row]
            ),
        )

        widths.append(column_width)

    def format_cell(
        value: str,
        column_index: int,
        is_total: bool = False,
    ) -> str:
        """Format and color an individual statistics cell."""

        if column_index == 0:
            if is_total:
                return colorize(
                    value,
                    f"{CYAN}{BOLD}",
                )

            return format_article(value)

        if is_total:
            return colorize(
                value,
                BOLD,
            )

        return value

    def format_row(
        row,
        is_total: bool = False,
    ) -> str:
        """Format a single statistics row."""

        cells = []

        for index, (value, width) in enumerate(
            zip(row, widths)
        ):
            formatted_value = format_cell(
                value,
                index,
                is_total,
            )

            if index == 0:
                formatted_value += (
                    " " * (width - len(value))
                )
            else:
                formatted_value = (
                    f"{value:>{width}}"
                )

            cells.append(formatted_value)

        return (
            "│ "
            + " │ ".join(cells)
            + " │"
        )

    top = (
        "┌─"
        + "─┬─".join(
            "─" * width
            for width in widths
        )
        + "─┐"
    )

    separator = (
        "├─"
        + "─┼─".join(
            "─" * width
            for width in widths
        )
        + "─┤"
    )

    bottom = (
        "└─"
        + "─┴─".join(
            "─" * width
            for width in widths
        )
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
            for header, width in zip(
                headers,
                widths,
            )
        )
        + " │"
    )

    article_rows = [
        format_row(row)
        for row in data
    ]

    total_row = format_row(
        total_row,
        is_total=True,
    )

    return "\n".join(
        [
            top,
            header,
            separator,
            *article_rows,
            separator,
            total_row,
            bottom,
        ]
    )

def print_german_question(
    english: str,
    question_number: int,
    total_questions: int,
    require_article: bool = False,
) -> None:
    """Print an English-to-German practice question."""

    print(
        f"{CYAN}Question "
        f"{question_number}/{total_questions}{RESET}"
    )

    print()

    print(
        f"{BOLD}"
        f"                    {english}"
        f"{RESET}"
    )

    print()

    if require_article:
        print(
            "What is the German word "
            "including its article?"
        )
    else:
        print("What is the German word?")

    print()

def print_correct_german_answer(
    english: str,
    article: str,
    german: str,
) -> None:
    """Print feedback for a correct German answer."""

    print()
    print_success("Correct!")
    print()

    print(
        f"    {english}"
        f" → "
        f"{format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )


def print_wrong_german_answer(
    english: str,
    article: str,
    german: str,
) -> None:
    """Print feedback for an incorrect German answer."""

    print()
    print_error("Incorrect!")
    print()

    print("The correct German word is:")
    print()

    print(
        f"    {english}"
        f" → "
        f"{format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )

    print()

def print_plural_question(
    german: str,
    article: str,
    question_number: int,
    total_questions: int,
) -> None:
    """Print a German-to-Plural practice question."""

    print(
        f"{CYAN}Question "
        f"{question_number}/{total_questions}"
        f"{RESET}"
    )

    print()

    print(
        f"                    "
        f"{format_article(article)} "
        f"{BOLD}{german}{RESET}"
    )

    print()

    print("What is the plural?")
    print()

def print_correct_plural_answer(
    article: str,
    german: str,
    plural: str,
) -> None:
    """Print feedback for a correct plural answer."""

    print()
    print_success("Correct!")
    print()

    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
        f" → "
        f"{BOLD}{plural}{RESET}"
    )

def print_wrong_plural_answer(
    article: str,
    german: str,
    plural: str,
) -> None:
    """Print feedback for an incorrect plural answer."""

    print()
    print_error("Incorrect!")
    print()

    print("The correct plural is:")
    print()

    print(
        f"    {format_article(article)} "
        f"{BOLD}{german}{RESET}"
        f" → "
        f"{BOLD}{plural}{RESET}"
    )

    print()