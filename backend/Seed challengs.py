"""
JastCodeLab — Seed Data 48 Tantangan Python
============================================
Jalankan sekali untuk mengisi tabel challenges:
    python seed_challenges.py

Strategi publish:
- Tantangan  1-10 : dipublikasi = 1 (langsung muncul) — MUDAH
- Tantangan 11-48 : dipublikasi = 0 (hidden, publish manual via admin panel)

Urutan kesulitan:
-  1-16 : Mudah
- 17-36 : Menengah
- 37-48 : Menengah-Sulit (bertahap)
"""

from database import get_db
from datetime import datetime


def seed_challenges():
    conn = get_db()
    cur  = conn.cursor()

    challenges = [

        # ══════════════════════════════════════════
        # MUDAH (1-16) — 10 pertama langsung publish
        # ══════════════════════════════════════════

        {
            "judul":         "Halo, Python!",
            "deskripsi":     "Tulis program pertamamu! Tampilkan teks 'Halo, Python!' ke layar.",
            "kode_awal":     "# Tampilkan teks: Halo, Python!\n",
            "contoh_input":  "",
            "contoh_output": "Halo, Python!",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Penjumlahan Dua Angka",
            "deskripsi":     "Buat variabel a = 15 dan b = 27, lalu tampilkan hasil penjumlahannya.",
            "kode_awal":     "# Buat variabel a dan b, lalu tampilkan a + b\n",
            "contoh_input":  "",
            "contoh_output": "42",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Luas Persegi Panjang",
            "deskripsi":     "Hitung luas persegi panjang dengan panjang = 8 dan lebar = 5. Tampilkan hasilnya.",
            "kode_awal":     "# Hitung luas persegi panjang\npanjang = 8\nlebar = 5\n# luas = ?\n",
            "contoh_input":  "",
            "contoh_output": "40",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Keliling Lingkaran",
            "deskripsi":     "Hitung keliling lingkaran dengan jari-jari r = 7. Gunakan pi = 3.14. Tampilkan hasilnya (tanpa desimal berlebih).",
            "kode_awal":     "# Hitung keliling lingkaran: 2 * pi * r\npi = 3.14\nr  = 7\n",
            "contoh_input":  "",
            "contoh_output": "43.96",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Cetak Nama 3 Kali",
            "deskripsi":     "Cetak kata 'Python' sebanyak 3 kali, masing-masing di baris baru.",
            "kode_awal":     "# Cetak 'Python' 3 kali\n",
            "contoh_input":  "",
            "contoh_output": "Python\nPython\nPython",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Konversi Suhu",
            "deskripsi":     "Konversi suhu 100 derajat Celsius ke Fahrenheit. Rumus: F = (C * 9/5) + 32",
            "kode_awal":     "# Konversi Celsius ke Fahrenheit\ncelsius = 100\n# fahrenheit = ?\n",
            "contoh_input":  "",
            "contoh_output": "212.0",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Sisa Bagi (Modulo)",
            "deskripsi":     "Tampilkan sisa pembagian dari 17 dibagi 5 menggunakan operator modulo (%).",
            "kode_awal":     "# Hitung sisa bagi 17 % 5\n",
            "contoh_input":  "",
            "contoh_output": "2",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Pangkat Dua",
            "deskripsi":     "Hitung 2 pangkat 10 menggunakan operator ** dan tampilkan hasilnya.",
            "kode_awal":     "# Hitung 2 pangkat 10\n",
            "contoh_input":  "",
            "contoh_output": "1024",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Tukar Nilai Variabel",
            "deskripsi":     "Tukar nilai variabel a = 5 dan b = 10, lalu tampilkan nilai a dan b setelah ditukar.",
            "kode_awal":     "a = 5\nb = 10\n# Tukar nilai a dan b\n# print a dan b setelah ditukar\n",
            "contoh_input":  "",
            "contoh_output": "10\n5",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Genap atau Ganjil",
            "deskripsi":     "Cek apakah angka 42 adalah genap atau ganjil. Tampilkan 'Genap' atau 'Ganjil'.",
            "kode_awal":     "angka = 42\n# Cek genap atau ganjil\n",
            "contoh_input":  "",
            "contoh_output": "Genap",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },

        # Mudah 11-16 (hidden)
        {
            "judul":         "Nilai Mutlak",
            "deskripsi":     "Tampilkan nilai mutlak dari -37 menggunakan fungsi abs().",
            "kode_awal":     "# Tampilkan nilai mutlak dari -37\n",
            "contoh_input":  "",
            "contoh_output": "37",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Panjang String",
            "deskripsi":     "Tampilkan panjang string 'JastCodeLab' menggunakan fungsi len().",
            "kode_awal":     "teks = 'JastCodeLab'\n# Tampilkan panjang teks\n",
            "contoh_input":  "",
            "contoh_output": "11",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Huruf Besar Semua",
            "deskripsi":     "Ubah string 'belajar python' menjadi huruf besar semua menggunakan method upper().",
            "kode_awal":     "teks = 'belajar python'\n# Tampilkan teks dalam huruf besar\n",
            "contoh_input":  "",
            "contoh_output": "BELAJAR PYTHON",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Elemen Pertama dan Terakhir",
            "deskripsi":     "Dari list [10, 20, 30, 40, 50], tampilkan elemen pertama dan elemen terakhir, masing-masing di baris baru.",
            "kode_awal":     "angka = [10, 20, 30, 40, 50]\n# Tampilkan elemen pertama dan terakhir\n",
            "contoh_input":  "",
            "contoh_output": "10\n50",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Jumlah List",
            "deskripsi":     "Hitung total dari semua elemen dalam list [5, 10, 15, 20, 25] menggunakan sum().",
            "kode_awal":     "angka = [5, 10, 15, 20, 25]\n# Tampilkan jumlah semua elemen\n",
            "contoh_input":  "",
            "contoh_output": "75",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Nilai Maksimum",
            "deskripsi":     "Temukan nilai terbesar dari list [34, 78, 12, 99, 45, 67] menggunakan max().",
            "kode_awal":     "nilai = [34, 78, 12, 99, 45, 67]\n# Tampilkan nilai terbesar\n",
            "contoh_input":  "",
            "contoh_output": "99",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },

        # ══════════════════════════════════════════
        # MENENGAH (17-36) — hidden
        # ══════════════════════════════════════════

        {
            "judul":         "FizzBuzz",
            "deskripsi":     "Cetak angka 1 sampai 20. Jika kelipatan 3 cetak 'Fizz', kelipatan 5 cetak 'Buzz', kelipatan keduanya cetak 'FizzBuzz'.",
            "kode_awal":     "# FizzBuzz 1 sampai 20\nfor i in range(1, 21):\n    pass\n",
            "contoh_input":  "",
            "contoh_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n16\n17\nFizz\n19\nBuzz",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Faktorial",
            "deskripsi":     "Hitung faktorial dari 6 (6! = 6 × 5 × 4 × 3 × 2 × 1) menggunakan perulangan.",
            "kode_awal":     "n = 6\nhasil = 1\n# Hitung faktorial n\n",
            "contoh_input":  "",
            "contoh_output": "720",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Balik String",
            "deskripsi":     "Balik string 'Python' sehingga menjadi 'nohtyP' menggunakan slicing.",
            "kode_awal":     "teks = 'Python'\n# Balik teks\n",
            "contoh_input":  "",
            "contoh_output": "nohtyP",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Palindrom",
            "deskripsi":     "Cek apakah kata 'katak' adalah palindrom (sama jika dibaca terbalik). Tampilkan 'Palindrom' atau 'Bukan Palindrom'.",
            "kode_awal":     "kata = 'katak'\n# Cek apakah palindrom\n",
            "contoh_input":  "",
            "contoh_output": "Palindrom",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Hitung Vokal",
            "deskripsi":     "Hitung jumlah huruf vokal (a, i, u, e, o) dalam string 'belajar python itu seru'. Tampilkan jumlahnya.",
            "kode_awal":     "teks = 'belajar python itu seru'\n# Hitung jumlah vokal\n",
            "contoh_input":  "",
            "contoh_output": "8",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Bilangan Prima",
            "deskripsi":     "Cetak semua bilangan prima antara 1 sampai 50, dipisahkan spasi dalam satu baris.",
            "kode_awal":     "# Cetak semua bilangan prima 1-50\n",
            "contoh_input":  "",
            "contoh_output": "2 3 5 7 11 13 17 19 23 29 31 37 41 43 47",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Deret Fibonacci",
            "deskripsi":     "Tampilkan 10 angka pertama deret Fibonacci (0, 1, 1, 2, 3, 5, ...) dipisahkan spasi.",
            "kode_awal":     "# Tampilkan 10 angka pertama Fibonacci\n",
            "contoh_input":  "",
            "contoh_output": "0 1 1 2 3 5 8 13 21 34",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Rata-Rata List",
            "deskripsi":     "Hitung rata-rata dari list [70, 85, 90, 65, 80, 95, 75]. Tampilkan hasilnya dengan 2 angka desimal.",
            "kode_awal":     "nilai = [70, 85, 90, 65, 80, 95, 75]\n# Hitung rata-rata\n",
            "contoh_input":  "",
            "contoh_output": "80.00",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Hapus Duplikat",
            "deskripsi":     "Hapus nilai duplikat dari list [1,2,3,2,4,3,5,1,6] dan tampilkan list yang sudah bersih (diurutkan).",
            "kode_awal":     "angka = [1, 2, 3, 2, 4, 3, 5, 1, 6]\n# Hapus duplikat dan urutkan\n",
            "contoh_input":  "",
            "contoh_output": "[1, 2, 3, 4, 5, 6]",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Frekuensi Karakter",
            "deskripsi":     "Hitung berapa kali setiap huruf muncul di 'programming'. Tampilkan setiap huruf dan jumlahnya, diurutkan alfabetis.",
            "kode_awal":     "teks = 'programming'\n# Hitung frekuensi setiap karakter\n",
            "contoh_input":  "",
            "contoh_output": "a: 1\ng: 2\ni: 1\nm: 2\nn: 1\no: 1\np: 1\nr: 2",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Fungsi Pangkat",
            "deskripsi":     "Buat fungsi pangkat(basis, eksponen) yang menghitung basis^eksponen tanpa menggunakan operator **. Hitung 3^4.",
            "kode_awal":     "def pangkat(basis, eksponen):\n    # Hitung basis^eksponen tanpa **\n    pass\n\nprint(pangkat(3, 4))\n",
            "contoh_input":  "",
            "contoh_output": "81",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Angka Terbesar Kedua",
            "deskripsi":     "Temukan angka terbesar kedua dari list [15, 42, 8, 73, 19, 55, 31] tanpa menggunakan sort().",
            "kode_awal":     "angka = [15, 42, 8, 73, 19, 55, 31]\n# Temukan angka terbesar kedua\n",
            "contoh_input":  "",
            "contoh_output": "55",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Caesar Cipher",
            "deskripsi":     "Enkripsi string 'hello' dengan Caesar Cipher geser 3 (h→k, e→h, l→o, o→r). Tampilkan hasil enkripsinya.",
            "kode_awal":     "def caesar(teks, geser):\n    hasil = ''\n    for huruf in teks:\n        # geser setiap huruf\n        pass\n    return hasil\n\nprint(caesar('hello', 3))\n",
            "contoh_input":  "",
            "contoh_output": "khoor",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Konversi Desimal ke Biner",
            "deskripsi":     "Konversi angka desimal 42 ke biner tanpa menggunakan fungsi bin(). Tampilkan hasilnya.",
            "kode_awal":     "def ke_biner(n):\n    # Konversi n ke biner tanpa bin()\n    pass\n\nprint(ke_biner(42))\n",
            "contoh_input":  "",
            "contoh_output": "101010",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Anagram",
            "deskripsi":     "Cek apakah 'listen' dan 'silent' adalah anagram (mengandung huruf yang sama). Tampilkan 'Anagram' atau 'Bukan Anagram'.",
            "kode_awal":     "kata1 = 'listen'\nkata2 = 'silent'\n# Cek apakah anagram\n",
            "contoh_input":  "",
            "contoh_output": "Anagram",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Matriks Transpos",
            "deskripsi":     "Transpose matriks 2x3 berikut menjadi 3x2. Matriks: [[1,2,3],[4,5,6]]. Tampilkan baris per baris.",
            "kode_awal":     "matriks = [[1, 2, 3], [4, 5, 6]]\n# Transpose matriks\n",
            "contoh_input":  "",
            "contoh_output": "[1, 4]\n[2, 5]\n[3, 6]",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Kata Terpanjang",
            "deskripsi":     "Temukan kata terpanjang dalam kalimat 'python adalah bahasa pemrograman yang hebat dan mudah dipelajari'.",
            "kode_awal":     "kalimat = 'python adalah bahasa pemrograman yang hebat dan mudah dipelajari'\n# Temukan kata terpanjang\n",
            "contoh_input":  "",
            "contoh_output": "pemrograman",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Jumlah Digit",
            "deskripsi":     "Hitung jumlah semua digit dari angka 123456789. Tampilkan hasilnya.",
            "kode_awal":     "angka = 123456789\n# Hitung jumlah semua digit\n",
            "contoh_input":  "",
            "contoh_output": "45",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Rotasi List",
            "deskripsi":     "Rotasi list [1,2,3,4,5] ke kanan sebanyak 2 posisi sehingga menjadi [4,5,1,2,3].",
            "kode_awal":     "angka = [1, 2, 3, 4, 5]\nk = 2\n# Rotasi list ke kanan sebanyak k\n",
            "contoh_input":  "",
            "contoh_output": "[4, 5, 1, 2, 3]",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Merge Dictionary",
            "deskripsi":     "Gabungkan dua dictionary: d1 = {'a':1,'b':2} dan d2 = {'c':3,'d':4}. Tampilkan dictionary gabungan.",
            "kode_awal":     "d1 = {'a': 1, 'b': 2}\nd2 = {'c': 3, 'd': 4}\n# Gabungkan d1 dan d2\n",
            "contoh_input":  "",
            "contoh_output": "{'a': 1, 'b': 2, 'c': 3, 'd': 4}",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },

        # ══════════════════════════════════════════
        # MENENGAH-SULIT (37-48) — hidden, bertahap
        # ══════════════════════════════════════════

        {
            "judul":         "Rekursi Faktorial",
            "deskripsi":     "Buat fungsi rekursif untuk menghitung faktorial. Hitung faktorial(7) menggunakan rekursi.",
            "kode_awal":     "def faktorial(n):\n    # Gunakan rekursi\n    pass\n\nprint(faktorial(7))\n",
            "contoh_input":  "",
            "contoh_output": "5040",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Binary Search",
            "deskripsi":     "Implementasikan binary search untuk mencari angka 37 dalam list terurut [2,7,15,22,37,49,58,71,85,99]. Tampilkan indeksnya.",
            "kode_awal":     "def binary_search(arr, target):\n    kiri, kanan = 0, len(arr) - 1\n    # Implementasikan binary search\n    pass\n\ndata = [2, 7, 15, 22, 37, 49, 58, 71, 85, 99]\nprint(binary_search(data, 37))\n",
            "contoh_input":  "",
            "contoh_output": "4",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Flatten List Bertingkat",
            "deskripsi":     "Ratakan list bertingkat [[1,2],[3,[4,5]],[6]] menjadi list 1 dimensi [1,2,3,4,5,6].",
            "kode_awal":     "def flatten(lst):\n    hasil = []\n    for item in lst:\n        # Cek apakah item adalah list\n        pass\n    return hasil\n\nprint(flatten([[1,2],[3,[4,5]],[6]]))\n",
            "contoh_input":  "",
            "contoh_output": "[1, 2, 3, 4, 5, 6]",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Bubble Sort",
            "deskripsi":     "Implementasikan algoritma bubble sort untuk mengurutkan [64,34,25,12,22,11,90] dari kecil ke besar.",
            "kode_awal":     "def bubble_sort(arr):\n    n = len(arr)\n    # Implementasikan bubble sort\n    pass\n\ndata = [64, 34, 25, 12, 22, 11, 90]\nbubble_sort(data)\nprint(data)\n",
            "contoh_input":  "",
            "contoh_output": "[11, 12, 22, 25, 34, 64, 90]",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Kelompokkan Ganjil Genap",
            "deskripsi":     "Pisahkan list [1,2,3,4,5,6,7,8,9,10] menjadi dua list: ganjil dan genap. Tampilkan keduanya.",
            "kode_awal":     "angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n# Pisahkan ganjil dan genap\n",
            "contoh_input":  "",
            "contoh_output": "Ganjil: [1, 3, 5, 7, 9]\nGenap: [2, 4, 6, 8, 10]",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Pangkat Rekursif",
            "deskripsi":     "Buat fungsi rekursif hitung_pangkat(basis, eksponen) yang menghitung basis^eksponen. Hitung 2^10.",
            "kode_awal":     "def hitung_pangkat(basis, eksponen):\n    # Gunakan rekursi\n    pass\n\nprint(hitung_pangkat(2, 10))\n",
            "contoh_input":  "",
            "contoh_output": "1024",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Kelas Persegi Panjang",
            "deskripsi":     "Buat class PersegiPanjang dengan method luas() dan keliling(). Buat objek dengan panjang=8, lebar=5 lalu tampilkan luas dan kelilingnya.",
            "kode_awal":     "class PersegiPanjang:\n    def __init__(self, panjang, lebar):\n        pass\n\n    def luas(self):\n        pass\n\n    def keliling(self):\n        pass\n\np = PersegiPanjang(8, 5)\nprint(p.luas())\nprint(p.keliling())\n",
            "contoh_input":  "",
            "contoh_output": "40\n26",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Pangkat Semua Elemen",
            "deskripsi":     "Gunakan map() untuk mengkuadratkan semua elemen list [1,2,3,4,5]. Tampilkan hasilnya sebagai list.",
            "kode_awal":     "angka = [1, 2, 3, 4, 5]\n# Gunakan map() untuk mengkuadratkan\n",
            "contoh_input":  "",
            "contoh_output": "[1, 4, 9, 16, 25]",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "GCD dan LCM",
            "deskripsi":     "Hitung GCD (FPB) dan LCM (KPK) dari 48 dan 18. Tampilkan GCD dan LCM masing-masing di baris baru.",
            "kode_awal":     "def gcd(a, b):\n    # Gunakan algoritma Euclidean\n    pass\n\ndef lcm(a, b):\n    # LCM = (a * b) / gcd(a, b)\n    pass\n\nprint(gcd(48, 18))\nprint(lcm(48, 18))\n",
            "contoh_input":  "",
            "contoh_output": "6\n144",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Angka Armstrong",
            "deskripsi":     "Cek apakah 153 adalah angka Armstrong (153 = 1³ + 5³ + 3³ = 1+125+27 = 153). Tampilkan 'Armstrong' atau 'Bukan Armstrong'.",
            "kode_awal":     "n = 153\n# Cek angka Armstrong\n",
            "contoh_input":  "",
            "contoh_output": "Armstrong",
            "tingkat":       "menengah",
            "xp_reward":     30,
        },
        {
            "judul":         "Stack Sederhana",
            "deskripsi":     "Implementasikan stack sederhana dengan class. Tambahkan 3 elemen (1,2,3), lalu pop dua kali dan tampilkan elemen yang dikeluarkan.",
            "kode_awal":     "class Stack:\n    def __init__(self):\n        self.data = []\n\n    def push(self, item):\n        pass\n\n    def pop(self):\n        pass\n\ns = Stack()\ns.push(1)\ns.push(2)\ns.push(3)\nprint(s.pop())\nprint(s.pop())\n",
            "contoh_input":  "",
            "contoh_output": "3\n2",
            "tingkat":       "menengah",
            "xp_reward":     35,
        },
        {
            "judul":         "Dekoder Frekuensi",
            "deskripsi":     "Buat fungsi yang menerima list kata dan mengembalikan dictionary berisi frekuensi setiap kata. Input: ['apel','mangga','apel','jeruk','mangga','apel']",
            "kode_awal":     "def hitung_frekuensi(kata_list):\n    frek = {}\n    # Hitung frekuensi setiap kata\n    pass\n    return frek\n\nkata = ['apel', 'mangga', 'apel', 'jeruk', 'mangga', 'apel']\nhasil = hitung_frekuensi(kata)\nfor k in sorted(hasil):\n    print(f'{k}: {hasil[k]}')\n",
            "contoh_input":  "",
            "contoh_output": "apel: 3\njeruk: 1\nmangga: 2",
            "tingkat":       "menengah",
            "xp_reward":     35,
        },
    ]

    berhasil = 0
    for i, ch in enumerate(challenges, start=1):
        # 10 pertama langsung publish, sisanya hidden
        dipublikasi = 1 if i <= 10 else 0
        status_txt  = "✅ PUBLISH" if dipublikasi else "🔒 hidden "

        try:
            cur.execute("""
                INSERT INTO challenges
                    (judul, deskripsi, kode_awal, contoh_input, contoh_output,
                     tingkat, xp_reward, dipublikasi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                ch["judul"],
                ch["deskripsi"],
                ch["kode_awal"],
                ch["contoh_input"],
                ch["contoh_output"],
                ch["tingkat"],
                ch["xp_reward"],
                dipublikasi,
            ))
            berhasil += 1
            print(f"  {status_txt} [{i:02d}] {ch['judul']}")
        except Exception as e:
            print(f"  ❌ [{i:02d}] {ch['judul']}: {e}")

    conn.commit()
    conn.close()

    print(f"""
🎉 Selesai! {berhasil}/{len(challenges)} tantangan berhasil ditambahkan.

📋 Ringkasan:
   ✅ 10 tantangan MUDAH langsung publish (muncul di halaman)
   🔒 38 tantangan tersembunyi (publish manual via Admin Panel)

💡 Cara publish tantangan berikutnya:
   → Buka Admin Panel di browser
   → Klik menu Tantangan
   → Klik tombol Publish pada tantangan yang ingin ditampilkan
   → Tidak perlu edit kode atau database sama sekali!

📅 Saran jadwal publish:
   - Sekarang    : 10 tantangan mudah (sudah aktif)
   - Minggu ke-2 : Publish 6 tantangan mudah berikutnya (no.11-16)
   - Minggu ke-3 : Publish 10 tantangan menengah (no.17-26)
   - Minggu ke-4 : Publish 10 tantangan menengah (no.27-36)
   - Bulan ke-2  : Publish 12 tantangan menengah-sulit (no.37-48)
""")


if __name__ == "__main__":
    print("⚡ Menambahkan 48 tantangan Python ke database...\n")
    seed_challenges()