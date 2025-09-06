// Pewarisan, privat/protected via konvensi, dan properti getter/setter

kelas Hewan {
    tugas __init__(nama) {
        ini._nama = nama;     // privat
        ini.__umur = 0;       // protected
    }

    properti nama {
        get { kembalikan ini._nama; }
        set(n) { jika (panjang(n) > 0) { ini._nama = n; } }
    }

    tugas sapa() { tampilkan("Aku hewan bernama", ini._nama); }
}

kelas Anjing : Hewan {
    tugas __init__(nama, ras) {
        super.__init__(nama);
        ini.ras = ras;
    }

    tugas sapa() {
        tampilkan("Guk! Namaku", ini._nama, "ras", ini.ras);
        super.sapa();
    }
}

// --- Demo ---
tampilkan("=== Demo Pewarisan & Properti ===");
teks a;
a = baru Anjing("Dogi", "Kintamani");
a.sapa();
tampilkan("Nama:", a.nama);   // via getter
a.nama = "Doge";              // via setter
tampilkan("Nama baru:", a.nama);
