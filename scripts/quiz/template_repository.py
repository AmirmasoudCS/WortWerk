import json

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


def _normalize_name(
    name: str,
) -> str:
    """Normalize a quiz template name."""

    return " ".join(
        name.strip().split()
    )


def template_exists(
    name: str,
) -> bool:
    """Return whether a saved template exists."""

    normalized_name = _normalize_name(
        name
    )

    templates = _load_templates()

    return normalized_name in templates


def save_template(
    template: QuizTemplate,
) -> None:
    """Save a quiz template."""

    template.validate()

    template.name = _normalize_name(
        template.name
    )

    if not template.name:
        raise ValueError(
            "Quiz template name cannot be empty."
        )

    templates = _load_templates()

    if template.name in templates:
        raise ValueError(
            f"A quiz template named "
            f"'{template.name}' already exists."
        )

    templates[template.name] = (
        template.question_counts
    )

    _save_templates(
        templates
    )


def load_templates() -> dict[str, QuizTemplate]:
    """Load all saved quiz templates."""

    data = _load_templates()

    templates = {}

    for name, question_counts in data.items():
        template = QuizTemplate(
            name=name,
            question_counts=question_counts,
        )

        template.validate()

        templates[name] = template

    return templates


def load_template(
    name: str,
) -> QuizTemplate | None:
    """Load a saved quiz template by name."""

    normalized_name = _normalize_name(
        name
    )

    templates = load_templates()

    return templates.get(
        normalized_name
    )


def delete_template(
    name: str,
) -> bool:
    """Delete a saved quiz template.

    Return True when a template was deleted.
    """

    normalized_name = _normalize_name(
        name
    )

    templates = _load_templates()

    if normalized_name not in templates:
        return False

    del templates[
        normalized_name
    ]

    _save_templates(
        templates
    )

    return True