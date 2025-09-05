#!/usr/bin/env python3
import sys
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import IceSyntaxError, IceRuntimeError

USAGE = "Penggunaan: python -m ice_lang.main <file.ice>"

def run_file(path: Path):
    source = path.read_text(encoding="utf-8")
    # Lex
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    # Parse
    parser = Parser(tokens)
    program = parser.parse()
    # Interpret
    interp = Interpreter()
    interp.interpret(program)

def main():
    if len(sys.argv) < 2:
        print(USAGE); sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File tidak ditemukan: {path}")
        sys.exit(2)
    try:
        run_file(path)
    except IceSyntaxError as e:
        print(f"[Sintaks] {e.message} (baris {e.line}, kolom {e.column})")
        sys.exit(3)
    except IceRuntimeError as e:
        loc = f" (baris {e.line}, kolom {e.column})" if e.line else ""
        print(f"[Runtime] {e.message}{loc}")
        sys.exit(4)

if __name__ == "__main__":
    main()
