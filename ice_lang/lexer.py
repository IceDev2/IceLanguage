
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

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        ch = self.source[self.current]
        self.current += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _peek(self, k=0):
        idx = self.current + k
        if idx >= len(self.source): return '\0'
        return self.source[idx]

    def _match(self, expected):
        if self._is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1; self.col += 1
        return True

    def _add(self, t: TokenType, literal=None):
        txt = self.source[self.start:self.current]
        self.tokens.append(Token(t, txt, literal, self.line, self.col))

    def _scan_token(self):
        c = self._advance()
        # whitespace
        if c in ' \r\t': return
        if c == '\n': return
        # comments
        if c == '/' and self._peek() == '/':
            while self._peek() not in ('\n', '\0'): self._advance()
            return

        if c == '(': self._add(TokenType.LEFT_PAREN); return
        if c == ')': self._add(TokenType.RIGHT_PAREN); return
        if c == '{': self._add(TokenType.LEFT_BRACE); return
        if c == '}': self._add(TokenType.RIGHT_BRACE); return
        if c == ',': self._add(TokenType.COMMA); return
        if c == '.': self._add(TokenType.DOT); return
        if c == ':': self._add(TokenType.COLON); return
        if c == ';': self._add(TokenType.SEMICOLON); return
        if c == '+': self._add(TokenType.PLUS); return
        if c == '-': self._add(TokenType.MINUS); return
        if c == '*': self._add(TokenType.STAR); return
        if c == '%': self._add(TokenType.PERCENT); return
        if c == '!':
            if self._match('='):
                self._add(TokenType.BANG_EQUAL)
            else:
                self._add(TokenType.BANG)
            return
        if c == '=':
            if self._match('='):
                self._add(TokenType.EQUAL_EQUAL); return
            else:
                self._add(TokenType.EQUAL); return
        if c == '>':
            if self._match('='): self._add(TokenType.GREATER_EQUAL)
            else: self._add(TokenType.GREATER)
            return
        if c == '<':
            if self._match('='): self._add(TokenType.LESS_EQUAL)
            else: self._add(TokenType.LESS)
            return

        if c == '"':
            # string
            start_line, start_col = self.line, self.col
            s = []
            while not self._is_at_end() and self._peek() != '"':
                ch = self._advance()
                if ch == '\\':
                    esc = self._advance()
                    mapping = {'n':'\n','t':'\t','r':'\r','"':'"','\\':'\\'}
                    s.append(mapping.get(esc, esc))
                else:
                    s.append(ch)
            if self._is_at_end():
                raise IceSyntaxError("String tidak tertutup", start_line, start_col)
            self._advance()  # closing "
            self._add(TokenType.STRING, ''.join(s))
            return

        if c.isdigit():
            num = [c]
            is_float = False
            while self._peek().isdigit():
                num.append(self._advance())
            if self._peek()=='.' and self._peek(1).isdigit():
                is_float = True
                num.append(self._advance())
                while self._peek().isdigit():
                    num.append(self._advance())
            val = float(''.join(num)) if is_float else int(''.join(num))
            self._add(TokenType.NUMBER, val)
            return

        if c.isalpha() or c == '_':
            ident = [c]
            while self._peek().isalnum() or self._peek() == '_':
                ident.append(self._advance())
            word = ''.join(ident)
            ttype = KEYWORDS.get(word, TokenType.IDENT)
            self.tokens.append(Token(ttype, word, None, self.line, self.col))
            return

        raise IceSyntaxError(f"Karakter tidak dikenal: {c}", self.line, self.col)
