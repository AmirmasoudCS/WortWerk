import argparse

from config.paths import DB_PATH, SCHEMA_PATH
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
    parser = argparse.ArgumentParser(prog="wortwerk", description="WortWerk CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("add", help="Add a new word to the vocabulary")
    subparsers.add_parser("list", help="List words in the vocabulary")
    subparsers.add_parser("delete", help="Delete a word from the vocabulary")

    return parser


def handle_add(repo: VocabularyRepository) -> None:
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


def handle_list(repo: VocabularyRepository) -> None:
    print_info("Not implemented yet.")


def handle_delete(repo: VocabularyRepository) -> None:
    print_info("Not implemented yet.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    db = Database(DB_PATH)
    db.initialize_schema(SCHEMA_PATH)
    repo = VocabularyRepository(db)

    commands = {
        "add": handle_add,
        "list": handle_list,
        "delete": handle_delete,
    }
    commands[args.command](repo)

    db.close()


if __name__ == "__main__":
    main()