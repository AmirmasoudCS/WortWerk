import json
from pathlib import Path

from config.paths import QUIZ_TEMPLATES

from scripts.quiz.templates import QuizTemplate


def _load_templates() -> dict:
    """Load saved quiz templates from disk."""

    if not QUIZ_TEMPLATES.exists():
        return {}

    with QUIZ_TEMPLATES.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def _save_templates(
    templates: dict,
) -> None:
    """Save quiz templates to disk."""

    QUIZ_TEMPLATES.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with QUIZ_TEMPLATES.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            templates,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_template(
    template: QuizTemplate,
) -> None:
    """Save a quiz template."""

    template.validate()

    templates = _load_templates()

    templates[template.name] = {
        "question_counts": (
            template.question_counts
        ),
    }

    _save_templates(
        templates
    )


def load_template(
    name: str,
) -> QuizTemplate | None:
    """Load a saved quiz template by name."""

    templates = _load_templates()

    if name not in templates:
        return None

    data = templates[name]

    template = QuizTemplate(
        name=name,
        question_counts=data["question_counts"],
    )

    template.validate()

    return template


def get_saved_templates() -> dict[str, QuizTemplate]:
    """Return all saved quiz templates."""

    templates = _load_templates()

    saved_templates = {}

    for name, data in templates.items():
        template = QuizTemplate(
            name=name,
            question_counts=data["question_counts"],
        )

        template.validate()

        saved_templates[name] = template

    return saved_templates


def delete_template(
    name: str,
) -> bool:
    """Delete a saved quiz template.

    Returns True if the template existed and
    was deleted, otherwise False.
    """

    templates = _load_templates()

    if name not in templates:
        return False

    del templates[name]

    _save_templates(
        templates
    )

    return True