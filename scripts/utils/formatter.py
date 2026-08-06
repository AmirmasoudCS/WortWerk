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
    """Format a single vocabulary row for list output."""
    plural = row["plural"] or "-"
    level = row["level"] or "-"
    return f"{row['id']:>4}  {row['article']:<4} {row['german']:<20} {row['english']:<20} {plural:<15} {level}"


def format_word_header() -> str:
    return f"{'ID':>4}  {'ART':<4} {'GERMAN':<20} {'ENGLISH':<20} {'PLURAL':<15} {'LEVEL'}"