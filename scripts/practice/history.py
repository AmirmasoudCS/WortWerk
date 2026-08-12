import json
from datetime import datetime
from pathlib import Path

from config.paths import (
    HISTORY_DIR,
    SESSIONS_HISTORY,
    ARTICLE_HISTORY,
    ENGLISH_HISTORY,
    GERMAN_HISTORY,
    PLURAL_HISTORY,
)


def _load_json(path: Path):
    """Load JSON data from a file."""

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def _save_json(
    path: Path,
    data,
) -> None:
    """Save data to a JSON file."""

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


def initialize_history() -> None:
    """Create the history directory and files."""

    HISTORY_DIR.mkdir(
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


def load_history(path: Path):
    """Load a history file."""

    return _load_json(path)


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
) -> None:
    """Save the results of a practice or quiz session."""

    history = _load_json(
        SESSIONS_HISTORY
    )

    session_id = str(
        len(history) + 1
    )

    history[session_id] = {
        "date": datetime.now().isoformat(
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

    _save_json(
        SESSIONS_HISTORY,
        history,
    )


def record_word_result(
    word_id: int,
    mode: str,
    correct: bool,
    session_type: str,
) -> None:
    """Record the result of an individual vocabulary attempt."""

    history_paths = {
        "article": ARTICLE_HISTORY,
        "english": ENGLISH_HISTORY,
        "german": GERMAN_HISTORY,
        "plural": PLURAL_HISTORY,
    }

    if mode not in history_paths:
        raise ValueError(
            f"Invalid practice mode: {mode}"
        )

    path = history_paths[mode]

    history = _load_json(path)

    word_id = str(word_id)

    if word_id not in history:
        history[word_id] = {
            "attempts": 0,
            "correct": 0,
            "incorrect": 0,
        }

    history[word_id]["attempts"] += 1

    if correct:
        history[word_id]["correct"] += 1
    else:
        history[word_id]["incorrect"] += 1

    _save_json(
        path,
        history,
    )