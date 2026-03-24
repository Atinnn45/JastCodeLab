"""
JastCodeLab — Seed Data Pelajaran Python
=========================================
Jalankan file ini sekali untuk mengisi tabel lessons:
    python seed_lessons.py

20 Pelajaran dengan urutan & tingkat kesulitan meningkat:
 1-5  : Variabel
 6-10 : Tipe Data
11-15 : Input & Output
16-20 : Topik Lanjutan (if/else, for, while, fungsi, string, list, dict, OOP, error handling)
"""

from database import get_db
from datetime import datetime

def seed_lessons():
    conn = get_db()
    cur  = conn.cursor()

    lessons = [

        # ══════════════════════════════════════════
        # BAGIAN 1 — VARIABEL (Pelajaran 1-5)
        # ══════════════════════════════════════════

        {
            "judul":   "Mengenal Variabel di Python",
            "deskripsi": "Variabel adalah tempat untuk menyimpan data. Di Python, kamu tidak perlu mendeklarasikan tipe data secara eksplisit.",
            "konten": """# Mengenal Variabel di Python

## Apa itu Variabel?

Variabel adalah **wadah** untuk menyimpan nilai. Bayangkan variabel seperti sebuah kotak bernama, di mana kamu bisa menaruh nilai di dalamnya dan menggunakannya kapan saja.

## Cara Membuat Variabel

Di Python, membuat variabel sangat mudah — cukup tulis nama variabel, tanda `=`, lalu nilainya:

```python
nama = "Jastin"
umur = 17
tinggi = 165.5
```

## Aturan Penamaan Variabel

- Nama variabel **tidak boleh** dimulai dengan angka
- Nama variabel **boleh** mengandung huruf, angka, dan underscore `_`
- Nama variabel **bersifat case-sensitive** (huruf besar dan kecil berbeda)
- Hindari menggunakan kata kunci Python seperti `if`, `for`, `while`, dll.

```python
# ✅ Nama variabel yang valid
nama_user = "Budi"
nilai1    = 90
_skor     = 100

# ❌ Nama variabel yang tidak valid
1nama  = "salah"   # dimulai dengan angka
my-var = "salah"   # menggunakan tanda hubung
```

## Mencetak Nilai Variabel

Gunakan fungsi `print()` untuk menampilkan nilai variabel:

```python
nama = "Jastin"
print(nama)
```

## Multiple Assignment

Python memungkinkan kamu memberi nilai ke beberapa variabel sekaligus:

```python
x = y = z = 0          # semua bernilai 0
a, b, c = 1, 2, 3      # a=1, b=2, c=3
```
""",
            "kode_contoh": """nama = "Jastin"
umur = 17
tinggi = 165.5

print("Nama   :", nama)
print("Umur   :", umur)
print("Tinggi :", tinggi)

# Multiple assignment
x, y, z = 10, 20, 30
print("x =", x, "| y =", y, "| z =", z)""",
            "output_contoh": """Nama   : Jastin
Umur   : 17
Tinggi : 165.5
x = 10 | y = 20 | z = 30""",
            "xp_reward": 10, "urutan": 1,
        },

        {
            "judul":   "Mengubah Nilai Variabel",
            "deskripsi": "Nilai variabel di Python bisa diubah kapan saja. Pelajari cara memperbarui dan menukar nilai variabel.",
            "konten": """# Mengubah Nilai Variabel

## Nilai Variabel Bisa Berubah

Di Python, variabel bersifat **dinamis** — artinya nilainya bisa diubah kapan saja, bahkan tipenya pun bisa berubah!

```python
skor = 100
print(skor)   # 100

skor = 200    # nilai diperbarui
print(skor)   # 200

skor = "Sempurna"   # tipe berubah dari int ke str
print(skor)         # Sempurna
```

## Operator Penugasan

Python menyediakan operator penugasan singkat untuk memperbarui nilai variabel:

| Operator | Contoh      | Setara dengan  |
|----------|-------------|----------------|
| `+=`     | `x += 5`    | `x = x + 5`    |
| `-=`     | `x -= 3`    | `x = x - 3`    |
| `*=`     | `x *= 2`    | `x = x * 2`    |
| `/=`     | `x /= 4`    | `x = x / 4`    |

```python
poin = 50
poin += 25    # poin sekarang 75
poin -= 10    # poin sekarang 65
poin *= 2     # poin sekarang 130
print(poin)   # 130
```

## Menukar Nilai Dua Variabel

Di Python, menukar nilai dua variabel bisa dilakukan dalam satu baris:

```python
a = 5
b = 10
a, b = b, a   # swap!
print(a, b)   # 10 5
```
""",
            "kode_contoh": """# Memperbarui nilai variabel
poin = 50
print("Awal  :", poin)

poin += 25
print("Setelah +25 :", poin)

poin *= 2
print("Setelah x2  :", poin)

# Menukar dua variabel
a, b = 5, 10
print("Sebelum swap: a =", a, ", b =", b)
a, b = b, a
print("Setelah swap: a =", a, ", b =", b)""",
            "output_contoh": """Awal  : 50
Setelah +25 : 75
Setelah x2  : 150
Sebelum swap: a = 5 , b = 10
Setelah swap: a = 10 , b = 5""",
            "xp_reward": 10, "urutan": 2,
        },

        {
            "judul":   "Variabel Global dan Lokal",
            "deskripsi": "Pahami perbedaan variabel yang dibuat di dalam dan di luar fungsi, serta cara menggunakannya dengan benar.",
            "konten": """# Variabel Global dan Lokal

## Variabel Lokal

Variabel yang dibuat **di dalam fungsi** disebut variabel **lokal**. Variabel ini hanya bisa diakses di dalam fungsi tersebut.

```python
def sapa():
    pesan = "Halo!"   # variabel lokal
    print(pesan)

sapa()
# print(pesan)   # ❌ Error! 'pesan' tidak dikenal di luar fungsi
```

## Variabel Global

Variabel yang dibuat **di luar fungsi** disebut variabel **global**. Variabel ini bisa diakses dari mana saja.

```python
nama = "Python"   # variabel global

def cetak_nama():
    print(nama)   # bisa diakses

cetak_nama()   # Python
```

## Keyword `global`

Jika ingin **mengubah** variabel global dari dalam fungsi, gunakan keyword `global`:

```python
counter = 0

def tambah():
    global counter
    counter += 1

tambah()
tambah()
print(counter)   # 2
```

## Prioritas Variabel

Jika ada variabel lokal dan global dengan nama sama, variabel **lokal** yang diutamakan di dalam fungsi:

```python
x = "global"

def test():
    x = "lokal"
    print(x)   # lokal

test()
print(x)   # global
```
""",
            "kode_contoh": """# Contoh variabel global vs lokal
skor_total = 0   # global

def tambah_skor(nilai):
    global skor_total
    skor_total += nilai
    bonus = nilai * 0.1   # variabel lokal
    print(f"  Bonus lokal: {bonus}")

tambah_skor(100)
tambah_skor(200)
print("Skor total:", skor_total)""",
            "output_contoh": """  Bonus lokal: 10.0
  Bonus lokal: 20.0
Skor total: 300""",
            "xp_reward": 15, "urutan": 3,
        },

        {
            "judul":   "Konstanta dan Konvensi Penamaan",
            "deskripsi": "Pelajari cara memberi nama variabel yang baik dan konsep konstanta di Python.",
            "konten": """# Konstanta dan Konvensi Penamaan

## Konvensi Penamaan Python (PEP 8)

Python memiliki panduan penamaan resmi yang disebut **PEP 8**:

| Jenis        | Konvensi          | Contoh                  |
|--------------|-------------------|-------------------------|
| Variabel     | `snake_case`      | `nama_lengkap`, `skor`  |
| Fungsi       | `snake_case`      | `hitung_luas()`         |
| Konstanta    | `UPPER_CASE`      | `MAX_NILAI`, `PI`       |
| Class        | `PascalCase`      | `MobilBalap`            |

## Konstanta

Python tidak punya tipe konstanta bawaan, tapi **konvensi** menggunakan huruf besar semua untuk menandai nilai yang tidak boleh diubah:

```python
PI            = 3.14159
MAX_PERCOBAAN = 3
WARNA_MERAH   = "#FF0000"
```

## Nama Deskriptif vs Singkatan

Selalu utamakan nama yang **deskriptif** agar kode mudah dibaca:

```python
# ❌ Kurang deskriptif
x  = 85
n  = "Budi"
hs = 100

# ✅ Deskriptif dan jelas
nilai_ujian  = 85
nama_siswa   = "Budi"
nilai_maks   = 100
```
""",
            "kode_contoh": """# Konstanta program
GRAVITASI     = 9.8
KECEPATAN_MAX = 300_000   # bisa pakai underscore untuk keterbacaan
NAMA_APP      = "JastCodeLab"

# Menghitung berat benda di bumi
massa_benda = 10   # kg
berat       = massa_benda * GRAVITASI

print(f"Aplikasi  : {NAMA_APP}")
print(f"Massa     : {massa_benda} kg")
print(f"Gravitasi : {GRAVITASI} m/s²")
print(f"Berat     : {berat} N")""",
            "output_contoh": """Aplikasi  : JastCodeLab
Massa     : 10 kg
Gravitasi : 9.8 m/s²
Berat     : 98.0 N""",
            "xp_reward": 15, "urutan": 4,
        },

        {
            "judul":   "Variabel dan Ekspresi",
            "deskripsi": "Gunakan variabel dalam ekspresi matematika dan logika untuk membuat program yang lebih dinamis.",
            "konten": """# Variabel dan Ekspresi

## Ekspresi Matematika

Variabel bisa digunakan dalam operasi matematika:

| Operator | Keterangan       | Contoh    | Hasil |
|----------|------------------|-----------|-------|
| `+`      | Penjumlahan      | `5 + 3`   | 8     |
| `-`      | Pengurangan      | `10 - 4`  | 6     |
| `*`      | Perkalian        | `3 * 4`   | 12    |
| `/`      | Pembagian        | `10 / 3`  | 3.333 |
| `//`     | Pembagian bulat  | `10 // 3` | 3     |
| `%`      | Sisa bagi        | `10 % 3`  | 1     |
| `**`     | Pangkat          | `2 ** 8`  | 256   |

## Prioritas Operator

Python mengikuti aturan matematika: **PEMDAS** (Pangkat → Kali/Bagi → Tambah/Kurang):

```python
hasil = 2 + 3 * 4       # 14 (bukan 20!)
hasil = (2 + 3) * 4     # 20 (kurung dulu)
```

## Ekspresi dalam Variabel

```python
panjang = 8
lebar   = 5
luas    = panjang * lebar
keliling = 2 * (panjang + lebar)
```
""",
            "kode_contoh": """# Kalkulator nilai akhir
nilai_tugas = 85
nilai_uts   = 78
nilai_uas   = 90

# Bobot penilaian
bobot_tugas = 0.30
bobot_uts   = 0.30
bobot_uas   = 0.40

nilai_akhir = (nilai_tugas * bobot_tugas +
               nilai_uts   * bobot_uts   +
               nilai_uas   * bobot_uas)

print(f"Nilai Tugas : {nilai_tugas} (bobot 30%)")
print(f"Nilai UTS   : {nilai_uts} (bobot 30%)")
print(f"Nilai UAS   : {nilai_uas} (bobot 40%)")
print(f"Nilai Akhir : {nilai_akhir:.1f}")""",
            "output_contoh": """Nilai Tugas : 85 (bobot 30%)
Nilai UTS   : 78 (bobot 30%)
Nilai UAS   : 90 (bobot 40%)
Nilai Akhir : 84.9""",
            "xp_reward": 15, "urutan": 5,
        },

        # ══════════════════════════════════════════
        # BAGIAN 2 — TIPE DATA (Pelajaran 6-10)
        # ══════════════════════════════════════════

        {
            "judul":   "Tipe Data Integer dan Float",
            "deskripsi": "Pelajari tipe data angka di Python: integer untuk bilangan bulat dan float untuk bilangan desimal.",
            "konten": """# Tipe Data Integer dan Float

## Integer (int)

Integer adalah bilangan **bulat** tanpa desimal, bisa positif, negatif, atau nol:

```python
umur     = 17
suhu     = -5
populasi = 1_000_000   # underscore untuk keterbacaan
print(type(umur))      # <class 'int'>
```

## Float

Float adalah bilangan **desimal**:

```python
pi      = 3.14159
suhu    = -2.5
persen  = 0.85
print(type(pi))   # <class 'float'>
```

## Konversi Antar Tipe

```python
x = 10
y = float(x)    # int → float: 10.0
z = int(3.9)    # float → int: 3 (bukan 4! selalu bulatkan ke bawah)
```

## Operasi Khusus

```python
# Pembagian selalu menghasilkan float
print(10 / 2)    # 5.0 (bukan 5)
print(10 // 3)   # 3   (pembagian bulat)
print(10 % 3)    # 1   (sisa bagi / modulo)
print(2 ** 10)   # 1024 (pangkat)
```

## Nilai Maksimum

Python tidak punya batas maksimum untuk integer — bisa sebesar apapun!

```python
besar = 10 ** 100   # googol! Python bisa menanganinya
print(besar)
```
""",
            "kode_contoh": """# Konversi suhu Celsius ke Fahrenheit
suhu_celsius = 37.5
suhu_fahrenheit = (suhu_celsius * 9/5) + 32

print(f"Suhu      : {suhu_celsius}°C")
print(f"Fahrenheit: {suhu_fahrenheit}°F")
print(f"Tipe C    : {type(suhu_celsius)}")
print(f"Tipe F    : {type(suhu_fahrenheit)}")

# Pembagian bulat dan modulo
detik_total = 3723
jam    = detik_total // 3600
menit  = (detik_total % 3600) // 60
detik  = detik_total % 60
print(f"\\n{detik_total} detik = {jam}j {menit}m {detik}d")""",
            "output_contoh": """Suhu      : 37.5°C
Fahrenheit: 99.5°F
Tipe C    : <class 'float'>
Tipe F    : <class 'float'>

3723 detik = 1j 2m 3d""",
            "xp_reward": 15, "urutan": 6,
        },

        {
            "judul":   "Tipe Data String",
            "deskripsi": "String adalah tipe data untuk teks. Pelajari cara membuat, menggabungkan, dan memanipulasi string di Python.",
            "konten": """# Tipe Data String

## Membuat String

String dibuat dengan tanda kutip tunggal `'` atau ganda `"`:

```python
nama    = "Python"
kalimat = 'Belajar coding itu seru!'
panjang = len(nama)   # 6
```

## Multiline String

Untuk teks panjang lebih dari satu baris, gunakan tiga tanda kutip:

```python
teks = \"\"\"
Baris pertama
Baris kedua
Baris ketiga
\"\"\"
```

## Indexing dan Slicing

```python
kata = "Python"
print(kata[0])     # P  (indeks pertama = 0)
print(kata[-1])    # n  (indeks terakhir = -1)
print(kata[0:3])   # Pyt
print(kata[::2])   # Pto (setiap 2 karakter)
print(kata[::-1])  # nohtyP (dibalik)
```

## Operasi String

```python
s1 = "Hello"
s2 = "World"
print(s1 + " " + s2)   # Hello World (concatenation)
print(s1 * 3)           # HelloHelloHello (repetition)
```

## f-String (Format String)

Cara modern untuk menyisipkan variabel ke dalam string:

```python
nama  = "Budi"
nilai = 95
print(f"Nama: {nama}, Nilai: {nilai}")
print(f"Nilai kamu: {nilai:.2f}")   # 2 angka desimal
```
""",
            "kode_contoh": """teks = "JastCodeLab"

print("Teks asli  :", teks)
print("Panjang    :", len(teks))
print("Huruf besar:", teks.upper())
print("Huruf kecil:", teks.lower())
print("4 huruf pertama:", teks[:4])
print("4 huruf terakhir:", teks[-4:])
print("Dibalik    :", teks[::-1])

# f-string
nama  = "Jastin"
skor  = 9850
print(f"\\nPemain: {nama}")
print(f"Skor  : {skor:,}")   # format ribuan""",
            "output_contoh": """Teks asli  : JastCodeLab
Panjang    : 11
Huruf besar: JASTCODELAB
Huruf kecil: jastcodelab
4 huruf pertama: Jast
4 huruf terakhir: eLab
Dibalik    : baLedoCtsaJ

Pemain: Jastin
Skor  : 9,850""",
            "xp_reward": 15, "urutan": 7,
        },

        {
            "judul":   "Tipe Data Boolean",
            "deskripsi": "Boolean hanya memiliki dua nilai: True atau False. Tipe data ini sangat penting untuk logika dan kondisi program.",
            "konten": """# Tipe Data Boolean

## Apa itu Boolean?

Boolean adalah tipe data yang hanya punya **dua nilai**: `True` atau `False`.

```python
aktif     = True
selesai   = False
print(type(aktif))   # <class 'bool'>
```

## Operator Perbandingan

Operator perbandingan menghasilkan nilai Boolean:

| Operator | Arti                  | Contoh    | Hasil   |
|----------|-----------------------|-----------|---------|
| `==`     | Sama dengan           | `5 == 5`  | `True`  |
| `!=`     | Tidak sama dengan     | `5 != 3`  | `True`  |
| `>`      | Lebih besar           | `5 > 3`   | `True`  |
| `<`      | Lebih kecil           | `5 < 3`   | `False` |
| `>=`     | Lebih besar atau sama | `5 >= 5`  | `True`  |
| `<=`     | Lebih kecil atau sama | `5 <= 4`  | `False` |

## Operator Logika

| Operator | Keterangan                        |
|----------|-----------------------------------|
| `and`    | True jika **keduanya** True       |
| `or`     | True jika **salah satu** True     |
| `not`    | Membalik nilai Boolean            |

```python
print(True and False)   # False
print(True or False)    # True
print(not True)         # False
```

## Nilai Falsy dan Truthy

Nilai berikut dianggap `False` oleh Python:
- `0`, `0.0` — angka nol
- `""` — string kosong
- `[]`, `{}`, `()` — koleksi kosong
- `None`

Semua nilai lainnya dianggap `True`.
""",
            "kode_contoh": """nilai = 75
lulus_kkm  = nilai >= 70
nilai_a    = nilai >= 90

print(f"Nilai       : {nilai}")
print(f"Lulus KKM   : {lulus_kkm}")
print(f"Dapat Nilai A: {nilai_a}")

# Operator logika
hadir  = True
tugas_kumpul = True
bisa_ikut_ujian = hadir and tugas_kumpul
print(f"\\nBisa ikut ujian: {bisa_ikut_ujian}")

# Falsy vs Truthy
print(f"\\nbool(0)   = {bool(0)}")
print(f"bool(1)   = {bool(1)}")
print(f"bool('') = {bool('')}")
print(f"bool('a') = {bool('a')}")""",
            "output_contoh": """Nilai       : 75
Lulus KKM   : True
Dapat Nilai A: False

Bisa ikut ujian: True

bool(0)   = False
bool(1)   = True
bool('') = False
bool('a') = True""",
            "xp_reward": 15, "urutan": 8,
        },

        {
            "judul":   "Tipe Data List",
            "deskripsi": "List adalah koleksi data yang berurutan dan bisa diubah. Ini adalah salah satu tipe data paling sering digunakan di Python.",
            "konten": """# Tipe Data List

## Membuat List

List dibuat dengan tanda kurung siku `[]` dan bisa berisi tipe data apapun:

```python
buah    = ["apel", "mangga", "jeruk"]
angka   = [1, 2, 3, 4, 5]
campur  = [1, "dua", 3.0, True]
kosong  = []
```

## Mengakses Elemen

```python
buah = ["apel", "mangga", "jeruk"]
print(buah[0])    # apel    (indeks pertama)
print(buah[-1])   # jeruk   (indeks terakhir)
print(buah[1:3])  # ['mangga', 'jeruk']
```

## Mengubah, Menambah, Menghapus

```python
buah = ["apel", "mangga"]

buah[0]  = "semangka"   # ubah elemen
buah.append("pisang")   # tambah di akhir
buah.insert(1, "nanas") # sisipkan di indeks 1
buah.remove("mangga")   # hapus berdasarkan nilai
buah.pop()              # hapus elemen terakhir
buah.pop(0)             # hapus elemen indeks 0
```

## Operasi List

```python
a = [1, 2, 3]
b = [4, 5, 6]
print(a + b)        # [1, 2, 3, 4, 5, 6]
print(a * 2)        # [1, 2, 3, 1, 2, 3]
print(len(a))       # 3
print(3 in a)       # True
print(sorted(a, reverse=True))  # [3, 2, 1]
```
""",
            "kode_contoh": """# Daftar nilai siswa
nilai = [85, 92, 78, 95, 88, 70]

print("Daftar nilai :", nilai)
print("Jumlah siswa :", len(nilai))
print("Nilai tertinggi:", max(nilai))
print("Nilai terendah :", min(nilai))
print("Rata-rata      :", sum(nilai) / len(nilai))

# Tambah nilai baru
nilai.append(99)
print("\\nSetelah tambah 99:", nilai)

# Urutkan
nilai.sort()
print("Setelah diurutkan:", nilai)

# 3 nilai teratas
print("3 nilai teratas  :", nilai[-3:])""",
            "output_contoh": """Daftar nilai : [85, 92, 78, 95, 88, 70]
Jumlah siswa : 6
Nilai tertinggi: 95
Nilai terendah : 70
Rata-rata      : 84.66666666666667

Setelah tambah 99: [85, 92, 78, 95, 88, 70, 99]
Setelah diurutkan: [70, 78, 85, 88, 92, 95, 99]
3 nilai teratas  : [92, 95, 99]""",
            "xp_reward": 20, "urutan": 9,
        },

        {
            "judul":   "Tipe Data Dictionary",
            "deskripsi": "Dictionary menyimpan data dalam format key-value. Sangat berguna untuk merepresentasikan data terstruktur seperti data pengguna atau konfigurasi.",
            "konten": """# Tipe Data Dictionary

## Membuat Dictionary

Dictionary dibuat dengan kurung kurawal `{}` dalam format `key: value`:

```python
mahasiswa = {
    "nama"  : "Budi",
    "umur"  : 20,
    "jurusan": "Informatika"
}
```

## Mengakses dan Mengubah Data

```python
# Akses nilai
print(mahasiswa["nama"])          # Budi
print(mahasiswa.get("umur", 0))  # 20 (0 jika key tidak ada)

# Ubah nilai
mahasiswa["umur"] = 21

# Tambah key baru
mahasiswa["ipk"] = 3.85

# Hapus
del mahasiswa["jurusan"]
nilai = mahasiswa.pop("ipk")   # hapus dan ambil nilainya
```

## Iterasi Dictionary

```python
for key in mahasiswa:
    print(key, ":", mahasiswa[key])

for key, value in mahasiswa.items():
    print(f"{key} = {value}")
```

## Method Penting

```python
d = {"a": 1, "b": 2, "c": 3}
print(d.keys())    # dict_keys(['a', 'b', 'c'])
print(d.values())  # dict_values([1, 2, 3])
print(d.items())   # dict_items([('a',1), ('b',2), ('c',3)])
print("a" in d)    # True
```
""",
            "kode_contoh": """# Data profil pengguna
profil = {
    "username": "jastin17",
    "level"   : 5,
    "xp"      : 1250,
    "badge"   : ["Pemula", "Rajin Belajar"],
    "aktif"   : True
}

print("=== Profil Pengguna ===")
for key, value in profil.items():
    print(f"  {key:10}: {value}")

# Update XP dan level
profil["xp"] += 150
if profil["xp"] >= 1400:
    profil["level"] = 6

print(f"\\nSetelah belajar:")
print(f"  XP baru : {profil['xp']}")
print(f"  Level   : {profil['level']}")""",
            "output_contoh": """=== Profil Pengguna ===
  username  : jastin17
  level     : 5
  xp        : 1250
  badge     : ['Pemula', 'Rajin Belajar']
  aktif     : True

Setelah belajar:
  XP baru : 1400
  Level   : 6""",
            "xp_reward": 20, "urutan": 10,
        },

        # ══════════════════════════════════════════
        # BAGIAN 3 — INPUT & OUTPUT (Pelajaran 11-15)
        # ══════════════════════════════════════════

        {
            "judul":   "Input dari Pengguna",
            "deskripsi": "Buat program interaktif dengan menerima input dari pengguna menggunakan fungsi input().",
            "konten": """# Input dari Pengguna

## Fungsi input()

Fungsi `input()` digunakan untuk menerima input dari pengguna. Input selalu berupa **string**!

```python
nama = input("Masukkan nama kamu: ")
print("Halo,", nama)
```

## Konversi Tipe Input

Karena `input()` selalu mengembalikan string, kamu perlu mengkonversinya jika butuh angka:

```python
umur   = int(input("Masukkan umur: "))
tinggi = float(input("Masukkan tinggi (cm): "))
```

## Validasi Input Sederhana

```python
teks = input("Masukkan angka: ")
if teks.isdigit():
    angka = int(teks)
    print("Angkamu:", angka)
else:
    print("Itu bukan angka!")
```

## Input Multiple Nilai

```python
# Masukkan dua angka dipisah spasi: 10 20
a, b = input("Masukkan dua angka: ").split()
a, b = int(a), int(b)
print(f"{a} + {b} = {a + b}")
```
""",
            "kode_contoh": """# Simulasi input (diganti dengan nilai langsung untuk demo)
nama  = "Jastin"
umur  = 17
kota  = "Batam"

print(f"Nama  : {nama}")
print(f"Umur  : {umur} tahun")
print(f"Kota  : {kota}")
print()

# Konversi dan perhitungan
tahun_lahir = 2025 - umur
print(f"Kamu lahir sekitar tahun {tahun_lahir}")

# Cek apakah sudah dewasa
if umur >= 17:
    print("Kamu sudah bisa membuat KTP!")
else:
    sisa = 17 - umur
    print(f"Kamu perlu {sisa} tahun lagi untuk KTP.")""",
            "output_contoh": """Nama  : Jastin
Umur  : 17 tahun
Kota  : Batam

Kamu lahir sekitar tahun 2008
Kamu sudah bisa membuat KTP!""",
            "xp_reward": 20, "urutan": 11,
        },

        {
            "judul":   "Format Output dengan print()",
            "deskripsi": "Kuasai berbagai cara memformat output agar tampilannya rapi dan informatif.",
            "konten": """# Format Output dengan print()

## Parameter print()

Fungsi `print()` memiliki beberapa parameter berguna:

```python
print("Halo", "Dunia")              # Halo Dunia
print("Halo", "Dunia", sep="-")     # Halo-Dunia
print("Baris 1", end=" | ")
print("Baris 2")                    # Baris 1 | Baris 2
```

## f-String (Cara Modern)

```python
nama  = "Budi"
nilai = 95.5

print(f"Nama : {nama}")
print(f"Nilai: {nilai:.1f}")       # 1 angka desimal
print(f"Nilai: {nilai:08.2f}")     # 8 karakter, 2 desimal
print(f"Nama : {nama:>10}")        # rata kanan, 10 karakter
print(f"Nama : {nama:<10}|")       # rata kiri
print(f"Nama : {nama:^10}|")       # tengah
```

## Format Angka

```python
besar = 1_234_567.89
print(f"{besar:,.2f}")    # 1,234,567.89
print(f"{besar:e}")       # notasi ilmiah
print(f"{0.85:.0%}")      # 85% (persen)
```

## Karakter Escape

```python
print("Baris 1\\nBaris 2")   # newline
print("A\\tB\\tC")           # tab
print("Dia berkata \\"Halo\\"")  # tanda kutip
```
""",
            "kode_contoh": """# Laporan nilai siswa yang rapi
print("=" * 40)
print(f"{'LAPORAN NILAI SISWA':^40}")
print("=" * 40)

siswa = [
    ("Budi",    85, 90, 88),
    ("Sari",    92, 88, 95),
    ("Doni",    70, 75, 72),
    ("Mega",    98, 95, 97),
]

print(f"{'Nama':<10} {'Tugas':>6} {'UTS':>6} {'UAS':>6} {'Rata':>7}")
print("-" * 40)

for nama, tugas, uts, uas in siswa:
    rata = (tugas + uts + uas) / 3
    print(f"{nama:<10} {tugas:>6} {uts:>6} {uas:>6} {rata:>7.1f}")

print("=" * 40)""",
            "output_contoh": """========================================
           LAPORAN NILAI SISWA           
========================================
Nama        Tugas    UTS    UAS    Rata
----------------------------------------
Budi           85     90     88     87.7
Sari           92     88     95     91.7
Doni           70     75     72     72.3
Mega           98     95     97     96.7
========================================""",
            "xp_reward": 20, "urutan": 12,
        },

        {
            "judul":   "Kondisi if, elif, dan else",
            "deskripsi": "Buat program yang bisa membuat keputusan berdasarkan kondisi tertentu menggunakan if, elif, dan else.",
            "konten": """# Kondisi if, elif, dan else

## Struktur Dasar

```python
if kondisi:
    # kode jika kondisi True
elif kondisi_lain:
    # kode jika kondisi_lain True
else:
    # kode jika semua kondisi False
```

## Contoh Sederhana

```python
nilai = 85

if nilai >= 90:
    print("A")
elif nilai >= 80:
    print("B")
elif nilai >= 70:
    print("C")
else:
    print("D")
```

## Kondisi Bertingkat (Nested)

```python
umur   = 20
punya_ktp = True

if umur >= 17:
    if punya_ktp:
        print("Bisa memilih!")
    else:
        print("Perlu KTP dulu")
else:
    print("Belum cukup umur")
```

## Ternary Expression

Cara singkat untuk if-else sederhana:

```python
nilai = 85
status = "Lulus" if nilai >= 70 else "Tidak Lulus"
print(status)   # Lulus
```

## Operator in dan not in

```python
buah = ["apel", "mangga", "jeruk"]
if "apel" in buah:
    print("Apel ada!")
```
""",
            "kode_contoh": """def cek_bmi(berat, tinggi_cm):
    tinggi_m = tinggi_cm / 100
    bmi = berat / (tinggi_m ** 2)

    if bmi < 18.5:
        kategori = "Kurus"
    elif bmi < 25.0:
        kategori = "Normal"
    elif bmi < 30.0:
        kategori = "Kelebihan Berat"
    else:
        kategori = "Obesitas"

    return bmi, kategori

# Test beberapa kondisi
data = [(50, 165), (70, 170), (90, 168), (45, 175)]

print(f"{'Berat':>6} {'Tinggi':>7} {'BMI':>7} {'Kategori'}")
print("-" * 35)
for berat, tinggi in data:
    bmi, kat = cek_bmi(berat, tinggi)
    print(f"{berat:>6} {tinggi:>7} {bmi:>7.1f} {kat}")""",
            "output_contoh": """ Berat  Tinggi     BMI Kategori
-----------------------------------
    50     165    18.4 Kurus
    70     170    24.2 Normal
    90     168    31.9 Obesitas
    45     175    14.7 Kurus""",
            "xp_reward": 20, "urutan": 13,
        },

        {
            "judul":   "Perulangan for dan while",
            "deskripsi": "Gunakan perulangan untuk mengeksekusi kode berulang kali tanpa menulis kode yang sama berkali-kali.",
            "konten": """# Perulangan for dan while

## Perulangan for

`for` digunakan untuk iterasi melalui urutan (list, string, range, dll):

```python
for i in range(5):
    print(i)   # 0, 1, 2, 3, 4

buah = ["apel", "mangga", "jeruk"]
for b in buah:
    print(b)
```

## Fungsi range()

```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8
range(10, 0, -1) # 10, 9, ..., 1
```

## Perulangan while

`while` terus berjalan selama kondisi `True`:

```python
hitung = 1
while hitung <= 5:
    print(hitung)
    hitung += 1
```

## break dan continue

```python
for i in range(10):
    if i == 3:
        continue   # lewati i=3
    if i == 7:
        break      # hentikan loop
    print(i)
```

## enumerate() — indeks + nilai

```python
buah = ["apel", "mangga", "jeruk"]
for i, b in enumerate(buah, start=1):
    print(f"{i}. {b}")
```
""",
            "kode_contoh": """# Tabel perkalian
n = 5
print(f"Tabel Perkalian {n}")
print("-" * 25)
for i in range(1, 11):
    print(f"{n} x {i:2} = {n*i:3}")

# FizzBuzz klasik
print("\\nFizzBuzz 1-20:")
for i in range(1, 21):
    if i % 15 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")
print()""",
            "output_contoh": """Tabel Perkalian 5
-------------------------
5 x  1 =   5
5 x  2 =  10
5 x  3 =  15
5 x  4 =  20
5 x  5 =  25
5 x  6 =  30
5 x  7 =  35
5 x  8 =  40
5 x  9 =  45
5 x 10 =  50

FizzBuzz 1-20:
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz """,
            "xp_reward": 25, "urutan": 14,
        },

        {
            "judul":   "List Comprehension",
            "deskripsi": "List comprehension adalah cara Python yang elegan dan efisien untuk membuat list baru dari list yang sudah ada.",
            "konten": """# List Comprehension

## Sintaks Dasar

List comprehension memungkinkan kamu membuat list dalam satu baris:

```python
# Cara biasa
kuadrat = []
for i in range(1, 6):
    kuadrat.append(i ** 2)

# Dengan list comprehension
kuadrat = [i ** 2 for i in range(1, 6)]
# [1, 4, 9, 16, 25]
```

## Dengan Kondisi (Filter)

```python
angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Ambil hanya yang genap
genap = [x for x in angka if x % 2 == 0]
# [2, 4, 6, 8, 10]

# Kuadratkan yang ganjil saja
ganjil_kuadrat = [x**2 for x in angka if x % 2 != 0]
# [1, 9, 25, 49, 81]
```

## Transformasi String

```python
kata = ["python", "java", "javascript"]
besar = [k.upper() for k in kata]
# ['PYTHON', 'JAVA', 'JAVASCRIPT']

panjang = [len(k) for k in kata]
# [6, 4, 10]
```

## Dictionary Comprehension

```python
kuadrat = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```
""",
            "kode_contoh": """nilai = [85, 92, 45, 78, 95, 60, 88, 55, 70, 99]

# Nilai yang lulus (>= 70)
lulus = [n for n in nilai if n >= 70]

# Semua nilai dinaikkan 5 poin (maks 100)
nilai_baru = [min(n + 5, 100) for n in nilai]

# Kategori per nilai
kategori = ["A" if n >= 90 else "B" if n >= 80
            else "C" if n >= 70 else "D"
            for n in nilai]

print("Nilai asli  :", nilai)
print("Yang lulus  :", lulus)
print("Jumlah lulus:", len(lulus))
print("Nilai +5    :", nilai_baru)
print("Kategori    :", kategori)

# Rata-rata nilai yang lulus
rata = sum(lulus) / len(lulus)
print(f"Rata lulus  : {rata:.1f}")""",
            "output_contoh": """Nilai asli  : [85, 92, 45, 78, 95, 60, 88, 55, 70, 99]
Yang lulus  : [85, 92, 78, 95, 88, 70, 99]
Jumlah lulus: 7
Nilai +5    : [90, 97, 50, 83, 100, 65, 93, 60, 75, 100]
Kategori    : ['B', 'A', 'D', 'C', 'A', 'D', 'B', 'D', 'C', 'A']
Rata lulus  : 86.7""",
            "xp_reward": 25, "urutan": 15,
        },

        # ══════════════════════════════════════════
        # BAGIAN 4 — TOPIK LANJUTAN (Pelajaran 16-20)
        # ══════════════════════════════════════════

        {
            "judul":   "Fungsi di Python",
            "deskripsi": "Fungsi memungkinkan kamu mengelompokkan kode yang bisa digunakan ulang. Pelajari cara membuat dan menggunakan fungsi dengan efektif.",
            "konten": """# Fungsi di Python

## Mendefinisikan Fungsi

```python
def sapa(nama):
    print(f"Halo, {nama}!")

sapa("Budi")   # Halo, Budi!
```

## Return Value

```python
def tambah(a, b):
    return a + b

hasil = tambah(5, 3)
print(hasil)   # 8
```

## Default Parameter

```python
def sapa(nama, salam="Halo"):
    print(f"{salam}, {nama}!")

sapa("Budi")           # Halo, Budi!
sapa("Sari", "Hei")    # Hei, Sari!
```

## *args dan **kwargs

```python
def jumlahkan(*angka):
    return sum(angka)

print(jumlahkan(1, 2, 3, 4, 5))   # 15

def profil(**data):
    for k, v in data.items():
        print(f"{k}: {v}")

profil(nama="Budi", umur=20, kota="Jakarta")
```

## Lambda (Fungsi Anonim)

```python
kuadrat = lambda x: x ** 2
print(kuadrat(5))   # 25

# Sangat berguna dengan sorted/filter/map
angka = [5, 2, 8, 1, 9, 3]
urut  = sorted(angka, key=lambda x: -x)   # urutan terbalik
```
""",
            "kode_contoh": """def statistik(data):
    \"\"\"Hitung statistik dasar dari list angka.\"\"\"
    if not data:
        return None

    n      = len(data)
    total  = sum(data)
    rata   = total / n
    maks   = max(data)
    mins   = min(data)

    data_urut = sorted(data)
    if n % 2 == 0:
        median = (data_urut[n//2-1] + data_urut[n//2]) / 2
    else:
        median = data_urut[n//2]

    return {
        "jumlah" : n,
        "total"  : total,
        "rata"   : round(rata, 2),
        "median" : median,
        "maks"   : maks,
        "min"    : mins,
    }

nilai = [85, 92, 78, 95, 88, 70, 99, 65, 82, 91]
hasil = statistik(nilai)

print("=== Statistik Nilai ===")
for k, v in hasil.items():
    print(f"  {k:8}: {v}")""",
            "output_contoh": """=== Statistik Nilai ===
  jumlah  : 10
  total   : 845
  rata    : 84.5
  median  : 86.5
  maks    : 99
  min     : 65""",
            "xp_reward": 25, "urutan": 16,
        },

        {
            "judul":   "Manipulasi String Lanjutan",
            "deskripsi": "Kuasai berbagai method string Python untuk memproses dan memanipulasi teks secara efisien.",
            "konten": """# Manipulasi String Lanjutan

## Method String Penting

```python
s = "  Halo, Python World!  "

s.strip()           # hapus spasi di ujung
s.lstrip()          # hapus spasi di kiri
s.rstrip()          # hapus spasi di kanan
s.upper()           # HALO, PYTHON WORLD!
s.lower()           # halo, python world!
s.title()           # Halo, Python World!
s.replace("o", "0") # Hal0, Pyth0n W0rld!
s.split(", ")       # ['  Halo', 'Python World!  ']
s.startswith("  Ha")  # True
s.endswith("!  ")     # True
s.find("Python")      # 7 (indeks)
s.count("l")          # 3
```

## Join dan Split

```python
kata = ["Python", "Java", "Go"]
teks = ", ".join(kata)
print(teks)   # Python, Java, Go

baris = "apel,mangga,jeruk"
buah  = baris.split(",")
# ['apel', 'mangga', 'jeruk']
```

## String Formatting Lanjutan

```python
# Padding dan alignment
print(f"{'Nama':>15}: {'Nilai':>6}")
print(f"{'Budi':>15}: {85:>6}")

# Zero padding
print(f"{42:05d}")   # 00042

# Format tanggal manual
hari, bulan, tahun = 1, 3, 2025
print(f"{hari:02d}/{bulan:02d}/{tahun}")   # 01/03/2025
```
""",
            "kode_contoh": """def analisis_teks(teks):
    kata_list = teks.lower().split()
    jumlah_kata  = len(kata_list)
    jumlah_huruf = sum(len(k) for k in kata_list)
    jumlah_unik  = len(set(kata_list))

    # Kata terpanjang
    terpanjang = max(kata_list, key=len)

    # Frekuensi kata
    frekuensi = {}
    for kata in kata_list:
        frekuensi[kata] = frekuensi.get(kata, 0) + 1
    kata_terbanyak = max(frekuensi, key=frekuensi.get)

    return jumlah_kata, jumlah_huruf, jumlah_unik, terpanjang, kata_terbanyak, frekuensi[kata_terbanyak]

kalimat = "belajar python itu seru belajar coding setiap hari membuat kamu semakin pintar"
jk, jh, ju, tp, ktb, frek = analisis_teks(kalimat)

print(f"Jumlah kata  : {jk}")
print(f"Jumlah huruf : {jh}")
print(f"Kata unik    : {ju}")
print(f"Kata terpanjang: {tp}")
print(f"Kata terbanyak : '{ktb}' ({frek}x)")""",
            "output_contoh": """Jumlah kata  : 14
Jumlah huruf : 87
Kata unik    : 13
Kata terpanjang: membuat
Kata terbanyak : 'belajar' (2x)""",
            "xp_reward": 25, "urutan": 17,
        },

        {
            "judul":   "OOP — Class dan Object",
            "deskripsi": "Object-Oriented Programming (OOP) adalah paradigma pemrograman yang mengorganisir kode ke dalam objek. Pelajari cara membuat class dan object di Python.",
            "konten": """# OOP — Class dan Object

## Apa itu Class dan Object?

- **Class** adalah blueprint/cetakan
- **Object** adalah instance dari class (hasil cetakan)

```python
class Kucing:
    def __init__(self, nama, warna):
        self.nama  = nama
        self.warna = warna

    def bersuara(self):
        print(f"{self.nama} berkata: Meow!")

# Membuat object
kucing1 = Kucing("Whisker", "putih")
kucing2 = Kucing("Tom", "abu-abu")

kucing1.bersuara()   # Whisker berkata: Meow!
print(kucing2.warna) # abu-abu
```

## `__init__` (Constructor)

`__init__` dipanggil otomatis saat object dibuat. `self` merujuk ke object itu sendiri.

## Encapsulation

```python
class RekeningBank:
    def __init__(self, saldo_awal):
        self.__saldo = saldo_awal   # private (__)

    def setor(self, jumlah):
        self.__saldo += jumlah

    def tarik(self, jumlah):
        if jumlah <= self.__saldo:
            self.__saldo -= jumlah
        else:
            print("Saldo tidak cukup!")

    def cek_saldo(self):
        return self.__saldo
```

## Inheritance (Pewarisan)

```python
class Hewan:
    def __init__(self, nama):
        self.nama = nama

    def bernapas(self):
        print(f"{self.nama} bernapas")

class Anjing(Hewan):   # mewarisi Hewan
    def menggonggong(self):
        print(f"{self.nama}: Guk guk!")
```
""",
            "kode_contoh": """class Mahasiswa:
    jumlah = 0   # class variable

    def __init__(self, nama, nim):
        self.nama  = nama
        self.nim   = nim
        self.nilai = []
        Mahasiswa.jumlah += 1

    def tambah_nilai(self, nilai):
        self.nilai.append(nilai)

    def rata_nilai(self):
        if not self.nilai:
            return 0
        return sum(self.nilai) / len(self.nilai)

    def __str__(self):
        return f"{self.nim} - {self.nama} (IPK: {self.rata_nilai():.2f})"

m1 = Mahasiswa("Budi Santoso", "2024001")
m2 = Mahasiswa("Sari Dewi",   "2024002")

m1.tambah_nilai(85); m1.tambah_nilai(90); m1.tambah_nilai(88)
m2.tambah_nilai(92); m2.tambah_nilai(95); m2.tambah_nilai(97)

print(m1)
print(m2)
print(f"Total mahasiswa: {Mahasiswa.jumlah}")""",
            "output_contoh": """2024001 - Budi Santoso (IPK: 87.67)
2024002 - Sari Dewi (IPK: 94.67)
Total mahasiswa: 2""",
            "xp_reward": 30, "urutan": 18,
        },

        {
            "judul":   "Error Handling dengan try/except",
            "deskripsi": "Program yang baik bisa menangani error dengan elegan. Pelajari cara menggunakan try/except untuk membuat program yang lebih robust.",
            "konten": """# Error Handling dengan try/except

## Mengapa Error Handling Penting?

Tanpa error handling, program akan berhenti tiba-tiba saat ada error. Dengan `try/except`, kita bisa menanganinya dengan elegan.

## Sintaks Dasar

```python
try:
    angka = int(input("Masukkan angka: "))
    hasil = 10 / angka
    print(f"Hasil: {hasil}")
except ValueError:
    print("Itu bukan angka!")
except ZeroDivisionError:
    print("Tidak bisa dibagi nol!")
```

## finally dan else

```python
try:
    f = open("file.txt")
    data = f.read()
except FileNotFoundError:
    print("File tidak ditemukan!")
else:
    print("File berhasil dibaca:", data)   # hanya jika tidak ada error
finally:
    print("Blok ini selalu dijalankan")    # selalu dijalankan
```

## Exception Umum di Python

| Exception            | Penyebab                        |
|----------------------|---------------------------------|
| `ValueError`         | Konversi tipe yang tidak valid  |
| `TypeError`          | Operasi pada tipe yang salah    |
| `IndexError`         | Indeks di luar batas            |
| `KeyError`           | Key tidak ada di dictionary     |
| `ZeroDivisionError`  | Pembagian dengan nol            |
| `FileNotFoundError`  | File tidak ditemukan            |

## Raise Exception

```python
def bagi(a, b):
    if b == 0:
        raise ValueError("Pembagi tidak boleh nol!")
    return a / b
```
""",
            "kode_contoh": """def konversi_nilai(nilai_str):
    \"\"\"Konversi string ke nilai dengan validasi.\"\"\"
    try:
        nilai = float(nilai_str)
        if not (0 <= nilai <= 100):
            raise ValueError(f"Nilai {nilai} di luar rentang 0-100")
        return nilai
    except ValueError as e:
        print(f"  ❌ Error: {e}")
        return None

def hitung_rata(nilai_list):
    try:
        if not nilai_list:
            raise ValueError("List nilai kosong!")
        return sum(nilai_list) / len(nilai_list)
    except TypeError:
        print("  ❌ Semua elemen harus berupa angka!")
        return None

# Test berbagai kasus
test_input = ["85", "abc", "110", "90", "75"]
print("Proses input nilai:")
valid = []
for v in test_input:
    n = konversi_nilai(v)
    if n is not None:
        valid.append(n)
        print(f"  ✅ {v} → {n}")

rata = hitung_rata(valid)
print(f"\\nNilai valid: {valid}")
print(f"Rata-rata  : {rata:.1f}")""",
            "output_contoh": """Proses input nilai:
  ✅ 85 → 85.0
  ❌ Error: could not convert string to float: 'abc'
  ❌ Error: Nilai 110.0 di luar rentang 0-100
  ✅ 90 → 90.0
  ✅ 75 → 75.0

Nilai valid: [85.0, 90.0, 75.0]
Rata-rata  : 83.3""",
            "xp_reward": 30, "urutan": 19,
        },

        {
            "judul":   "Modul dan Library Python",
            "deskripsi": "Python memiliki ribuan library siap pakai. Pelajari cara menggunakan modul bawaan Python dan cara mengorganisir kode ke dalam modul sendiri.",
            "konten": """# Modul dan Library Python

## Import Modul

```python
import math
import random
import datetime

print(math.pi)          # 3.141592...
print(math.sqrt(16))    # 4.0
print(math.floor(3.9))  # 3
```

## Import Spesifik

```python
from math import pi, sqrt, factorial
from random import randint, choice, shuffle

print(pi)           # tanpa math.
print(sqrt(25))     # 5.0
print(factorial(5)) # 120
```

## Modul random

```python
import random

print(random.randint(1, 10))          # angka acak 1-10
print(random.random())                # float 0.0 - 1.0
print(random.choice(["a","b","c"]))   # pilih acak dari list

angka = [1, 2, 3, 4, 5]
random.shuffle(angka)                 # acak urutan
print(angka)
```

## Modul datetime

```python
from datetime import datetime, date

sekarang = datetime.now()
print(sekarang.year)    # tahun
print(sekarang.month)   # bulan
print(sekarang.day)     # tanggal

hari_ini = date.today()
print(hari_ini)         # 2025-03-01
```

## Membuat Modul Sendiri

Simpan sebagai `kalkulator.py`:
```python
def tambah(a, b): return a + b
def kurang(a, b): return a - b
```

Lalu import:
```python
import kalkulator
print(kalkulator.tambah(5, 3))   # 8
```
""",
            "kode_contoh": """import math
import random
from datetime import datetime

# === Modul math ===
print("=== MATH ===")
print(f"pi      = {math.pi:.5f}")
print(f"e       = {math.e:.5f}")
print(f"sqrt(2) = {math.sqrt(2):.5f}")
print(f"log10(1000) = {math.log10(1000):.0f}")

# === Modul random ===
print("\\n=== RANDOM ===")
dadu1 = random.randint(1, 6)
dadu2 = random.randint(1, 6)
print(f"Dadu 1: {dadu1}, Dadu 2: {dadu2}, Total: {dadu1+dadu2}")

kartu = ["♠A","♥K","♦Q","♣J","♠10"]
random.shuffle(kartu)
print(f"Kartu dikocok: {kartu}")
print(f"Kartu dipilih: {random.choice(kartu)}")

# === datetime ===
print("\\n=== DATETIME ===")
now = datetime.now()
print(f"Sekarang: {now.strftime('%d %B %Y, %H:%M:%S')}") """,
            "output_contoh": """=== MATH ===
pi      = 3.14159
e       = 2.71828
sqrt(2) = 1.41421
log10(1000) = 3

=== RANDOM ===
Dadu 1: 4, Dadu 2: 2, Total: 6
Kartu dikocok: ['♣J', '♠A', '♦Q', '♥K', '♠10']
Kartu dipilih: ♦Q

=== DATETIME ===
Sekarang: 01 Maret 2025, 10:30:45""",
            "xp_reward": 30, "urutan": 20,
        },
    ]

    # Insert semua pelajaran
    berhasil = 0
    for lesson in lessons:
        try:
            cur.execute("""
                INSERT INTO lessons
                    (judul, deskripsi, konten, kode_contoh, output_contoh, xp_reward, urutan, dipublikasi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
            """, (
                lesson["judul"],
                lesson["deskripsi"],
                lesson["konten"],
                lesson["kode_contoh"],
                lesson["output_contoh"],
                lesson["xp_reward"],
                lesson["urutan"],
            ))
            berhasil += 1
            print(f"  ✅ [{lesson['urutan']:02d}] {lesson['judul']}")
        except Exception as e:
            print(f"  ❌ [{lesson['urutan']:02d}] {lesson['judul']}: {e}")

    conn.commit()
    conn.close()
    print(f"\n🎉 Selesai! {berhasil}/{len(lessons)} pelajaran berhasil ditambahkan.")


if __name__ == "__main__":
    print("📚 Menambahkan 20 pelajaran Python ke database...\n")
    seed_lessons()