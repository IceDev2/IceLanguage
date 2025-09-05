from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Callable
from .errors import IceRuntimeError, IceReturnSignal

@dataclass
class Environment:
    enclosing: Optional['Environment'] = None

    def __post_init__(self):
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise IceRuntimeError(f"Variabel tidak didefinisikan: {name}")

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise IceRuntimeError(f"Variabel tidak didefinisikan: {name}")

class IceCallable:
    def arity(self) -> int: return -1  # variadic default
    def call(self, interpreter, args: list[Any]) -> Any: raise NotImplementedError

class IceFunction(IceCallable):
    def __init__(self, name: str, params: list[str], body, closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def bind(self, instance: 'IceInstance') -> 'IceFunction':
        env = Environment(self.closure)
        env.define('ini', instance)
        return IceFunction(self.name, self.params, self.body, env)

    def __repr__(self):
        return f"<fungsi {self.name}>"

    def arity(self) -> int:
        return len(self.params)

    def call(self, interpreter, args: list[Any]) -> Any:
        env = Environment(self.closure)
        for p, v in zip(self.params, args):
            env.define(p, v)
        try:
            interpreter.execute_block(self.body.statements, env)
        except IceReturnSignal as r:
            return r.value
        return None


class IceClass(IceCallable):
    def __init__(self, name: str, methods: dict[str, IceFunction]):
        self.name = name
        self.methods = methods

    def __repr__(self):
        return f"<kelas {self.name}>"

    def call(self, interpreter, args: list[Any]) -> Any:
        instance = IceInstance(self)
        initializer = self.methods.get("__init__")
        if initializer:
            bound = initializer.bind(instance)
            if bound.arity() != len(args) and bound.arity() >= 0:
                raise IceRuntimeError(f"Constructor __init__ mengharapkan {bound.arity()} argumen, diberi {len(args)}.")
            bound.call(interpreter, args)
        return instance

    def arity(self) -> int:
        init = self.methods.get("__init__")
        return len(init.params) if init else 0

class IceInstance:
    def __init__(self, klass: IceClass):
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def get(self, name: str):
        if name in self.fields:
            return self.fields[name]
        method = self.klass.methods.get(name)
        if method:
            return method.bind(self)
        raise IceRuntimeError(f"Properti atau method tidak ditemukan: {name}")

    def set(self, name: str, value: Any):
        self.fields[name] = value
        return value

    def __repr__(self):
        return f"<{self.klass.name} instance>"
