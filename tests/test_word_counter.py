import pytest

from projects.word_counter.counter import count_words


def test_happy_path():
    result = count_words("tests/data/sample.txt")
    assert result.total_words == 101


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        count_words("tests/data/nothing.txt")


def test_wrong_file_type():
    with pytest.raises(ValueError):
        count_words("tests/data/sample.csv")


def test_empty_file():
    with pytest.raises(ValueError):
        count_words("tests/data/sample_empty.txt")
