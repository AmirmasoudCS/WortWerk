from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from scripts.practice.history import load_sessions

from config.constants import VALID_PRACTICE_MODES, MIN_SESSIONS, ROLLING_WINDOW

from config.colors import CYAN, YELLOW, RESET, MODE_COLORS

from config.paths import PROGRESS_DIR

def _grouped_sessions() -> dict:
    """Group completed sessions by session_type and mode, in chronological order."""

    sessions = load_sessions()

    grouped = defaultdict(lambda: defaultdict(list))

    ordered = sorted(
        sessions.values(),
        key=lambda s: s.get("date", ""),
    )

    for session in ordered:
        if not session.get("completed", False):
            continue

        session_type = session.get("session_type")
        mode = session.get("mode")

        if session_type is None or mode is None:
            continue

        grouped[session_type][mode].append(
            {
                "accuracy": session.get("accuracy", 0.0),
                "date": session.get("date", ""),
            }
        )

    return grouped


def _rolling_average(values: list[float], window: int) -> list[float]:
    """Compute a simple rolling average over a list of values."""

    averages = []

    for i in range(len(values)):
        start = max(0, i - window + 1)
        chunk = values[start:i + 1]
        averages.append(sum(chunk) / len(chunk))

    return averages


def build_progress_summary() -> dict:
    """Build a text-ready summary of accuracy progress per session type and mode."""

    grouped = _grouped_sessions()

    summary = {}

    for session_type, modes in grouped.items():
        summary[session_type] = {}

        for mode, entries in modes.items():
            accuracies = [e["accuracy"] for e in entries]

            if len(accuracies) < MIN_SESSIONS:
                summary[session_type][mode] = None
                continue

            half = len(accuracies) // 2
            earlier = accuracies[:half] if half > 0 else accuracies[:1]
            recent = accuracies[half:]

            earlier_avg = sum(earlier) / len(earlier)
            recent_avg = sum(recent) / len(recent)

            summary[session_type][mode] = {
                "earlier_avg": earlier_avg,
                "recent_avg": recent_avg,
                "change": recent_avg - earlier_avg,
                "sessions": len(accuracies),
            }

    return summary


def print_progress_summary(summary: dict) -> None:
    """Print the progress summary to the terminal."""

    print()
    print(f"{CYAN}Progress Over Time{RESET}")
    print()

    if not summary:
        print(f"{YELLOW}[INFO]{RESET} No completed sessions found yet.")
        return

    for session_type, modes in summary.items():
        print(f"{CYAN}{session_type.capitalize()}{RESET}")

        has_data = False

        for mode, stats in modes.items():
            if stats is None:
                continue

            has_data = True

            sign = "+" if stats["change"] >= 0 else ""

            print(
                f"  {mode:<10} "
                f"{stats['earlier_avg']:.1f}% → {stats['recent_avg']:.1f}% "
                f"({sign}{stats['change']:.1f}%) "
                f"[{stats['sessions']} sessions]"
            )

        if not has_data:
            print(f"  {YELLOW}Not enough sessions yet.{RESET}")

        print()


def build_progress_chart(save: bool = False) -> Path | None:
    """Build the progress chart figure, optionally saving it to disk."""

    grouped = _grouped_sessions()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    titles = ["Practice", "Quiz", "Combined"]

    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlabel("Session #")
        ax.set_ylabel("Accuracy (%)")
        ax.set_ylim(0, 100)

    def plot_on(ax, session_type):
        modes = grouped.get(session_type, {})

        for mode in VALID_PRACTICE_MODES:
            entries = modes.get(mode)

            if not entries or len(entries) < MIN_SESSIONS:
                continue

            accuracies = [e["accuracy"] for e in entries]
            x = list(range(1, len(accuracies) + 1))

            color = MODE_COLORS.get(mode, "#333333")

            ax.scatter(x, accuracies, color=color, alpha=0.4, s=20)
            ax.plot(
                x,
                _rolling_average(accuracies, ROLLING_WINDOW),
                color=color,
                label=mode,
                linewidth=2,
            )

        if modes:
            ax.legend(fontsize=8)

    plot_on(axes[0], "practice")
    plot_on(axes[1], "quiz")

    for session_type in ("practice", "quiz"):
        plot_on(axes[2], session_type)

    fig.tight_layout()

    if not save:
        plt.show()
        return None

    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = PROGRESS_DIR / f"progress_{timestamp}.png"

    fig.savefig(filepath, dpi=150)
    plt.close(fig)

    return filepath