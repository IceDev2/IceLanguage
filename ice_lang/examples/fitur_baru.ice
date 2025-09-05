// Fitur baru: panjang, tipe, int/float/str dan REPL tersedia via 'ice --repl'

tugas demo() {
    teks kalimat = "Halo ICE!";
    tampilkan("kalimat:", kalimat);
    tampilkan("panjang:", panjang(kalimat));
    tampilkan("tipe(123):", tipe(123));
    tampilkan("tipe(3.14):", tipe(3.14));
    tampilkan("tipe(\"x\"):", tipe("x"));
    tampilkan("konversi:", int("42"), float("3.5"), str(100));
}

demo();
