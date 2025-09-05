from __future__ import annotations
from .tokens import Token, TokenType
from .errors import IceSyntaxError
from .ast import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self._is_at_end():
            statements.append(self.declaration())
        return statements

    # Utilities
    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _check(self, t: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == t

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, t: TokenType, msg: str):
        if self._check(t):
            return self._advance()
        token = self._peek()
        raise IceSyntaxError(msg, token.line, token.column)

    # Grammar
    def declaration(self) -> Stmt:
        if self._match(TokenType.KELAS):
            return self.class_declaration()
        if self._match(TokenType.TUGAS, TokenType.FUNGSI):
            return self.function_declaration()
        if self._match(TokenType.BILANGAN, TokenType.DESIMAL, TokenType.TEKS, TokenType.BOOLEAN):
            name = self._consume(TokenType.IDENT, "Nama variabel diharapkan.")
            init = None
            if self._match(TokenType.EQUAL):
                init = self.expression()
            self._consume(TokenType.SEMICOLON, "Titik koma ';' diharapkan setelah deklarasi variabel.")
            return VarDecl(name.lexeme, init)
        return self.statement()

    def function_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENT, "Nama fungsi diharapkan.")
        self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah nama fungsi.")
        params = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                p = self._consume(TokenType.IDENT, "Nama parameter diharapkan.")
                params.append(p.lexeme)
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah parameter.")
        block = self.block()
        return FunctionDecl(name.lexeme, params, block)

    def class_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENT, "Nama kelas diharapkan.")
        self._consume(TokenType.LEFT_BRACE, "Diharapkan '{' untuk memulai isi kelas.")
        methods: list[FunctionDecl] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.TUGAS, TokenType.FUNGSI):
                methods.append(self.function_declaration())
            else:
                token = self._peek()
                raise IceSyntaxError("Hanya 'tugas' yang diperbolehkan di dalam kelas.", token.line, token.column)
        self._consume(TokenType.RIGHT_BRACE, "Diharapkan '}' untuk menutup kelas.")
        return ClassDecl(name.lexeme, methods)

    def statement(self) -> Stmt:
        if self._match(TokenType.LEFT_BRACE):
            stmts = self._block_inner()
            return Block(stmts)
        if self._match(TokenType.JIKA):
            return self.if_statement()
        if self._match(TokenType.SELAGI):
            return self.while_statement()
        if self._match(TokenType.UNTUK):
            return self.for_range_statement()
        if self._match(TokenType.KEMBALIKAN):
            val = None
            if not self._check(TokenType.SEMICOLON):
                val = self.expression()
            self._consume(TokenType.SEMICOLON, "Diharapkan ';' setelah return.")
            return ReturnStmt(val)
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Diharapkan ';' setelah ekspresi.")
        return ExprStmt(expr)

    def block(self) -> Block:
        self._consume(TokenType.LEFT_BRACE, "Diharapkan '{' untuk memulai blok.")
        stmts = self._block_inner()
        return Block(stmts)

    def _block_inner(self) -> list[Stmt]:
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self.declaration())
        self._consume(TokenType.RIGHT_BRACE, "Diharapkan '}' untuk menutup blok.")
        return statements

    def if_statement(self) -> IfStmt:
        self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah 'jika'.")
        cond = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah kondisi.")
        then_block = self.block()
        branches = [(cond, then_block)]
        while self._match(TokenType.JIKALAU):
            self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah 'jikalau'.")
            c = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah kondisi.")
            b = self.block()
            branches.append((c, b))
        else_branch = None
        if self._match(TokenType.KALAU):
            else_branch = self.block()
        return IfStmt(branches, else_branch)

    def while_statement(self) -> WhileStmt:
        self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah 'selagi'.")
        cond = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah kondisi.")
        body = self.block()
        return WhileStmt(cond, body)

    def for_range_statement(self) -> ForRangeStmt:
        var = self._consume(TokenType.IDENT, "Nama variabel loop diharapkan.").lexeme
        self._consume(TokenType.DALAM, "Diharapkan kata 'dalam'.")
        self._consume(TokenType.RENTANG, "Diharapkan kata 'rentang'.")
        self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah rentang.")
        args = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self.expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah argumen rentang.")
        body = self.block()
        return ForRangeStmt(var, args, body)

    # Expressions
    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.or_()
        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            if isinstance(expr, Get):
                return Set(expr.obj, expr.name, value)
            raise IceSyntaxError("Target penugasan (assignment) tidak valid.", equals.line, equals.column)
        return expr

    def or_(self) -> Expr:
        expr = self.and_()
        while self._match(TokenType.ATAU):
            op = "atau"
            right = self.and_()
            expr = Logical(expr, op, right)
        return expr

    def and_(self) -> Expr:
        expr = self.equality()
        while self._match(TokenType.DAN):
            op = "dan"
            right = self.equality()
            expr = Logical(expr, op, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op_token = self._previous()
            op = "!=" if op_token.type == TokenType.BANG_EQUAL else "=="
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            t = self._previous().type
            op = {TokenType.GREATER: ">", TokenType.GREATER_EQUAL: ">=", TokenType.LESS: "<", TokenType.LESS_EQUAL: "<="}[t]
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = "+" if self._previous().type == TokenType.PLUS else "-"
            right = self.factor()
            expr = Binary(expr, op, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            t = self._previous().type
            op = "*" if t == TokenType.STAR else ("/" if t == TokenType.SLASH else "%")
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self) -> Expr:
        if self._match(TokenType.MINUS, TokenType.BUKAN, TokenType.BANG):
            t = self._previous().type
            op = "-" if t == TokenType.MINUS else "bukan"
            right = self.unary()
            return Unary(op, right)
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                args = []
                if not self._check(TokenType.RIGHT_PAREN):
                    while True:
                        args.append(self.expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah argumen.")
                expr = Call(expr, args)
            elif self._match(TokenType.DOT):
                name = self._consume(TokenType.IDENT, "Nama properti/method diharapkan setelah '.'").lexeme
                expr = Get(expr, name)
            else:
                break
        return expr

    def primary(self) -> Expr:
        if self._match(TokenType.SALAH):
            return Literal(False)
        if self._match(TokenType.BENAR):
            return Literal(True)
        if self._match(TokenType.KOSONG):
            return Literal(None)
        if self._match(TokenType.NUMBER):
            return Literal(self._previous().literal)
        if self._match(TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.INI):
            return This()
        if self._match(TokenType.BARU):
            cls = self._consume(TokenType.IDENT, "Nama kelas diharapkan setelah 'baru'.").lexeme
            self._consume(TokenType.LEFT_PAREN, "Diharapkan '(' setelah nama kelas.")
            args = []
            if not self._check(TokenType.RIGHT_PAREN):
                while True:
                    args.append(self.expression())
                    if not self._match(TokenType.COMMA):
                        break
            self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah argumen.")
            return NewExpr(cls, args)
        if self._match(TokenType.IDENT, TokenType.TAMPILKAN, TokenType.CETAK, TokenType.RENTANG):
            return Variable(self._previous().lexeme)
        if self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Diharapkan ')' setelah ekspresi.")
            return Grouping(expr)
        token = self._peek()
        raise IceSyntaxError("Ekspresi tidak valid.", token.line, token.column)
