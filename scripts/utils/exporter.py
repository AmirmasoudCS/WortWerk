import csv

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from pathlib import Path

from config.paths import EXPORTS


EXPORT_COLUMNS = [
    "id",
    "german",
    "article",
    "english",
    "plural",
    "level",
]

EXPORT_HEADERS = [
    "ID",
    "German",
    "Article",
    "English",
    "Plural",
    "Level",
]

ARTICLE_COLORS = {
    "der": colors.HexColor("#3b82f6"),   # matches CLI BLUE
    "die": colors.HexColor("#ef4444"),   # matches CLI BRIGHT_RED
    "das": colors.HexColor("#22c55e"),   # matches CLI GREEN
}

ARTICLE_COLUMN_INDEX = EXPORT_COLUMNS.index("article")


def _rows_to_values(rows) -> list[list]:
    """Convert sqlite Row objects into plain value lists."""

    return [
        [row[col] if row[col] is not None else "" for col in EXPORT_COLUMNS]
        for row in rows
    ]


def _build_output_path(
    fmt: str,
    extension: str,
    sort_by: str,
    reverse: bool,
) -> Path:
    """Build the export path: exports/<format>/vocabulary_<sort>[_desc].<ext>"""

    format_dir = EXPORTS / fmt
    format_dir.mkdir(parents=True, exist_ok=True)

    suffix = "_desc" if reverse else ""
    filename = f"vocabulary_{sort_by}{suffix}.{extension}"

    return format_dir / filename


def export_csv(
    rows,
    sort_by: str = "id",
    reverse: bool = False,
) -> str:
    """Export vocabulary rows to a CSV file. Returns the output path."""

    output_path = _build_output_path("csv", "csv", sort_by, reverse)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(EXPORT_HEADERS)
        writer.writerows(_rows_to_values(rows))

    return str(output_path)


def export_excel(
    rows,
    sort_by: str = "id",
    reverse: bool = False,
) -> str:
    """Export vocabulary rows to an Excel file. Returns the output path."""

    output_path = _build_output_path("excel", "xlsx", sort_by, reverse)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Vocabulary"

    sheet.append(EXPORT_HEADERS)

    for value_row in _rows_to_values(rows):
        sheet.append(value_row)

    for column_cells in sheet.columns:
        max_length = max(
            len(str(cell.value)) for cell in column_cells
        )
        sheet.column_dimensions[column_cells[0].column_letter].width = (
            max_length + 2
        )

    workbook.save(output_path)

    return str(output_path)


def export_pdf(
    rows,
    sort_by: str = "id",
    reverse: bool = False,
) -> str:
    """Export vocabulary rows to a PDF file. Returns the output path."""

    output_path = _build_output_path("pdf", "pdf", sort_by, reverse)

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
    )

    table_data = [EXPORT_HEADERS] + _rows_to_values(rows)
    table = Table(table_data, repeatRows=1)

    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]

    for row_index, row in enumerate(table_data[1:], start=1):
        article = row[ARTICLE_COLUMN_INDEX].lower()
        color = ARTICLE_COLORS.get(article)

        if color is not None:
            style_commands.append(
                (
                    "TEXTCOLOR",
                    (ARTICLE_COLUMN_INDEX, row_index),
                    (ARTICLE_COLUMN_INDEX, row_index),
                    color,
                )
            )
            style_commands.append(
                (
                    "FONTNAME",
                    (ARTICLE_COLUMN_INDEX, row_index),
                    (ARTICLE_COLUMN_INDEX, row_index),
                    "Helvetica-Bold",
                )
            )

    table.setStyle(TableStyle(style_commands))

    document.build([table])

    return str(output_path)


EXPORT_HANDLERS = {
    "csv": export_csv,
    "excel": export_excel,
    "pdf": export_pdf,
}