from src.vocabulary.repository import (
    VocabularyRepository,
    DuplicateWordError,
    InvalidArticleError,
    InvalidLevelError,
)
from scripts.utils.formatter import (
    print_success,
    print_error,
    print_info,
    prompt,
    format_word_table,
    format_stats_table,
)


def handle_init(
    repo: VocabularyRepository,
    args,
) -> None:
    """Initialize the database."""

    repo.db.initialize_schema()

    print_success(
        "Database initialized."
    )


def handle_add(
    repo: VocabularyRepository,
    args,
) -> None:
    """Add a new word to the vocabulary."""

    german = prompt("German")
    english = prompt("English")
    article = prompt(
        "Article (der/die/das)"
    )
    plural = prompt(
        "Plural",
        required=False,
    )
    level = prompt(
        "Level",
        required=False,
    )

    try:
        word_id = repo.add_word(
            german=german,
            english=english,
            article=article,
            plural=plural,
            level=level,
        )

        print_success(
            f"Added '{german}' (id={word_id})"
        )

    except (
        InvalidArticleError,
        InvalidLevelError,
        DuplicateWordError,
    ) as e:
        print_error(str(e))


def handle_stats(
    repo: VocabularyRepository,
    args,
) -> None:
    """Display vocabulary statistics."""

    statistics = repo.get_statistics()

    print()
    print_info(
        "Vocabulary Statistics"
    )
    print()

    print(
        format_stats_table(statistics)
    )

    print()


def handle_search(
    repo: VocabularyRepository,
    args,
) -> None:
    """Search the vocabulary."""

    rows = repo.search_words(
        args.query
    )

    if not rows:
        print_info(
            f"No words found for '{args.query}'."
        )
        return

    print()
    print_info(
        f"Search results for '{args.query}'"
    )
    print()

    print(
        format_word_table(rows)
    )


def handle_list(
    repo: VocabularyRepository,
    args,
) -> None:
    """List vocabulary words."""

    rows = repo.list_words(
        article=args.article,
        level=args.level,
        sort_by=args.sort,
        reverse=args.reverse,
    )

    if not rows:
        print_info(
            "No words found."
        )
        return

    print(
        format_word_table(rows)
    )


def handle_delete(
    repo: VocabularyRepository,
    args,
) -> None:
    """Delete a vocabulary word."""

    if repo.delete_word(args.id):
        print_success(
            f"Deleted word id={args.id}"
        )
    else:
        print_error(
            f"No word found with id={args.id}"
        )


def edit_prompt(
    label: str,
    current_value: str | None,
) -> str:
    """Prompt for an edited value, keeping the current value if blank."""

    display_value = current_value or "-"

    value = input(
        f"{label} [{display_value}]: "
    ).strip()

    if value:
        return value

    return current_value or ""


def handle_edit(
    repo: VocabularyRepository,
    args,
) -> None:
    """Edit an existing vocabulary word."""

    word = repo.get_word(args.id)

    if word is None:
        print_error(
            f"No word found with id={args.id}"
        )
        return

    print_info(
        f"Editing word id={args.id}"
    )
    print()

    german = edit_prompt(
        "German",
        word["german"],
    )

    english = edit_prompt(
        "English",
        word["english"],
    )

    article = edit_prompt(
        "Article (der/die/das)",
        word["article"],
    )

    plural = edit_prompt(
        "Plural",
        word["plural"],
    )

    level = edit_prompt(
        "Level",
        word["level"],
    )

    try:
        updated = repo.update_word(
            word_id=args.id,
            german=german,
            english=english,
            article=article,
            plural=plural,
            level=level,
        )

        if updated:
            print_success(
                f"Updated '{german}' (id={args.id})"
            )

    except (
        InvalidArticleError,
        InvalidLevelError,
        DuplicateWordError,
    ) as e:
        print_error(str(e))

COMMAND_HANDLERS = {
    "init": handle_init,
    "add": handle_add,
    "stats": handle_stats,
    "search": handle_search,
    "list": handle_list,
    "delete": handle_delete,
    "edit": handle_edit,
}