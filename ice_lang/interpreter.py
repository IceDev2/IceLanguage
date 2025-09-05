
from __future__ import annotations
from typing import Any
from .ast import *
from .errors import IceRuntimeError, IceReturnSignal
from .runtime import Environment, IceFunction
from .builtins import (
    BuiltinTampilkan, BuiltinRentang,
    BuiltinPanjang, BuiltinTipe, BuiltinInt, BuiltinFloat, BuiltinStr
)

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.env = self.globals
        # builtins
        self.globals.define("tampilkan", BuiltinTampilkan())
        self.globals.define("rentang", BuiltinRentang())
        self.globals.define("panjang", BuiltinPanjang())
        self.globals.define("tipe", BuiltinTipe())
        self.globals.define("int", BuiltinInt())
        self.globals.define("float", BuiltinFloat())
        self.globals.define("str", BuiltinStr())

    # Execution
    def interpret(self, statements: list[Stmt]):
        for st in statements:
            self.execute(st)

    def execute(self, stmt: Stmt):
        if isinstance(stmt, ExprStmt):
            self.evaluate(stmt.expr)
        elif isinstance(stmt, VarDecl):
            value = None if stmt.init is None else self.evaluate(stmt.init)
            self.env.define(stmt.name, value)
        elif isinstance(stmt, Block):
            self.execute_block(stmt.statements, Environment(self.env))
        elif isinstance(stmt, IfStmt):
            done = False
            for cond, blk in stmt.branches:
                if self._is_truthy(self.evaluate(cond)):
                    self.execute(blk)
                    done = True
                    break
            if not done and stmt.else_branch:
                self.execute(stmt.else_branch)
        elif isinstance(stmt, WhileStmt):
            while self._is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)
        elif isinstance(stmt, ForRangeStmt):
            rng = self._iterable_from_args(stmt.args)
            for v in rng:
                self.env.define(stmt.var, v) if stmt.var not in self.env.values else self.env.assign(stmt.var, v)
                self.execute(stmt.body)
        elif isinstance(stmt, ReturnStmt):
            value = None if stmt.value is None else self.evaluate(stmt.value)
            raise IceReturnSignal(value)
        elif isinstance(stmt, FunctionDecl):
            func = IceFunction(stmt.name, stmt.params, stmt.body, self.env)
            self.env.define(stmt.name, func)
        elif isinstance(stmt, ClassDecl):
            methods = {}
            for m in stmt.methods:
                methods[m.name] = IceFunction(m.name, m.params, m.body, self.env)
            from .runtime import IceClass
            self.env.define(stmt.name, IceClass(stmt.name, methods))
        else:
            raise IceRuntimeError(f"Pernyataan tidak dikenal: {stmt}")

    def execute_block(self, statements: list[Stmt], new_env: Environment):
        prev = self.env
        try:
            self.env = new_env
            for st in statements:
                self.execute(st)
        finally:
            self.env = prev

    def evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Variable):
            return self.env.get(expr.name)
        if isinstance(expr, This):
            return self.env.get('ini')
        if isinstance(expr, Assign):
            val = self.evaluate(expr.value)
            self.env.assign(expr.name, val)
            return val
        if isinstance(expr, Get):
            obj = self.evaluate(expr.obj)
            from .runtime import IceInstance
            if isinstance(obj, IceInstance):
                return obj.get(expr.name)
            raise IceRuntimeError('Akses properti pada non-objek.')
        if isinstance(expr, Set):
            obj = self.evaluate(expr.obj)
            val = self.evaluate(expr.value)
            from .runtime import IceInstance
            if isinstance(obj, IceInstance):
                return obj.set(expr.name, val)
            raise IceRuntimeError('Penetapan properti pada non-objek.')
        if isinstance(expr, Grouping):
            return self.evaluate(expr.expr)
        if isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            if expr.op == "-":
                return -self._num(right, "unary '-' membutuhkan angka")
            if expr.op == "bukan":
                return not self._is_truthy(right)
            raise IceRuntimeError(f"Operator unary tidak didukung: {expr.op}")
        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.op
            if op == "+":
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                raise IceRuntimeError("Operator '+': tipe tidak cocok.")
            if op == "-": return self._num(left, "'-' butuh angka") - self._num(right, "'-' butuh angka")
            if op == "*": return self._num(left, "'*' butuh angka") * self._num(right, "'*' butuh angka")
            if op == "/": return self._num(left, "'/' butuh angka") / self._num(right, "'/' butuh angka")
            if op == "%": return self._num(left, "'%' butuh angka") % self._num(right, "'%' butuh angka")
            if op == "==": return left == right
            if op == "!=": return left != right
            if op == ">": return self._num(left, "'>' butuh angka") > self._num(right, "'>' butuh angka")
            if op == ">=": return self._num(left, "'>=' butuh angka") >= self._num(right, "'>=' butuh angka")
            if op == "<": return self._num(left, "'<' butuh angka") < self._num(right, "'<' butuh angka")
            if op == "<=": return self._num(left, "'<=' butuh angka") <= self._num(right, "'<=' butuh angka")
            raise IceRuntimeError(f"Operator biner tidak dikenal: {op}")
        if isinstance(expr, Logical):
            left = self.evaluate(expr.left)
            if expr.op == "atau":
                if self._is_truthy(left): return left
                return self.evaluate(expr.right)
            else:
                if not self._is_truthy(left): return left
                return self.evaluate(expr.right)
        if isinstance(expr, NewExpr):
            klass = self.env.get(expr.class_name)
            args = [self.evaluate(a) for a in expr.args]
            if hasattr(klass, 'call'):
                return klass.call(self, args)
            raise IceRuntimeError('Target "baru" bukan kelas yang dapat diinstansiasi.')
        if isinstance(expr, Call):
            callee = self.evaluate(expr.callee)
            args = [self.evaluate(a) for a in expr.args]
            if hasattr(callee, "call"):
                try:
                    arity = callee.arity()
                except Exception:
                    arity = -1
                if arity >= 0 and len(args) != arity:
                    raise IceRuntimeError(f"Jumlah argumen tidak cocok. Diharapkan {arity}, diberi {len(args)}.")
                return callee.call(self, args)
            raise IceRuntimeError("Objek tidak dapat dipanggil sebagai fungsi.")
        raise IceRuntimeError(f"Ekspresi tidak didukung: {expr}")

    def _num(self, v, msg):
        if isinstance(v, (int, float)): return v
        raise IceRuntimeError(msg)

    def _is_truthy(self, v):
        return bool(v)

    def _iterable_from_args(self, args):
        from .builtins import BuiltinRentang
        iter_obj = BuiltinRentang().call(self, [self.evaluate(a) if isinstance(a, Expr) else a for a in args])
        return iter_obj
