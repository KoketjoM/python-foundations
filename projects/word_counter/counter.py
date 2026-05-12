import logging
import re
import time
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class WordCountResults:
    filepath: str
    total_words: int
    unique_words: int
    top_10: list[tuple[str, int]]


# GENERATOR
def readlines(filepath: Path) -> Generator[str, None, None]:
    with open(filepath, encoding="utf-8") as f:
        yield from f


# DECORATOR FUNCTION
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info("%s completed in %.4f seconds", func.__name__, end - start)
        return result

    return wrapper


@timer
def count_words(filepath: str) -> WordCountResults:
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"No file found at: {path}")
    if path.suffix != ".txt":
        raise ValueError(f"Expected txt file, got: {path.suffix}")

    logger.info("Reading file: %s", filepath)

    total_words = 0
    word_counts: dict[str, int] = {}

    for line in readlines(path):
        clean_line = re.sub(r"[^\w\s]", "", line).lower()
        words = clean_line.split()
        total_words += len(words)
        for word in words:
            word_counts[word] = (
                word_counts.get(word, 0) + 1
            )  # <---- Get increments found word, or initializes new word with 0

    top_10: list[tuple[str, int]] = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]

    return WordCountResults(
        filepath=filepath,
        total_words=total_words,
        unique_words=len(word_counts),
        top_10=top_10,
    )


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python counter.py myfile.txt")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        result = count_words(filepath)
    except (FileNotFoundError, ValueError) as e:
        logger.error("Failed to analyse file: %s", e)
        sys.exit(1)

    print("\n--- Analysis Report ---")
    print(f"{'File':<14}:         {result.filepath}")
    print(f"{'Word total':<14}:        {result.total_words}")
    print(f"{'Unique Words':<14}:        {result.unique_words}")
    print("\n--- Top 10 repeated words ---")
    for word, count in result.top_10:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
