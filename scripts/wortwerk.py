from config.paths import SQLITE_DATABASE
from src.database.database import Database
from src.vocabulary.repository import VocabularyRepository
from scripts.cli.parser import build_parser
from scripts.cli.handlers import COMMAND_HANDLERS
from scripts.utils.formatter import print_error


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    db = Database(SQLITE_DATABASE)
    repo = VocabularyRepository(db)

    try:
        if (
            args.command != "init"
            and not db.table_exists("vocabulary")
        ):
            print_error(
                "Database not initialized. "
                "Run 'wortwerk init' first."
            )
            return

        COMMAND_HANDLERS[args.command](repo, args)

    finally:
        db.close()


if __name__ == "__main__":
    main()