from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Token:
    """Text input tokens"""
    text: str
    start: int
    end: int
    ttype: Optional[str]

TokenSeq = List[Token]

def tokenize(text: str) -> TokenSeq:
    pass

def detokenize(tokens: TokenSeq) -> str:
    pass

def tokenize_with_offsets(text: str) -> TokenSeq:
    pass

