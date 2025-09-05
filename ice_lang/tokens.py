from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # Single-char
    LEFT_PAREN = auto(); RIGHT_PAREN = auto()
    LEFT_BRACE = auto(); RIGHT_BRACE = auto()
    COMMA = auto(); DOT = auto(); MINUS = auto(); PLUS = auto()
    SEMICOLON = auto(); SLASH = auto(); STAR = auto(); PERCENT = auto()
    BANG = auto(); EQUAL = auto(); GREATER = auto(); LESS = auto()

    # One or two char
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENT = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords (Indonesian)
    TUGAS = auto()
    FUNGSI = auto()  # kompatibel
    JIKA = auto()
    JIKALAU = auto()
    KALAU = auto()
    SELAGI = auto()
    UNTUK = auto()
    DALAM = auto()
    RENTANG = auto()

    KEMBALIKAN = auto()
    TAMPILKAN = auto()
    CETAK = auto()  # kompatibel

    BENAR = auto()
    SALAH = auto()
    KOSONG = auto()
    DAN = auto()
    ATAU = auto()
    BUKAN = auto()

    BILANGAN = auto()
    DESIMAL = auto()
    TEKS = auto()
    BOOLEAN = auto()
    KELAS = auto()
    BARU = auto()
    INI = auto()

    EOF = auto()

KEYWORDS = {
    "tugas": TokenType.TUGAS,
    "fungsi": TokenType.FUNGSI,
    "jika": TokenType.JIKA,
    "jikalau": TokenType.JIKALAU,
    "kalau": TokenType.KALAU,
    "selagi": TokenType.SELAGI,
    "untuk": TokenType.UNTUK,
    "dalam": TokenType.DALAM,
    "rentang": TokenType.RENTANG,
    "kembalikan": TokenType.KEMBALIKAN,
    "tampilkan": TokenType.TAMPILKAN,
    "cetak": TokenType.CETAK,
    "benar": TokenType.BENAR,
    "salah": TokenType.SALAH,
    "kosong": TokenType.KOSONG,
    "dan": TokenType.DAN,
    "atau": TokenType.ATAU,
    "bukan": TokenType.BUKAN,
    "bilangan": TokenType.BILANGAN,
    "desimal": TokenType.DESIMAL,
    "teks": TokenType.TEKS,
    "boolean": TokenType.BOOLEAN,
    "kelas": TokenType.KELAS,
    "baru": TokenType.BARU,
    "ini": TokenType.INI,
}

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.lexeme!r}, {self.literal!r}, line={self.line}, col={self.column})"
