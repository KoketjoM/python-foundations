import pytest

from projects.csv_analyser.analyser import analyse_csv


def test_happy_path():
    result = analyse_csv("tests/data/sample.csv")
    assert result.row_count == 3
    assert result.column_count == 3
    assert result.most_nulls_column == "age"


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyse_csv("tests/data/nothing.csv")


def test_wrong_file_type():
    with pytest.raises(ValueError):
        analyse_csv("tests/data/sample.txt")


def test_file_empty():
    with pytest.raises(ValueError):
        analyse_csv("tests/data/sample_empty.csv")
