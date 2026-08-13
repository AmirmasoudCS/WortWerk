from dataclasses import dataclass

from config.constants import (
    QUIZ_TEMPLATE_QUESTION_COUNTS,
    VALID_PRACTICE_MODES,
)


@dataclass
class QuizTemplate:
    """Define the structure of a quiz template."""

    name: str
    question_counts: dict[str, int]
    levels: list[str] | None = None

    @property
    def total_questions(self) -> int:
        """Return the total number of questions."""

        return sum(
            self.question_counts.values()
        )

    def validate(self) -> None:
        """Validate the quiz template."""

        if not self.name.strip():
            raise ValueError(
                "Quiz template name cannot be empty."
            )

        for mode, count in self.question_counts.items():
            if mode not in VALID_PRACTICE_MODES:
                raise ValueError(
                    f"Invalid quiz mode: {mode}"
                )

            if not isinstance(count, int):
                raise ValueError(
                    f"Question count must be an integer: "
                    f"{mode}={count}"
                )

            if count < 0:
                raise ValueError(
                    f"Question count cannot be negative: "
                    f"{mode}={count}"
                )

        if self.total_questions <= 0:
            raise ValueError(
                "A quiz must contain at least one question."
            )


def _create_default_template(
    name: str,
    template_key: str,
) -> QuizTemplate:
    """Create a default quiz template."""

    return QuizTemplate(
        name=name,
        question_counts=(
            QUIZ_TEMPLATE_QUESTION_COUNTS[
                template_key
            ].copy()
        ),
    )


SHORT_QUIZ = _create_default_template(
    name="Short",
    template_key="short",
)

MEDIUM_QUIZ = _create_default_template(
    name="Medium",
    template_key="medium",
)

LONG_QUIZ = _create_default_template(
    name="Long",
    template_key="long",
)


DEFAULT_QUIZ_TEMPLATES = {
    "short": SHORT_QUIZ,
    "medium": MEDIUM_QUIZ,
    "long": LONG_QUIZ,
}