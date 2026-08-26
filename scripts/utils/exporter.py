import csv

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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


def _rows_to_values(rows) -> list[list]:
    """Convert sqlite Row objects into plain value lists."""

    return [
        [row[col] if row[col] is not None else "" for col in EXPORT_COLUMNS]
        for row in rows
    ]


def _ensure_exports_dir() -> None:
    """Create the exports directory if it doesn't exist."""

    EXPORTS.mkdir(parents=True, exist_ok=True)


def export_csv(rows, filename: str = "vocabulary.csv") -> str:
    """Export vocabulary rows to a CSV file. Returns the output path."""

    _ensure_exports_dir()
    output_path = EXPORTS / filename

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(EXPORT_HEADERS)
        writer.writerows(_rows_to_values(rows))

    return str(output_path)


def export_excel(rows, filename: str = "vocabulary.xlsx") -> str:
    """Export vocabulary rows to an Excel file. Returns the output path."""

    _ensure_exports_dir()
    output_path = EXPORTS / filename

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


def export_pdf(rows, filename: str = "vocabulary.pdf") -> str:
    """Export vocabulary rows to a PDF file. Returns the output path."""

    _ensure_exports_dir()
    output_path = EXPORTS / filename

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
    )

    table_data = [EXPORT_HEADERS] + _rows_to_values(rows)
    table = Table(table_data, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    document.build([table])

    return str(output_path)


EXPORT_HANDLERS = {
    "csv": export_csv,
    "excel": export_excel,
    "pdf": export_pdf,
}