
from __future__ import annotations
from typing import Any, Optional

class Environment:
    def __init__(self, enclosing: 'Environment|None'=None):
        self.enclosing = enclosing
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value; return
        if self.enclosing is not None:
            self.enclosing.assign(name, value); return
        raise Exception(f"Variabel tidak didefinisikan: {name}")

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise Exception(f"Variabel tidak didefinisikan: {name}")

class IceCallable:
    def arity(self) -> int: return -1
    def call(self, interpreter, args: list[Any]) -> Any: raise NotImplementedError

class IceFunction(IceCallable):
    def __init__(self, name: str, params: list[str], body, closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure
        self.owner = None  # akan diisi oleh interpreter saat membangun kelas

    def bind(self, instance: 'IceInstance') -> 'IceFunction':
        env = Environment(self.closure)
        env.define('ini', instance)
        f = IceFunction(self.name, self.params, self.body, env)
        f.owner = self.owner
        return f

    def arity(self) -> int:
        return len(self.params)

    def call(self, interpreter, args: list[Any]) -> Any:
        from .errors import IceReturnSignal
        env = Environment(self.closure)
        if self.owner is not None:
            env.define('__class__', self.owner)
        for i, p in enumerate(self.params):
            env.define(p, args[i] if i < len(args) else None)
        prev = interpreter.env
        try:
            interpreter.env = env
            interpreter.execute(self.body)
        except IceReturnSignal as rs:
            return rs.value
        finally:
            interpreter.env = prev
        return None

class IceClass(IceCallable):
    def __init__(self, name: str, methods: dict[str, IceFunction], superclass: 'IceClass|None'=None):
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def __repr__(self):
        return f"<kelas {self.name}>"

    def is_subclass_of(self, other: 'IceClass') -> bool:
        k = self.superclass
        while k is not None:
            if k is other:
                return True
            k = k.superclass
        return False

    def find_method(self, name: str):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.find_method(name)
        return None

    def call(self, interpreter, args: list[Any]) -> Any:
        instance = IceInstance(self)
        initializer = self.find_method("__init__")
        if initializer:
            bound = initializer.bind(instance)
            if bound.arity() != len(args) and bound.arity() >= 0:
                raise Exception(f"Constructor __init__ mengharapkan {bound.arity()} argumen, diberi {len(args)}.")
            bound.call(interpreter, args)
        return instance

    def arity(self) -> int:
        init = self.find_method("__init__")
        return len(init.params) if init else 0

class IceInstance:
    def __init__(self, klass: IceClass):
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def _check_access(self, name: str, current_instance: 'IceInstance|None'):
        if name.startswith('__'):
            if current_instance is None:
                raise Exception(f"Anggota protected '{name}' hanya boleh diakses dari dalam kelas atau subclass.")
            if not (current_instance.klass is self.klass or current_instance.klass.is_subclass_of(self.klass)):
                raise Exception(f"Anggota protected '{name}' hanya untuk kelas {self.klass.name} dan turunannya.")
        elif name.startswith('_'):
            if current_instance is None or current_instance.klass is not self.klass:
                raise Exception(f"Anggota privat '{name}' hanya boleh diakses dalam kelas {self.klass.name}.")

    def get(self, name: str, current_instance: 'IceInstance|None'=None, interpreter=None):
        self._check_access(name, current_instance)
        if name in self.fields:
            return self.fields[name]
        getter = self.klass.find_method(f"get_{name}")
        if getter:
            return getter.bind(self).call(interpreter, [])
        method = self.klass.find_method(name)
        if method:
            return method.bind(self)
        raise Exception(f"Properti atau method tidak ditemukan: {name}")

    def set(self, name: str, value: Any, current_instance: 'IceInstance|None'=None, interpreter=None):
        self._check_access(name, current_instance)
        setter = self.klass.find_method(f"set_{name}")
        if setter:
            setter.bind(self).call(interpreter, [value])
            return value
        self.fields[name] = value
        return value

    def __repr__(self):
        return f"<{self.klass.name} instance>"
