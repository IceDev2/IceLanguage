from __future__ import annotations
from .tokens import Token, TokenType, KEYWORDS
from .errors import IceSyntaxError

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.col))
        return self.tokens

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _peek(self) -> str:
        if self._is_at_end(): return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        self.col += 1
        return True

    def _add(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line, self.col))

    def _scan_token(self):
        c = self._advance()

        # whitespace
        if c in ' \r\t':
            return
        if c == '\n':
            return

        # comments
        if c == '/' and self._peek() == '/':
            while self._peek() != '\n' and not self._is_at_end():
                self._advance()
            return
        if c == '/' and self._peek() == '*':
            self._advance()
            while not self._is_at_end() and not (self._peek() == '*' and self._peek_next() == '/'):
                self._advance()
            if not self._is_at_end():
                self._advance()  # '*'
                self._advance()  # '/'
            return

        # single char tokens
        if c == '(': self._add(TokenType.LEFT_PAREN); return
        if c == ')': self._add(TokenType.RIGHT_PAREN); return
        if c == '{': self._add(TokenType.LEFT_BRACE); return
        if c == '}': self._add(TokenType.RIGHT_BRACE); return
        if c == ',': self._add(TokenType.COMMA); return
        if c == '.': self._add(TokenType.DOT); return
        if c == '-': self._add(TokenType.MINUS); return
        if c == '+': self._add(TokenType.PLUS); return
        if c == ';': self._add(TokenType.SEMICOLON); return
        if c == '*': self._add(TokenType.STAR); return
        if c == '%': self._add(TokenType.PERCENT); return
        if c == '/': self._add(TokenType.SLASH); return
        if c == '!':
            if self._match('='): self._add(TokenType.BANG_EQUAL)
            else: self._add(TokenType.BANG)
            return
        if c == '=':
            if self._match('='): self._add(TokenType.EQUAL_EQUAL)
            else: self._add(TokenType.EQUAL)
            return
        if c == '>':
            if self._match('='): self._add(TokenType.GREATER_EQUAL)
            else: self._add(TokenType.GREATER)
            return
        if c == '<':
            if self._match('='): self._add(TokenType.LESS_EQUAL)
            else: self._add(TokenType.LESS)
            return

        # string
        if c == '"' or c == "'":
            quote = c
            value = []
            while not self._is_at_end() and self._peek() != quote:
                ch = self._advance()
                if ch == '\\':
                    nxt = self._advance()
                    if nxt == 'n': value.append('\n')
                    elif nxt == 't': value.append('\t')
                    elif nxt == '"': value.append('"')
                    elif nxt == "'": value.append("'")
                    else: value.append(nxt)
                else:
                    value.append(ch)
            if self._is_at_end():
                raise IceSyntaxError("String tidak tertutup", self.line, self.col)
            self._advance()  # closing quote
            self._add(TokenType.STRING, ''.join(value))
            return

        # number
        if c.isdigit():
            while self._peek().isdigit():
                self._advance()
            if self._peek() == '.' and self._peek_next().isdigit():
                self._advance()  # .
                while self._peek().isdigit():
                    self._advance()
            num_text = self.source[self.start:self.current]
            self._add(TokenType.NUMBER, float(num_text) if '.' in num_text else int(num_text))
            return

        # identifier / keyword
        if c.isalpha() or c == '_':
            while self._peek().isalnum() or self._peek() == '_':
                self._advance()
            text = self.source[self.start:self.current]
            lower = text.lower()
            ttype = KEYWORDS.get(lower, TokenType.IDENT)
            self.tokens.append(Token(ttype, text, None, self.line, self.col))
            return

        raise IceSyntaxError(f"Karakter tidak dikenal: {c}", self.line, self.col)
