// Test suite: pewarisan multi-level, super, properti syntax, privat/protected

tugas assert_sama(a, b, nama) {
    jika (a == b) { tampilkan("[OK]", nama); }
    kalau { tampilkan("[FAIL]", nama, "=>", a, "!=", b); }
}

kelas A {
    tugas __init__(x) { ini.__x = x; ini._sekret = "rahasiaA"; ini.pub = "A"; }

    properti nilai {
        get { kembalikan ini.__x; }
        set(v) { ini.__x = v; }
    }

    tugas sapa() { kembalikan 1; }
}

kelas B : A {
    tugas __init__(x, y) { super.__init__(x); ini.y = y; ini.pub = "B"; }
    tugas sapa() { kembalikan super.sapa() + 1; }
    tugas baca_protected() { kembalikan ini.__x; } // protected
}

kelas C : B {
    tugas __init__(x, y, z) { super.__init__(x, y); ini.z = z; ini.pub = "C"; }
    tugas sapa() { kembalikan super.sapa() + 1; }
}

tampilkan("=== MULAI TEST ===");
teks obj;
obj = baru C(10, 20, 30);

// properti syntax
assert_sama(obj.nilai, 10, "getter properti");
obj.nilai = 99;
assert_sama(obj.nilai, 99, "setter properti");

// super chain: A(1) -> B(+1) -> C(+1) = 3
assert_sama(obj.sapa(), 3, "super chain override");

// protected via subclass OK
assert_sama(obj.baca_protected(), 99, "protected via subclass");

// publik
obj.pub = "X";
assert_sama(obj.pub, "X", "field publik");

tampilkan("=== SELESAI TEST ===");
