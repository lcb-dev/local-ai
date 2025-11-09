import pytest
from typing import List, Tuple

from local_ai.preprocessing.tokenizer import tokenize, Token

def token_texts(tokens: List[Token]) -> List[str]:
    return [t.text for t in tokens]

def token_tuples(tokens: List[Token]) -> List[Tuple[str, int, int, object]]:
    return [(t.text, t.start, t.end, t.type) for t in tokens]


def check_offsets(tokens: List[Token], text: str):
    for t in tokens:
        assert 0 <= t.start < t.end <= len(text), f"bad range for token {t}"
        assert text[t.start:t.end] == t.text, f"token text mismatch {t}"
    for a, b in zip(tokens, tokens[1:]):
        assert a.end <= b.start, f"tokens overlap or unordered: {a} / {b}"


def test_tokenize_whitespace_basic_and_empty():
    text = "hello world"
    toks = tokenize(text, mode="whitespace")
    assert token_texts(toks) == ["hello", "world"]
    check_offsets(toks, text)

    toks_empty = tokenize("", mode="whitespace")
    assert toks_empty == []


def test_tokenize_wordpunct_contractions_and_question():
    text = "what's up?"
    toks = tokenize(text, mode="wordpunct")
    assert token_texts(toks) == ["what's", "up", "?"], token_texts(toks)
    check_offsets(toks, text)


def test_tokenize_wordpunct_emoji_and_spaces():
    text = "hey 😊 what's going on!!!"
    toks = tokenize(text, mode="wordpunct")
    texts = token_texts(toks)
    assert texts[0] == "hey"
    assert any("😊" in t for t in texts)
    assert "!" in texts or "!!!" in texts
    check_offsets(toks, text)


def test_offsets_non_overlapping_and_correct_substrings():
    text = "  lots   of   spaces  "
    toks = tokenize(text, mode="whitespace")
    assert token_texts(toks) == ["lots", "of", "spaces"]
    check_offsets(toks, text)
