
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # single-char
    LEFT_PAREN = auto(); RIGHT_PAREN = auto()
    LEFT_BRACE = auto(); RIGHT_BRACE = auto()
    COMMA = auto(); DOT = auto(); COLON = auto(); MINUS = auto(); PLUS = auto()
    SEMICOLON = auto(); SLASH = auto(); STAR = auto(); PERCENT = auto()
    EQUAL = auto(); BANG = auto()
    GREATER = auto(); GREATER_EQUAL = auto()
    LESS = auto(); LESS_EQUAL = auto()
    EQUAL_EQUAL = auto(); BANG_EQUAL = auto()

    IDENT = auto(); STRING = auto(); NUMBER = auto()

    # keywords
    JIKA = auto(); KALAU = auto(); JIKALAU = auto()
    SELAGI = auto(); UNTUK = auto(); DALAM = auto()
    KEMBALIKAN = auto()
    BUKAN = auto(); DAN = auto(); ATAU = auto()
    BENAR = auto(); SALAH = auto(); KOSONG = auto()
    TUGAS = auto(); FUNGSI = auto()
    BILANGAN = auto(); DESIMAL = auto(); TEKS = auto(); BOOLEAN = auto()
    KELAS = auto(); BARU = auto(); INI = auto(); SUPER = auto()
    PROPERTI = auto(); GET = auto(); SET = auto()

    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
    column: int
    def __repr__(self) -> str:
        return f"{self.type.name}({self.lexeme!r}, {self.literal!r})@{self.line}:{self.column}"

KEYWORDS = {
    "jika": TokenType.JIKA,
    "kalau": TokenType.KALAU,
    "jikalau": TokenType.JIKALAU,
    "selagi": TokenType.SELAGI,
    "untuk": TokenType.UNTUK,
    "dalam": TokenType.DALAM,
    "kembalikan": TokenType.KEMBALIKAN,
    "bukan": TokenType.BUKAN,
    "dan": TokenType.DAN,
    "atau": TokenType.ATAU,
    "benar": TokenType.BENAR,
    "salah": TokenType.SALAH,
    "kosong": TokenType.KOSONG,
    "tugas": TokenType.TUGAS,
    "fungsi": TokenType.FUNGSI,
    "bilangan": TokenType.BILANGAN,
    "desimal": TokenType.DESIMAL,
    "teks": TokenType.TEKS,
    "boolean": TokenType.BOOLEAN,
    "kelas": TokenType.KELAS,
    "baru": TokenType.BARU,
    "ini": TokenType.INI,
    "super": TokenType.SUPER,
    "properti": TokenType.PROPERTI,
    "get": TokenType.GET,
    "set": TokenType.SET,
}
