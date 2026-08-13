from datetime import datetime

from config.paths import SESSIONS_HISTORY
from scripts.practice.history import _load_json


def load_sessions() -> dict:
    """Load all saved practice and quiz sessions."""

    return _load_json(
        SESSIONS_HISTORY
    )


def get_recent_sessions(
    limit: int = 10,
) -> list[dict]:
    """Return the most recent sessions."""

    history = load_sessions()

    sessions = []

    for session_id, session in history.items():
        session_data = session.copy()

        session_data["id"] = session_id

        sessions.append(
            session_data
        )

    sessions.sort(
        key=lambda session: datetime.fromisoformat(
            session["date"]
        ),
        reverse=True,
    )

    return sessions[:limit]