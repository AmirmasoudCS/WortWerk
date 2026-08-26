import argparse

from config.constants import (
    VALID_ARTICLES,
    VALID_LEVELS,
    VALID_EXPORT_FORMATS,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the WortWerk CLI argument parser."""

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

    subparsers.add_parser(
        "stats",
        help="Show vocabulary statistics",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search vocabulary",
    )

    search_parser.add_argument(
        "query",
        help="Search for a word or translation",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List words in the vocabulary",
    )

    list_parser.add_argument(
        "--article",
        "-art",
        choices=sorted(VALID_ARTICLES),
        help="Filter by article",
    )

    list_parser.add_argument(
        "--level",
        "-lev",
        choices=sorted(VALID_LEVELS),
        help="Filter by level",
    )

    list_parser.add_argument(
        "--sort",
        "-s",
        choices=[
            "id",
            "alphabetical",
            "level",
        ],
        default="id",
        help="Sort words by id, alphabetical order, or level",
    )

    list_parser.add_argument(
        "--reverse",
        "-rev",
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

    edit_parser = subparsers.add_parser(
        "edit",
        help="Edit a word by id",
    )

    edit_parser.add_argument(
        "id",
        type=int,
        help="ID of the word to edit",
    )

    export_parser = subparsers.add_parser(
        "export",
        help="Export vocabulary to a file",
    )

    export_parser.add_argument(
        "--format",
        "-f",
        choices=sorted(VALID_EXPORT_FORMATS),
        default="all",
        help="Export format: csv, excel, pdf, or all",
    )

    return parser