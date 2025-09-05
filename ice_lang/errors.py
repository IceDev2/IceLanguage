from dataclasses import dataclass

class IceError(Exception):
    pass

@dataclass
class IceSyntaxError(IceError):
    message: str
    line: int
    column: int

@dataclass
class IceRuntimeError(IceError):
    message: str
    line: int | None = None
    column: int | None = None

class IceReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
