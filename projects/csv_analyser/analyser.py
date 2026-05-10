import csv
import logging
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    filepath: str
    row_count: int
    column_count: int
    column_names: list[str]
    most_nulls_column: str
    null_counts: dict[str, int]


def analyse_csv(filepath: str) -> AnalysisResult:
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"No file found at: {filepath}")
    if path.suffix != ".csv":
        raise ValueError(f"Expected a csv file, got: {path.suffix}")

    logger.info("Reading file: %s", filepath)

    null_counts: dict[str, int] = {}
    row_count = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file appears to be empty.")

        column_names = list(reader.fieldnames)
        null_counts = {col: 0 for col in column_names}

        for row in reader:
            row_count += 1
            for col in column_names:
                if row[col] is None or row[col].strip() == "":
                    null_counts[col] += 1

    most_null_column = max(null_counts, key=lambda col: null_counts[col])

    logger.info("Analysis complete. %d rows processed.", row_count)

    return AnalysisResult(
        filepath=filepath,
        row_count=row_count,
        column_count=len(column_names),
        column_names=column_names,
        most_nulls_column=most_null_column,
        null_counts=null_counts,
    )


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python analyser.py <path_to_csv>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        result = analyse_csv(filepath)
    except (FileNotFoundError, ValueError) as e:
        logger.error("Failed to analyse file: %s", e)
        sys.exit(1)

    print("\n--- Analysis Report ---")
    print(f"{'File':<14}:         {result.filepath}")
    print(f"{'Rows':<14}:        {result.row_count}")
    print(f"{'Columns':<14}:      {result.column_count}")
    print(f"{'Column names':<14}: {', '.join(result.column_names)}")
    print(
        f"{'Most nulls':<14}:   {result.most_nulls_column} ({result.null_counts[result.most_nulls_column]} nulls)"
    )
    print("\nNull counts per column:")
    for col, count in result.null_counts.items():
        print(f"  {col}: {count}")


if __name__ == "__main__":
    main()
