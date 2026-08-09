def print_success(message: str) -> None:
    print(f"[OK] {message}")


def print_error(message: str) -> None:
    print(f"[ERROR] {message}")


def print_info(message: str) -> None:
    print(f"[INFO] {message}")


def prompt(label: str, required: bool = True) -> str:
    """Prompt the user for input. Re-prompts if required and left blank."""
    while True:
        value = input(f"{label}: ").strip()

        if value or not required:
            return value

        print_error(f"{label} cannot be empty.")


def format_word_row(row) -> str:
    """Format a single vocabulary row as a table row."""
    plural = row["plural"] or "-"
    level = row["level"] or "-"

    return (
        f"│ "
        f"{str(row['id']):<{TABLE_WIDTHS['id']}} │ "
        f"{row['article']:<{TABLE_WIDTHS['article']}} │ "
        f"{row['german']:<{TABLE_WIDTHS['german']}} │ "
        f"{row['english']:<{TABLE_WIDTHS['english']}} │ "
        f"{plural:<{TABLE_WIDTHS['plural']}} │ "
        f"{level:<{TABLE_WIDTHS['level']}} │"
    )


def format_word_header() -> str:
    """Format the vocabulary table header."""
    return (
        f"│ "
        f"{'ID':<{TABLE_WIDTHS['id']}} │ "
        f"{'ART':<{TABLE_WIDTHS['article']}} │ "
        f"{'GERMAN':<{TABLE_WIDTHS['german']}} │ "
        f"{'ENGLISH':<{TABLE_WIDTHS['english']}} │ "
        f"{'PLURAL':<{TABLE_WIDTHS['plural']}} │ "
        f"{'LEVEL':<{TABLE_WIDTHS['level']}} │"
    )


def format_word_separator() -> str:
    """Create a horizontal separator for the vocabulary table."""
    return (
        "├─"
        + "─┼─".join(
            "─" * width
            for width in TABLE_WIDTHS.values()
        )
        + "─┤"
    )


def format_word_table(rows) -> str:
    """Format vocabulary rows as a complete table."""
    if not rows:
        return ""

    widths = {
        "id": max(
            len("ID"),
            max(len(str(row["id"])) for row in rows),
        ),
        "article": max(
            len("ART"),
            max(len(row["article"]) for row in rows),
        ),
        "german": max(
            len("GERMAN"),
            max(len(row["german"]) for row in rows),
        ),
        "english": max(
            len("ENGLISH"),
            max(len(row["english"]) for row in rows),
        ),
        "plural": max(
            len("PLURAL"),
            max(len(row["plural"] or "-") for row in rows),
        ),
        "level": max(
            len("LEVEL"),
            max(len(row["level"] or "-") for row in rows),
        ),
    }

    global TABLE_WIDTHS
    TABLE_WIDTHS = widths

    top = (
        "┌─"
        + "─┬─".join(
            "─" * width
            for width in widths.values()
        )
        + "─┐"
    )

    header = format_word_header()
    separator = format_word_separator()

    table_rows = [
        format_word_row(row)
        for row in rows
    ]

    bottom = (
        "└─"
        + "─┴─".join(
            "─" * width
            for width in widths.values()
        )
        + "─┘"
    )

    return "\n".join(
        [top, header, separator, *table_rows, bottom]
    )
