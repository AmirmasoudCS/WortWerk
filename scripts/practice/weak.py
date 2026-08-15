import random

from scripts.practice.history import load_word_history

from scripts.utils.formatter import print_info


def _get_word_stats(
    word_id,
    history: dict,
) -> tuple[int, int]:
    """Return combined (attempts, incorrect) for a word across practice and quiz history."""

    record = history.get(
        str(word_id),
        {},
    )

    attempts = 0
    incorrect = 0

    for session_type in (
        "practice",
        "quiz",
    ):
        stats = record.get(
            session_type,
            {},
        )

        attempts += stats.get(
            "attempts",
            0,
        )
        incorrect += stats.get(
            "incorrect",
            0,
        )

    return attempts, incorrect


def _weighted_sample_without_replacement(
    rows: list,
    weights: list[float],
    count: int,
) -> list:
    """Select `count` rows from `rows`, weighted by `weights`, without replacement."""

    pool = list(rows)
    pool_weights = list(weights)
    selected = []

    while pool and len(selected) < count:
        chosen = random.choices(
            pool,
            weights=pool_weights,
            k=1,
        )[0]

        index = pool.index(chosen)

        selected.append(pool.pop(index))
        pool_weights.pop(index)

    return selected


def get_weak_words(
    rows: list,
    mode: str,
    word_count: int,
    min_attempts: int = 3,
    max_accuracy: float = 0.8,
) -> list:
    """Return a weighted selection of weak words from the given pool."""

    history = load_word_history(mode)

    weak_rows = []
    weights = []

    for row in rows:
        attempts, incorrect = _get_word_stats(
            row["id"],
            history,
        )

        if attempts < min_attempts:
            continue

        accuracy = (
            attempts - incorrect
        ) / attempts

        if accuracy >= max_accuracy:
            continue

        error_rate = incorrect / attempts

        weak_rows.append(row)
        weights.append(error_rate)

    if not weak_rows:
        print_info(
            "No weak words found yet. Starting a normal practice session instead."
        )
        return rows[:word_count]

    selected = _weighted_sample_without_replacement(
        weak_rows,
        weights,
        word_count,
    )

    if len(selected) < word_count:
        print_info(
            f"Only {len(selected)} weak word(s) found. "
            "Filling the rest with a random selection."
        )

        remaining_pool = [
            row
            for row in rows
            if row not in selected
        ]

        random.shuffle(remaining_pool)

        needed = word_count - len(selected)

        selected.extend(
            remaining_pool[:needed]
        )

    return selected

def list_weak_words(
    rows: list,
    mode: str,
    min_attempts: int = 3,
    max_accuracy: float = 0.8,
) -> list[dict]:
    """Return weak words with their stats, sorted from lowest to highest accuracy."""

    history = load_word_history(mode)

    weak_words = []

    for row in rows:
        attempts, incorrect = _get_word_stats(
            row["id"],
            history,
        )

        if attempts < min_attempts:
            continue

        accuracy = (
            attempts - incorrect
        ) / attempts

        if accuracy >= max_accuracy:
            continue

        weak_words.append(
            {
                "row": row,
                "attempts": attempts,
                "incorrect": incorrect,
                "accuracy": accuracy,
            }
        )

    weak_words.sort(
        key=lambda item: item["accuracy"]
    )

    return weak_words