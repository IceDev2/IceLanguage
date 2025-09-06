
from __future__ import annotations
from typing import Any
from .ast import *
from .errors import IceRuntimeError, IceReturnSignal
from .runtime import Environment, IceFunction, IceClass, IceInstance
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
            first_iter = True
            for v in rng:
                if first_iter and stmt.var not in self.env.values:
                    self.env.define(stmt.var, v)
                else:
                    self.env.assign(stmt.var, v)
                first_iter = False
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
                if isinstance(m, FunctionDecl):
                    methods[m.name] = IceFunction(m.name, m.params, m.body, self.env)
                elif isinstance(m, PropertyDecl):
                    if m.getter is not None:
                        methods[f"get_{m.name}"] = IceFunction(f"get_{m.name}", [], m.getter, self.env)
                    if m.setter is not None:
                        param = [m.setter_param] if m.setter_param else []
                        methods[f"set_{m.name}"] = IceFunction(f"set_{m.name}", param, m.setter, self.env)
                else:
                    raise IceRuntimeError('Anggota kelas tidak dikenal saat konstruksi.')
            superclass = None
            if stmt.superclass is not None:
                sc = self.env.get(stmt.superclass)
                if not isinstance(sc, IceClass):
                    raise IceRuntimeError('Superclass harus berupa kelas.')
                superclass = sc
            klass = IceClass(stmt.name, methods, superclass)
            # isi owner untuk method
            for name, fn in list(methods.items()):
                try:
                    fn.owner = klass
                except Exception:
                    pass
            self.env.define(stmt.name, klass)
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
        if isinstance(expr, SuperGet):
            inst = self.env.get('ini')
            try:
                current_class = self.env.get('__class__')
            except Exception:
                current_class = inst.klass
            klass = current_class
            if klass.superclass is None:
                raise IceRuntimeError("Tidak ada superclass untuk 'super'.")
            m = klass.superclass.find_method(expr.name)
            if not m:
                raise IceRuntimeError(f"Method '{expr.name}' tidak ditemukan pada superclass.")
            return m.bind(inst)
        if isinstance(expr, Assign):
            val = self.evaluate(expr.value)
            self.env.assign(expr.name, val)
            return val
        if isinstance(expr, Get):
            obj = self.evaluate(expr.obj)
            if isinstance(obj, IceInstance):
                current = None
                try:
                    current = self.env.get('ini')
                except Exception:
                    current = None
                return obj.get(expr.name, current, self)
            raise IceRuntimeError('Akses properti pada non-objek.')
        if isinstance(expr, Set):
            obj = self.evaluate(expr.obj)
            val = self.evaluate(expr.value)
            if isinstance(obj, IceInstance):
                current = None
                try:
                    current = self.env.get('ini')
                except Exception:
                    current = None
                return obj.set(expr.name, val, current, self)
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
                name = getattr(callee, 'name', type(callee).__name__)
                try:
                    arity = callee.arity()
                except Exception:
                    arity = -1
                owner = getattr(callee, 'owner', None)
                oname = getattr(owner, 'name', None)
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
        # evaluate args; we still use python range from BuiltinRentang semantics
        vals = [self.evaluate(a) if isinstance(a, Expr) else a for a in args]
        if not (1 <= len(vals) <= 3):
            raise IceRuntimeError("rentang membutuhkan 1..3 argumen")
        return range(*[int(a) for a in vals])
