// OOP: kelas + constructor (__init__) + properti + method + 'ini' (this)

kelas Orang {
    tugas __init__(nama) {
        ini.nama = nama;
        ini.hitung = 0;
    }

    tugas sapa() {
        tampilkan("Halo, saya", ini.nama);
        ini.hitung = ini.hitung + 1;
    }
}

bilangan n = 0;

// Instansiasi bisa dengan 'baru Kelas(...)' atau memanggil nama kelas langsung:
teks siapa = "Budi";
teks o1; teks o2; // deklarasi variabel (tipe diabaikan)
o1 = baru Orang(siapa);
o1.sapa();
tampilkan("hitung =", o1.hitung);

// Panggilan langsung kelas (tanpa 'baru') juga didukung:
o2 = Orang("Sari");
o2.sapa();
tampilkan("hitung o2 =", o2.hitung);
