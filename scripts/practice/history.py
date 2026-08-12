import json
from datetime import datetime
from pathlib import Path

from config.paths import (
    HISTORY,
    SESSIONS_HISTORY,
    ARTICLE_HISTORY,
    ENGLISH_HISTORY,
    GERMAN_HISTORY,
    PLURAL_HISTORY,
)

from config.constants import (
    VALID_SESSION_TYPES,
    VALID_PRACTICE_MODES,
)


HISTORY_PATHS = {
    "article": ARTICLE_HISTORY,
    "english": ENGLISH_HISTORY,
    "german": GERMAN_HISTORY,
    "plural": PLURAL_HISTORY,
}


def initialize_history() -> None:
    """Create the history directory and history files."""

    HISTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    history_files = [
        SESSIONS_HISTORY,
        ARTICLE_HISTORY,
        ENGLISH_HISTORY,
        GERMAN_HISTORY,
        PLURAL_HISTORY,
    ]

    for path in history_files:
        if not path.exists():
            _save_json(
                path,
                {},
            )


def _load_json(path: Path) -> dict:
    """Load JSON data from a history file."""

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def _save_json(
    path: Path,
    data: dict,
) -> None:
    """Save JSON data to a history file."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def _migrate_word_history(
    word_history: dict,
) -> dict:
    """Convert legacy word history to the current format."""

    if "attempts" not in word_history:
        return word_history

    return {
        "practice": {
            "attempts": word_history["attempts"],
            "correct": word_history["correct"],
            "incorrect": word_history["incorrect"],
        }
    }


def _create_word_result() -> dict:
    """Create an empty word-result record."""

    return {
        "attempts": 0,
        "correct": 0,
        "incorrect": 0,
    }


def save_session(
    session_type: str,
    mode: str,
    levels: list[str] | None,
    questions: int,
    correct: int,
    incorrect: int,
    accuracy: float,
    elapsed_time: float,
    completed: bool = True,
    question_counts: dict[str, int] | None = None,
) -> None:
    """Save the results of a practice or quiz session."""

    if session_type not in VALID_SESSION_TYPES:
        raise ValueError(
            f"Invalid session type: {session_type}"
        )

    if (
        session_type == "practice"
        and mode not in VALID_PRACTICE_MODES
    ):
        raise ValueError(
            f"Invalid practice mode: {mode}"
        )

    history = _load_json(
        SESSIONS_HISTORY
    )

    now = datetime.now()

    session_id = now.strftime(
        "%Y%m%d%H%M%S%f"
    )

    session = {
        "date": now.isoformat(
            timespec="seconds"
        ),
        "session_type": session_type,
        "mode": mode,
        "levels": levels,
        "questions": questions,
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": accuracy,
        "time": elapsed_time,
        "completed": completed,
    }

    if question_counts is not None:
        session["question_counts"] = (
            question_counts
        )

    history[session_id] = session

    _save_json(
        SESSIONS_HISTORY,
        history,
    )


def record_word_result(
    word_id: int,
    mode: str,
    session_type: str,
    correct: bool,
) -> None:
    """Record an individual vocabulary attempt."""

    if mode not in VALID_PRACTICE_MODES:
        raise ValueError(
            f"Invalid practice mode: {mode}"
        )

    if session_type not in VALID_SESSION_TYPES:
        raise ValueError(
            f"Invalid session type: {session_type}"
        )

    path = HISTORY_PATHS[mode]

    history = _load_json(path)

    word_id = str(word_id)

    if word_id not in history:
        history[word_id] = {}

    history[word_id] = _migrate_word_history(
        history[word_id]
    )

    if session_type not in history[word_id]:
        history[word_id][session_type] = (
            _create_word_result()
        )

    result = history[word_id][session_type]

    result["attempts"] += 1

    if correct:
        result["correct"] += 1
    else:
        result["incorrect"] += 1

    _save_json(
        path,
        history,
    )