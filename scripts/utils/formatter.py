from config.colors import (
    RESET,
    BOLD,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
)


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
        "die": MAGENTA,
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