from dataclasses import dataclass

from config.constants import (
    QUIZ_TEMPLATE_QUESTION_COUNTS,
    VALID_PRACTICE_MODES,
)


@dataclass
class QuizTemplate:
    """Define the structure of a quiz."""

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

        for mode, count in self.question_counts.items():
            if mode not in VALID_PRACTICE_MODES:
                raise ValueError(
                    f"Invalid quiz mode: {mode}"
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


SHORT_QUIZ = QuizTemplate(
    name="Short",
    question_counts=QUIZ_TEMPLATE_QUESTION_COUNTS["short"],
)


MEDIUM_QUIZ = QuizTemplate(
    name="Medium",
    question_counts=QUIZ_TEMPLATE_QUESTION_COUNTS["medium"],
)


LONG_QUIZ = QuizTemplate(
    name="Long",
    question_counts=QUIZ_TEMPLATE_QUESTION_COUNTS["long"],
)


DEFAULT_QUIZ_TEMPLATES = {
    "short": SHORT_QUIZ,
    "medium": MEDIUM_QUIZ,
    "long": LONG_QUIZ,
}