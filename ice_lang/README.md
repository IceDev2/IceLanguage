
# ICE — Bahasa Pemrograman Berbahasa Indonesia

Fitur utama:
- `jika` / `jikalau` / `kalau` (if / else if / else)
- `tugas` (function), `kembalikan` (return)
- deklarasi variabel: `bilangan`, `desimal`, `teks`, `boolean` (hanya untuk gaya, tipe diabaikan saat runtime)
- cetak: `tampilkan(...)`
- perulangan: `selagi (kondisi) { ... }`, atau `untuk i dalam rentang(awal, akhir, [langkah]) { ... }`
- OOP: `kelas`, constructor `__init__`, `ini` (this), pemanggilan method & properti `obj.x`, `obj.m()`
- instansiasi: `baru Kelas(...)` **atau** panggil `Kelas(...)`
- **pewarisan**: `kelas Anak : Induk { ... }`
- **super**: `super.__init__(...)`, `super.metode()` untuk memanggil milik induk
- **akses**: `_privat` (hanya kelas itu sendiri), `__protected` (kelas + subclass)
- **properti** dengan sintaks khusus:
  ```
  properti nama {
    get { ... kembalikan nilai; }
    set(x) { ... }
  }
  ```
  getter/setter ini juga otomatis aktif jika Anda menulis `get_nama()` / `set_nama(x)`.

## Instal
Pastikan ada `pyproject.toml` di root (lihat di repo/ZIP ini), lalu:
```bash
pip install .
# atau untuk dev:
pip install -e .
```

## CLI
```bash
ice file.ice            # jalankan berkas .ice
ice --repl              # REPL interaktif
ice -t -a file.ice      # tampilkan tokens dan AST
ice --time file.ice     # ukur waktu eksekusi
```

## OOP
Lihat `examples/oop.ice` dan `examples/pewarisan.ice`.

## Tutorial: Menjalankan Test

Contoh test terintegrasi ada di `examples/test.ice`. Jalankan:

```bash
ice ice_lang/examples/test.ice
```

Gunakan helper berikut di test Anda:
```ice
tugas assert_sama(a, b, nama) {
    jika (a == b) { tampilkan("[OK]", nama); }
    kalau { tampilkan("[FAIL]", nama, "=>", a, "!=", b); }
}
```
