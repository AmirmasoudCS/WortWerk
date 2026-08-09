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


def format_word_table(rows) -> str:
    """Format vocabulary rows as a table."""

    headers = ["ID", "ART", "GERMAN", "ENGLISH", "PLURAL", "LEVEL"]

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

    def format_row(row) -> str:
        return (
            "│ "
            + " │ ".join(
                f"{value:<{width}}"
                for value, width in zip(row, widths)
            )
            + " │"
        )

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

    header = format_row(headers)
    table_rows = [format_row(row) for row in data]

    return "\n".join(
        [
            top,
            header,
            separator,
            *table_rows,
            bottom,
        ]
    )