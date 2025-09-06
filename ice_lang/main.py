
from pathlib import Path
import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import IceSyntaxError, IceRuntimeError

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python -m ice_lang.main <file.ice>")
        sys.exit(2)
    path = Path(sys.argv[1])
    source = path.read_text(encoding="utf-8")
    try:
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        Interpreter().interpret(program)
    except (IceSyntaxError, IceRuntimeError) as e:
        print(e)
        sys.exit(1)
