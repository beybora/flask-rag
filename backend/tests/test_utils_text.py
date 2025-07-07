import pytest
from app.utils.text import split_text

def test_split_text_basic():
    text = "abcdefghij"
    chunks = split_text(text, chunk_size=4, chunk_overlap=2)
    assert chunks == ["abcd", "cdef", "efgh", "ghij"]

def test_split_text_empty():
    assert split_text("") == []

def test_split_text_shorter_than_chunk():
    assert split_text("abc", chunk_size=10) == ["abc"]

def test_split_text_exact_chunk():
    assert split_text("abcdefghij", chunk_size=10) == ["abcdefghij"] 