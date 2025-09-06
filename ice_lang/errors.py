
class IceSyntaxError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(f"SyntaxError (baris {line}, kolom {column}): {message}")
        self.line = line
        self.column = column

class IceRuntimeError(Exception):
    pass

class IceReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
