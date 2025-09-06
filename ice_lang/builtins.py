
from __future__ import annotations
from typing import Any
from .runtime import IceCallable

class BuiltinTampilkan(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        print(*args)
        return None

class BuiltinRentang(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if not (1 <= len(args) <= 3):
            raise Exception("rentang membutuhkan 1..3 argumen")
        return range(*[int(a) for a in args])

class BuiltinPanjang(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if len(args) != 1:
            raise Exception("panjang(x) membutuhkan 1 argumen")
        return len(args[0])

class BuiltinTipe(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if len(args) != 1:
            raise Exception("tipe(x) membutuhkan 1 argumen")
        x = args[0]
        if x is None: return "kosong"
        if isinstance(x, bool): return "boolean"
        if isinstance(x, int): return "bilangan"
        if isinstance(x, float): return "desimal"
        if isinstance(x, str): return "teks"
        return type(x).__name__

class BuiltinInt(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if len(args) != 1:
            raise Exception("int(x) membutuhkan 1 argumen")
        return int(args[0])

class BuiltinFloat(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if len(args) != 1:
            raise Exception("float(x) membutuhkan 1 argumen")
        return float(args[0])

class BuiltinStr(IceCallable):
    def call(self, interpreter, args: list[Any]) -> Any:
        if len(args) != 1:
            raise Exception("str(x) membutuhkan 1 argumen")
        return str(args[0])
