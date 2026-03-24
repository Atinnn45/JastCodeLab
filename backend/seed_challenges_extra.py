"""
JastCodeLab — Seed Tantangan Tambahan (Sesuai Pelajaran)
=========================================================
Jalankan setelah seed_challenges.py:
    python seed_challenges_extra.py

Tantangan ini dirancang sesuai urutan 20 pelajaran:
- Pelajaran 1-5  (Variabel)        → Tantangan extra 1-8
- Pelajaran 6-10 (Tipe Data)       → Tantangan extra 9-16
- Pelajaran 11-15 (Input/Output)   → Tantangan extra 17-24
- Pelajaran 16-20 (Lanjutan)       → Tantangan extra 25-32

Semua dipublikasi = 0 (hidden), publish manual sesuai jadwal pelajaran.
"""

from database import get_db
from datetime import datetime


def seed_challenges_extra():
    conn = get_db()
    cur  = conn.cursor()

    challenges = [

        # ══════════════════════════════════════════
        # SESUAI PELAJARAN 1-5: VARIABEL
        # ══════════════════════════════════════════

        {
            "judul":         "Hitung Indeks Massa Tubuh",
            "deskripsi":     "Hitung BMI seseorang dengan berat = 65 kg dan tinggi = 170 cm. Rumus: BMI = berat / (tinggi_meter ** 2). Tampilkan hasilnya dengan 2 angka desimal.",
            "kode_awal":     "berat  = 65\ntinggi = 170\n# Hitung BMI\n",
            "contoh_input":  "",
            "contoh_output": "22.49",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Konversi Menit ke Jam",
            "deskripsi":     "Konversi 145 menit ke jam dan menit. Tampilkan dalam format '2 jam 25 menit'.",
            "kode_awal":     "total_menit = 145\n# Konversi ke jam dan menit\n",
            "contoh_input":  "",
            "contoh_output": "2 jam 25 menit",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Harga Setelah Diskon",
            "deskripsi":     "Harga barang Rp 250000 dan diskon 20%. Hitung harga setelah diskon dan tampilkan hasilnya.",
            "kode_awal":     "harga  = 250000\ndiskon = 20\n# Hitung harga setelah diskon\n",
            "contoh_input":  "",
            "contoh_output": "200000.0",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Luas dan Keliling Persegi",
            "deskripsi":     "Hitung luas dan keliling persegi dengan sisi = 12. Tampilkan luas di baris pertama dan keliling di baris kedua.",
            "kode_awal":     "sisi = 12\n# Hitung luas dan keliling\n",
            "contoh_input":  "",
            "contoh_output": "144\n48",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Kecepatan Rata-Rata",
            "deskripsi":     "Sebuah kendaraan menempuh jarak 240 km dalam 3 jam. Hitung kecepatan rata-ratanya (km/jam) dan tampilkan hasilnya.",
            "kode_awal":     "jarak = 240\nwaktu = 3\n# Hitung kecepatan rata-rata\n",
            "contoh_input":  "",
            "contoh_output": "80.0",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Tukar Tiga Variabel",
            "deskripsi":     "Tukar nilai: a=1, b=2, c=3 sehingga menjadi a=3, b=1, c=2. Tampilkan nilai a, b, c masing-masing di baris baru.",
            "kode_awal":     "a = 1\nb = 2\nc = 3\n# Tukar nilai sehingga a=3, b=1, c=2\n",
            "contoh_input":  "",
            "contoh_output": "3\n1\n2",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Celsius ke Kelvin",
            "deskripsi":     "Konversi suhu 25 derajat Celsius ke Kelvin. Rumus: K = C + 273.15. Tampilkan hasilnya.",
            "kode_awal":     "celsius = 25\n# Konversi ke Kelvin\n",
            "contoh_input":  "",
            "contoh_output": "298.15",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Volume Kubus",
            "deskripsi":     "Hitung volume kubus dengan sisi = 7. Rumus: V = sisi³. Tampilkan hasilnya.",
            "kode_awal":     "sisi = 7\n# Hitung volume kubus\n",
            "contoh_input":  "",
            "contoh_output": "343",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },

        # ══════════════════════════════════════════
        # SESUAI PELAJARAN 6-10: TIPE DATA
        # ══════════════════════════════════════════

        {
            "judul":         "Cek Tipe Data",
            "deskripsi":     "Tampilkan tipe data dari: 42, 3.14, 'Python', True. Masing-masing di baris baru menggunakan type().",
            "kode_awal":     "# Tampilkan tipe data dari 4 nilai\n",
            "contoh_input":  "",
            "contoh_output": "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Gabung String",
            "deskripsi":     "Gabungkan kata 'Belajar', 'Python', 'Itu', 'Seru' dengan spasi di antaranya menggunakan join(). Tampilkan hasilnya.",
            "kode_awal":     "kata = ['Belajar', 'Python', 'Itu', 'Seru']\n# Gabungkan dengan spasi\n",
            "contoh_input":  "",
            "contoh_output": "Belajar Python Itu Seru",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Hitung Kata dalam Kalimat",
            "deskripsi":     "Hitung jumlah kata dalam kalimat 'aku suka belajar python setiap hari'. Tampilkan jumlahnya.",
            "kode_awal":     "kalimat = 'aku suka belajar python setiap hari'\n# Hitung jumlah kata\n",
            "contoh_input":  "",
            "contoh_output": "6",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Urutkan List Terbalik",
            "deskripsi":     "Urutkan list [3,1,4,1,5,9,2,6] dari besar ke kecil dan tampilkan hasilnya.",
            "kode_awal":     "angka = [3, 1, 4, 1, 5, 9, 2, 6]\n# Urutkan dari besar ke kecil\n",
            "contoh_input":  "",
            "contoh_output": "[9, 6, 5, 4, 3, 2, 1, 1]",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Akses Dictionary",
            "deskripsi":     "Dari dictionary berikut, tampilkan nama dan nilai secara berurutan.\nprofil = {'nama': 'Budi', 'nilai': 95, 'kota': 'Jakarta'}",
            "kode_awal":     "profil = {'nama': 'Budi', 'nilai': 95, 'kota': 'Jakarta'}\n# Tampilkan nama dan nilai\n",
            "contoh_input":  "",
            "contoh_output": "Budi\n95",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Cek Keanggotaan List",
            "deskripsi":     "Cek apakah 'Python' ada dalam list ['Java','Python','Go','Rust']. Tampilkan True atau False.",
            "kode_awal":     "bahasa = ['Java', 'Python', 'Go', 'Rust']\n# Cek apakah 'Python' ada\n",
            "contoh_input":  "",
            "contoh_output": "True",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Konversi Boolean",
            "deskripsi":     "Tampilkan hasil konversi berikut ke boolean: 0, 1, '', 'python', [], [1,2,3]. Masing-masing di baris baru.",
            "kode_awal":     "# Tampilkan bool() dari setiap nilai\n",
            "contoh_input":  "",
            "contoh_output": "False\nTrue\nFalse\nTrue\nFalse\nTrue",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },
        {
            "judul":         "Tambah dan Hapus Elemen List",
            "deskripsi":     "Dari list [1,2,3,4,5], hapus elemen terakhir lalu tambahkan angka 10 di awal. Tampilkan list hasil akhirnya.",
            "kode_awal":     "angka = [1, 2, 3, 4, 5]\n# Hapus terakhir, tambah 10 di awal\n",
            "contoh_input":  "",
            "contoh_output": "[10, 1, 2, 3, 4]",
            "tingkat":       "mudah",
            "xp_reward":     10,
        },

        # ══════════════════════════════════════════
        # SESUAI PELAJARAN 11-15: INPUT/OUTPUT & KONDISI
        # ══════════════════════════════════════════

        {
            "judul":         "Nilai Huruf",
            "deskripsi":     "Konversi nilai 88 ke huruf. A(90-100), B(80-89), C(70-79), D(60-69), E(<60). Tampilkan hurufnya.",
            "kode_awal":     "nilai = 88\n# Konversi nilai ke huruf\n",
            "contoh_input":  "",
            "contoh_output": "B",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Tahun Kabisat",
            "deskripsi":     "Cek apakah tahun 2024 adalah tahun kabisat. Tahun kabisat: habis dibagi 4, tapi jika habis dibagi 100 harus juga habis dibagi 400. Tampilkan 'Kabisat' atau 'Bukan Kabisat'.",
            "kode_awal":     "tahun = 2024\n# Cek tahun kabisat\n",
            "contoh_input":  "",
            "contoh_output": "Kabisat",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Segitiga Bintang",
            "deskripsi":     "Tampilkan segitiga bintang dengan tinggi 5 baris seperti output berikut.",
            "kode_awal":     "# Tampilkan segitiga bintang tinggi 5\n",
            "contoh_input":  "",
            "contoh_output": "*\n**\n***\n****\n*****",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Jumlah Kelipatan 3",
            "deskripsi":     "Hitung jumlah semua kelipatan 3 dari 1 sampai 50 (inklusif). Tampilkan hasilnya.",
            "kode_awal":     "# Hitung jumlah kelipatan 3 dari 1-50\n",
            "contoh_input":  "",
            "contoh_output": "408",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Format Tabel Sederhana",
            "deskripsi":     "Tampilkan tabel perkalian 3 baris pertama (1x1 sampai 3x3) dengan format rapi seperti output.",
            "kode_awal":     "# Tampilkan tabel perkalian 3x3\n",
            "contoh_input":  "",
            "contoh_output": "1 2 3\n2 4 6\n3 6 9",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Deret Angka Genap",
            "deskripsi":     "Tampilkan semua angka genap dari 2 sampai 20 dipisahkan spasi dalam satu baris.",
            "kode_awal":     "# Tampilkan angka genap 2-20\n",
            "contoh_input":  "",
            "contoh_output": "2 4 6 8 10 12 14 16 18 20",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Filter List Comprehension",
            "deskripsi":     "Dari list [1,2,3,4,5,6,7,8,9,10], buat list baru yang hanya berisi angka yang habis dibagi 3 menggunakan list comprehension.",
            "kode_awal":     "angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n# Gunakan list comprehension\n",
            "contoh_input":  "",
            "contoh_output": "[3, 6, 9]",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },
        {
            "judul":         "Hitung Mundur",
            "deskripsi":     "Tampilkan hitung mundur dari 10 sampai 1, lalu tampilkan 'Selesai!' di baris terakhir.",
            "kode_awal":     "# Hitung mundur dari 10 ke 1\n",
            "contoh_input":  "",
            "contoh_output": "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\nSelesai!",
            "tingkat":       "mudah",
            "xp_reward":     15,
        },

        # ══════════════════════════════════════════
        # SESUAI PELAJARAN 16-20: LANJUTAN
        # ══════════════════════════════════════════

        {
            "judul":         "Fungsi Nilai Terbesar",
            "deskripsi":     "Buat fungsi terbesar(a, b, c) yang mengembalikan nilai terbesar dari tiga angka tanpa menggunakan max(). Uji dengan terbesar(15, 42, 27).",
            "kode_awal":     "def terbesar(a, b, c):\n    # Cari terbesar tanpa max()\n    pass\n\nprint(terbesar(15, 42, 27))\n",
            "contoh_input":  "",
            "contoh_output": "42",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Balik Kata dalam Kalimat",
            "deskripsi":     "Balik urutan kata dalam kalimat 'saya suka python' menjadi 'python suka saya'. Tampilkan hasilnya.",
            "kode_awal":     "kalimat = 'saya suka python'\n# Balik urutan kata\n",
            "contoh_input":  "",
            "contoh_output": "python suka saya",
            "tingkat":       "menengah",
            "xp_reward":     20,
        },
        {
            "judul":         "Kelas Lingkaran",
            "deskripsi":     "Buat class Lingkaran dengan method luas() dan keliling(). Gunakan pi = 3.14. Buat objek dengan jari_jari=10 dan tampilkan luas lalu keliling.",
            "kode_awal":     "class Lingkaran:\n    pi = 3.14\n\n    def __init__(self, jari_jari):\n        pass\n\n    def luas(self):\n        pass\n\n    def keliling(self):\n        pass\n\nl = Lingkaran(10)\nprint(l.luas())\nprint(l.keliling())\n",
            "contoh_input":  "",
            "contoh_output": "314.0\n62.8",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
        {
            "judul":         "Tangkap Error Pembagian",
            "deskripsi":     "Buat fungsi bagi(a, b) yang mengembalikan hasil a/b. Jika b=0, tangkap error dan tampilkan 'Error: tidak bisa dibagi nol'. Uji dengan bagi(10,2) dan bagi(5,0).",
            "kode_awal":     "def bagi(a, b):\n    try:\n        pass\n    except ZeroDivisionError:\n        pass\n\nprint(bagi(10, 2))\nprint(bagi(5, 0))\n",
            "contoh_input":  "",
            "contoh_output": "5.0\nError: tidak bisa dibagi nol",
            "tingkat":       "menengah",
            "xp_reward":     25,
        },
    ]

    berhasil = 0
    for i, ch in enumerate(challenges, start=1):
        try:
            cur.execute("""
                INSERT INTO challenges
                    (judul, deskripsi, kode_awal, contoh_input, contoh_output,
                     tingkat, xp_reward, dipublikasi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
            """, (
                ch["judul"],
                ch["deskripsi"],
                ch["kode_awal"],
                ch["contoh_input"],
                ch["contoh_output"],
                ch["tingkat"],
                ch["xp_reward"],
            ))
            berhasil += 1
            print(f"  🔒 [{i:02d}] {ch['judul']}")
        except Exception as e:
            print(f"  ❌ [{i:02d}] {ch['judul']}: {e}")

    conn.commit()
    conn.close()
    print(f"""
🎉 Selesai! {berhasil}/{len(challenges)} tantangan extra berhasil ditambahkan.

📋 Semua tersembunyi (dipublikasi = 0).

💡 Cara publish sesuai jadwal pelajaran:
   - Setelah Pelajaran 1-5   selesai → Publish tantangan extra 1-8
   - Setelah Pelajaran 6-10  selesai → Publish tantangan extra 9-16
   - Setelah Pelajaran 11-15 selesai → Publish tantangan extra 17-24
   - Setelah Pelajaran 16-20 selesai → Publish tantangan extra 25-32
""")

if __name__ == "__main__":
    print("⚡ Menambahkan 32 tantangan extra (sesuai pelajaran)...\n")
    seed_challenges_extra()

