
#!/usr/bin/env python3
import sys, argparse, time, re
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import IceSyntaxError, IceRuntimeError

VERSION = "0.2.0"

def run_source(source: str, show_tokens=False, show_ast=False, use_env=None):
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    if show_tokens:
        for t in tokens:
            print(t)
    parser = Parser(tokens)
    program = parser.parse()
    if show_ast:
        for node in program:
            print(repr(node))
    interp = use_env or Interpreter()
    interp.interpret(program)
    return interp

def run_file(path: Path, **opts):
    source = path.read_text(encoding="utf-8")
    return run_source(source, **opts)

def brace_delta(s: str) -> int:
    # Hapus literal string supaya brace di dalam string diabaikan
    s2 = re.sub(r"'(?:\\.|[^'])*'|\\\"(?:\\\\.|[^\\\"])*\\\"", "", s)
    return s2.count('{') - s2.count('}')

def repl():
    print("ICE REPL — ketik 'keluar' untuk berhenti. Baris kosong mengeksekusi buffer.")
    interp = Interpreter()
    buf = []
    depth = 0
    while True:
        try:
            prompt = "... " if depth > 0 or buf else "ice> "
            line = input(prompt)
        except EOFError:
            print()
            break
        if line.strip() == "keluar":
            break
        depth += brace_delta(line)
        buf.append(line)
        if depth <= 0 and (not line.strip() or line.strip().endswith(";") or line.strip().endswith("}")):
            src = "\n".join(buf) + "\n"
            buf.clear(); depth = 0
            if not src.strip():
                continue
            try:
                run_source(src, use_env=interp)
            except (IceSyntaxError, IceRuntimeError) as e:
                print(e)

def main():
    ap = argparse.ArgumentParser(prog="ice", description="ICE language runner")
    ap.add_argument("file", nargs="?", help="file .ice (atau '-' untuk stdin)")
    ap.add_argument("-t", "--show-tokens", action="store_true", help="tampilkan token hasil lexing")
    ap.add_argument("-a", "--show-ast", action="store_true", help="tampilkan AST hasil parsing")
    ap.add_argument("--time", action="store_true", help="ukur waktu eksekusi")
    ap.add_argument("--repl", action="store_true", help="masuk mode REPL")
    ap.add_argument("--version", action="store_true", help="tampilkan versi")
    args = ap.parse_args()

    if args.version:
        print(VERSION); return

    if args.repl or not args.file:
        repl(); return

    if args.file == "-":
        source = sys.stdin.read()
        t0 = time.time()
        run_source(source, show_tokens=args.show_tokens, show_ast=args.show_ast)
        if args.time:
            print(f"Waktu: {time.time()-t0:.4f}s")
    else:
        path = Path(args.file)
        if not path.exists():
            print(f"File tidak ditemukan: {path}", file=sys.stderr)
            sys.exit(2)
        t0 = time.time()
        run_file(path, show_tokens=args.show_tokens, show_ast=args.show_ast)
        if args.time:
            print(f"Waktu: {time.time()-t0:.4f}s")

if __name__ == "__main__":
    main()
