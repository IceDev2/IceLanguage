# ICE Language (Bahasa Indonesia)

Arsitektur dipisah:
- `lexer.py` — lexer/tokenizer
- `parser.py` — parser (AST)
- `ast.py` — definisi node AST
- `interpreter.py` — interpreter (visitor)
- `runtime.py` — environment, function, dll
- `builtins.py` — fungsi bawaan (`tampilkan`, `rentang`)
- `errors.py` — kelas error
- `main.py` — CLI runner
- `examples/hello.ice` — contoh

## Jalankan
```bash
# dari folder yang berisi paket ice_lang/
python -m ice_lang.main ice_lang/examples/hello.ice
```

## Fitur Bahasa (MVP)
- `tugas nama(args) { ... }` — fungsi
- `jika (cond) { ... } jikalau (cond) { ... } kalau { ... }` — if/elif/else
- `selagi (cond) { ... }` — while
- `untuk i dalam rentang(a, b, [c]) { ... }` — loop rentang
- `kembalikan expr;` — return
- `tampilkan(...)` — cetak ke stdout
- `benar/salah`, `bukan`, `dan/atau`, `kosong`
- Deklarasi bertipe opsional: `bilangan x = 0;`, `teks s;` (tipe diabaikan saat runtime)

## Roadmap Selanjutnya
- `kelas` OOP (constructor, properti, method)
- module system (`impor`), stdlib (string, math, waktu)
- error reporter lebih rapi (caret, snippet)
- arity checking & default params
- optimizer & transpiler ke Python
- REPL dan formatter


## CLI
Setelah `pip install .`, perintah berikut tersedia:
```bash
ice file.ice            # jalankan berkas .ice
ice --repl              # REPL interaktif
ice -t -a file.ice      # tampilkan tokens dan AST
ice --time file.ice     # ukur waktu eksekusi
```
Jika tidak menginstal, pakai launcher:
```bash
# Linux/macOS
bash scripts/ice ice_lang/examples/hello.ice
# Windows (PowerShell)
scripts\ice.cmd ice_lang\examples\hello.ice
```


## OOP
Fitur pemrograman berorientasi objek:

- `kelas Nama { ... }` mendefinisikan kelas.
- Konstruktor bernama `__init__(...)` dipanggil saat instansiasi.
- Gunakan `ini` di dalam method untuk mengakses instance (setara `this`).
- Akses properti/method dengan `obj.properti` / `obj.method(...)`.
- Instansiasi:
  - `baru Nama(arg1, arg2)` atau
  - `Nama(arg1, arg2)` (memanggil kelas langsung).

Contoh: lihat `examples/oop.ice`.
