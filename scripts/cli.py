import argparse

from config.paths import SQLITE_DATABASE
from src.database.database import Database
from src.vocabulary.repository import (
    VocabularyRepository,
    DuplicateWordError,
    InvalidArticleError,
)
from scripts.utils.formatter import (
    print_success,
    print_error,
    print_info,
    prompt,
    format_word_row,
    format_word_header,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wortwerk",
        description="WortWerk CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "init",
        help="Initialize the database",
    )

    subparsers.add_parser(
        "add",
        help="Add a new word to the vocabulary",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List words in the vocabulary",
    )

    list_parser.add_argument(
        "--article",
        choices=["der", "die", "das"],
        help="Filter by article",
    )

    list_parser.add_argument(
        "--level",
        help="Filter by level",
    )

    list_parser.add_argument(
        "--sort",
        choices=["id", "alphabetical", "level"],
        default="id",
        help="Sort words by id, alphabetical order, or level",
    )

    list_parser.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse the sort order",
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a word by id",
    )

    delete_parser.add_argument(
        "id",
        type=int,
        help="ID of the word to delete",
    )

    return parser


def handle_init(repo: VocabularyRepository, args) -> None:
    repo.db.initialize_schema()
    print_success("Database initialized.")


def handle_add(repo: VocabularyRepository, args) -> None:
    german = prompt("German")
    english = prompt("English")
    article = prompt("Article (der/die/das)")
    plural = prompt("Plural", required=False)
    level = prompt("Level", required=False)

    try:
        word_id = repo.add_word(
            german=german,
            english=english,
            article=article,
            plural=plural,
            level=level,
        )

        print_success(f"Added '{german}' (id={word_id})")

    except (InvalidArticleError, DuplicateWordError) as e:
        print_error(str(e))


def handle_list(repo: VocabularyRepository, args) -> None:
    rows = repo.list_words(
        article=args.article,
        level=args.level,
        sort_by=args.sort,
        reverse=args.reverse,
    )

    if not rows:
        print_info("No words found.")
        return

    print(format_word_header())

    for row in rows:
        print(format_word_row(row))


def handle_delete(repo: VocabularyRepository, args) -> None:
    if repo.delete_word(args.id):
        print_success(f"Deleted word id={args.id}")
    else:
        print_error(f"No word found with id={args.id}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    db = Database(SQLITE_DATABASE)
    repo = VocabularyRepository(db)

    if args.command != "init" and not db.table_exists("vocabulary"):
        print_error(
            "Database not initialized. Run 'wortwerk init' first."
        )
        db.close()
        return

    commands = {
        "init": handle_init,
        "add": handle_add,
        "list": handle_list,
        "delete": handle_delete,
    }

    commands[args.command](repo, args)

    db.close()


if __name__ == "__main__":
    main()
