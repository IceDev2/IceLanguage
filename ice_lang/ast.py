from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional

# Expressions
class Expr: pass

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Variable(Expr):
    name: str

@dataclass
class Assign(Expr):
    name: str
    value: Expr

@dataclass
class Unary(Expr):
    op: str
    right: Expr

@dataclass
class Binary(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class Logical(Expr):
    left: Expr
    op: str  # 'dan' / 'atau'
    right: Expr

@dataclass
class Grouping(Expr):
    expr: Expr

@dataclass
class Call(Expr):
    callee: Expr
    args: List[Expr]

# Statements
class Stmt: pass

@dataclass
class ExprStmt(Stmt):
    expr: Expr

@dataclass
class PrintStmt(Stmt):
    exprs: List[Expr]  # if needed, but we use builtin tampilkan()

@dataclass
class VarDecl(Stmt):
    name: str
    init: Optional[Expr]

@dataclass
class Block(Stmt):
    statements: List[Stmt]

@dataclass
class IfStmt(Stmt):
    branches: list[tuple[Expr, Block]]  # [(cond, block), ...]
    else_branch: Optional[Block]

@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Block

@dataclass
class ForRangeStmt(Stmt):
    var: str
    args: List[Expr]
    body: Block

@dataclass
class ReturnStmt(Stmt):
    value: Optional[Expr]

@dataclass
class FunctionDecl(Stmt):
    name: str
    params: List[str]
    body: Block


@dataclass
class This(Expr):
    pass

@dataclass
class Get(Expr):
    obj: Expr
    name: str

@dataclass
class Set(Expr):
    obj: Expr
    name: str
    value: Expr

@dataclass
class NewExpr(Expr):
    class_name: str
    args: List[Expr]

@dataclass
class ClassDecl(Stmt):
    name: str
    methods: List[FunctionDecl]
