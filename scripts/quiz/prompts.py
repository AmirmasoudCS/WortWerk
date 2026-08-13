from config.colors import CYAN, RESET
from config.constants import VALID_PRACTICE_MODES

from scripts.quiz.templates import (
    QuizTemplate,
    DEFAULT_QUIZ_TEMPLATES,
)

from scripts.quiz.template_repository import (
    load_templates,
    save_template,
)

from scripts.utils.formatter import print_error


MODE_NAMES = {
    "article": "German → Article",
    "english": "German → English",
    "german": "English → German",
    "plural": "German → Plural",
}


def ask_quiz_template() -> QuizTemplate | None:
    """Ask the user which quiz template they want."""

    templates = list(
        DEFAULT_QUIZ_TEMPLATES.items()
    )

    while True:
        print()
        print("What type of quiz would you like?")
        print()

        for index, (_, template) in enumerate(
            templates,
            start=1,
        ):
            print(
                f"  {index}. "
                f"{template.name} "
                f"({template.total_questions} questions)"
            )

        custom_option = len(templates) + 1
        saved_option = custom_option + 1

        print(
            f"  {custom_option}. Custom"
        )

        print(
            f"  {saved_option}. Saved templates"
        )

        print()

        value = input(
            "Choose a quiz type "
            f"(1-{saved_option}, or q to quit): "
        ).strip().lower()

        if value == "q":
            return None

        try:
            choice = int(value)
        except ValueError:
            print_error(
                f"Please choose 1-{saved_option}, "
                "or q to quit."
            )
            continue

        if 1 <= choice <= len(templates):
            return templates[choice - 1][1]

        if choice == custom_option:
            return ask_custom_quiz()

        if choice == saved_option:
            return ask_saved_quiz()

        print_error(
            f"Please choose 1-{saved_option}, "
            "or q to quit."
        )


def ask_custom_quiz() -> QuizTemplate | None:
    """Build a custom quiz template interactively."""

    print()
    print("Custom Quiz")
    print()

    question_counts = {}

    for mode in VALID_PRACTICE_MODES:
        count = ask_question_count(mode)

        if count is None:
            return None

        question_counts[mode] = count

    template = QuizTemplate(
        name="Custom",
        question_counts=question_counts,
    )

    try:
        template.validate()
    except ValueError as error:
        print_error(str(error))
        return None

    print()
    print(
        f"Total questions: "
        f"{template.total_questions}"
    )
    print()

    if not ask_confirmation(
        "Create this quiz? (y/n): "
    ):
        return None

    if ask_confirmation(
        "Save this quiz as a reusable template? (y/n): "
    ):
        name = ask_quiz_template_name()

        if name is None:
            return template

        template.name = name

        try:
            save_template(template)

            print()
            print(
                f"Quiz template '{name}' saved."
            )

        except ValueError as error:
            print_error(str(error))

    return template


def ask_question_count(
    mode: str,
) -> int | None:
    """Ask how many questions of a type to include."""

    name = MODE_NAMES.get(
        mode,
        mode,
    )

    while True:
        value = input(
            f"How many {name} questions? "
            "(0 or a positive number, or q to quit): "
        ).strip().lower()

        if value == "q":
            return None

        try:
            count = int(value)

            if count < 0:
                print_error(
                    "Please enter 0 or a positive number."
                )
                continue

            return count

        except ValueError:
            print_error(
                "Please enter a number or q to quit."
            )


def ask_confirmation(
    message: str,
) -> bool:
    """Ask the user for a yes/no confirmation."""

    while True:
        value = input(
            message
        ).strip().lower()

        if value in {"y", "yes"}:
            return True

        if value in {"n", "no"}:
            return False

        print_error(
            "Please enter y or n."
        )


def ask_quiz_template_name() -> str | None:
    """Ask the user for a name for a quiz template."""

    while True:
        value = input(
            f"{CYAN}"
            "Quiz template name"
            f"{RESET} "
            "(or q to cancel): "
        ).strip()

        if value.lower() == "q":
            return None

        if value:
            return value

        print_error(
            "Please enter a template name."
        )


def ask_saved_quiz() -> QuizTemplate | None:
    """Ask the user to select a saved quiz template."""

    templates = load_templates()

    if not templates:
        print()
        print_error(
            "No saved quiz templates found."
        )
        print()

        input(
            "Press Enter to return..."
        )

        return None

    templates = list(
        templates.values()
    )

    while True:
        print()
        print("Saved Quiz Templates")
        print()

        for index, template in enumerate(
            templates,
            start=1,
        ):
            print(
                f"  {index}. "
                f"{template.name} "
                f"({template.total_questions} questions)"
            )

        print()
        print(
            "Choose a template "
            f"(1-{len(templates)}, or q to return): "
        )

        value = input(
            "> "
        ).strip().lower()

        if value == "q":
            return None

        try:
            choice = int(value)
        except ValueError:
            print_error(
                f"Please choose 1-{len(templates)}, "
                "or q to return."
            )
            continue

        if 1 <= choice <= len(templates):
            return templates[choice - 1]

        print_error(
            f"Please choose 1-{len(templates)}, "
            "or q to return."
        )