// demo fitur dasar ICE

tugas faktorial(n) {
    jika (n <= 1) {
        kembalikan 1;
    } jikalau (n == 2) {
        kembalikan 2;
    } kalau {
        kembalikan n * faktorial(n - 1);
    }
}

tugas sapa(nama) {
    tampilkan("Halo,", nama);
}

bilangan total = 0;
untuk i dalam rentang(1, 6) {
    total = total + i;
    tampilkan("i =", i);
}

sapa("Dunia!");
tampilkan("5! =", faktorial(5));
tampilkan("Total =", total);
