from typing import List, Optional, Literal
from dataclasses import dataclass
from warnings import deprecated
import re

TokenMode = Literal["whitespace", "wordpunct"]

@dataclass(frozen=True)
class Token:
    """Text input tokens"""
    text: str
    start: int
    end: int
    ttype: Optional[str] = None

TokenSeq = List[Token]
_wordpunct_pattern = re.compile(
    r"""
    \d+(?:\.\d+)?           |           # numbers, e.g. 123 or 12.34
    [A-Za-z0-9_]+(?:'[A-Za-z0-9_]+)? |  # words with optional contraction/apostrophe
    [^\s\w]                             # any single non-space, non-word char (punctuation, emoji, symbols)
    """,
    re.VERBOSE,
)


def _classify_token(text: str) -> str:
    if text.isdigit() or re.fullmatch(r"\d+(?:\.\d+)?", text):
        return "number"
    if len(text) == 1 and not text.isalnum() and not text.isspace():
        return "punct"
    return "word"


def tokenize(text: str, mode: TokenMode = "wordpunct") -> List[Token]:
    """
    Public tokenizer function.
    CONTRACT:
      - Input must be normalized already (lowercased, spacing rules applied) if you rely on normalization.
      - Returns a list of Token objects with offsets relative to the given `text`.
    Modes:
      - "whitespace": minimal, preserves punctuation attached to tokens
      - "wordpunct": splits words from punctuation and gives simple token types
    """
    if mode == "whitespace":
        return tokenize_whitespace(text)
    if mode == "wordpunct":
        return tokenize_wordpunct(text)
    raise ValueError(f"unknown tokenization mode: {mode!r}")

def detokenize(tokens: TokenSeq) -> str:
    pass

def tokenize_whitespace(text: str) -> List[Token]:
    """
    Simple tokenizer: finds runs of non-whitespace characters and returns them as tokens with offsets.
    - Works on already-normalized text (caller should lowercase/collapse-space etc.).
    - Keeps punctuation attached to tokens (e.g., "hello!" -> token "hello!").
    """
    if not text:
        return []

    tokens: List[Token] = []
    for m in re.finditer(r"\S+", text):
        tok = m.group(0)
        tokens.append(Token(text=tok, start=m.start(), end=m.end(), type=None))
    return tokens

def tokenize_wordpunct(text: str) -> List[Token]:
    """
    Regex tokenizer that separates words and punctuation.
    Returns tokens with offsets and a best-effort `type` annotation.
    """
    if not text:
        return []

    tokens: List[Token] = []
    for m in _wordpunct_pattern.finditer(text):
        tok = m.group(0)
        typ = _classify_token(tok)
        tokens.append(Token(text=tok, start=m.start(), end=m.end(), type=typ))
    return tokens

if __name__ == '__main__':
    examples = [
        "hello world",
        "what?",
        "😊",
        "  lots   of   spaces  ",
        "",
        "email@example.com",
    ]

    for ex in examples:
        print("INPUT:", repr(ex))
        for mode in ("whitespace", "wordpunct"):
            toks = tokenize(ex, mode=mode)
            print(f"  mode={mode} -> {len(toks)} tokens")
            for t in toks:
                print(f"    [{t.start}:{t.end}] {t.text!r} type={t.type}")
        print()