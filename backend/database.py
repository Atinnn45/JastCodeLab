"""
JastCodeLab — Koneksi Database MySQL (PyMySQL)
==============================================
Step 1: Challenge Feedback + Streak + Level
Step 2: Coin + Badge + Shop
Step 3: Friend System
Step 4: Duel Challenge 1v1
Step 5: Daily Challenge
"""

import pymysql
import pymysql.cursors
import os

DB_NAME = os.environ.get("DB_NAME", "jastcodelab")

DB_CONFIG = {
    "host":        os.environ.get("DB_HOST",     "localhost"),
    "port":        int(os.environ.get("DB_PORT", "3306")),
    "user":        os.environ.get("DB_USER",     "root"),
    "password":    os.environ.get("DB_PASSWORD", ""),
    "database":    DB_NAME,
    "charset":     "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit":  False,
}

_DB_CONFIG_NO_DB = {k: v for k, v in DB_CONFIG.items() if k != "database"}


def _ensure_database_exists():
    try:
        conn = pymysql.connect(**_DB_CONFIG_NO_DB)
        cur  = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        conn.close()
        print(f"✅ Database '{DB_NAME}' siap digunakan.")
    except pymysql.err.OperationalError as e:
        raise RuntimeError(f"Gagal konek ke MySQL: {e}")


def get_db():
    try:
        return pymysql.connect(**DB_CONFIG)
    except pymysql.err.OperationalError as e:
        raise RuntimeError(f"Gagal konek ke database MySQL: {e}")


def init_db():
    _ensure_database_exists()
    conn = get_db()
    cur  = conn.cursor()

    # ── users ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id                  INT AUTO_INCREMENT PRIMARY KEY,
            username            VARCHAR(50)  NOT NULL UNIQUE,
            email               VARCHAR(100) NOT NULL UNIQUE,
            password_hash       VARCHAR(200) NOT NULL,
            xp                  INT          NOT NULL DEFAULT 0,
            coins               INT          NOT NULL DEFAULT 0,
            streak_days         INT          NOT NULL DEFAULT 0,
            last_challenge_date DATE                  DEFAULT NULL,
            active_title        VARCHAR(100)          DEFAULT NULL,
            is_admin            TINYINT(1)   NOT NULL DEFAULT 0,
            is_banned           TINYINT(1)   NOT NULL DEFAULT 0,
            created_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS coins        INT          NOT NULL DEFAULT 0")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS active_title VARCHAR(100) DEFAULT NULL")

    # ── lessons ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            judul          VARCHAR(200) NOT NULL,
            deskripsi      TEXT,
            konten         LONGTEXT,
            kode_contoh    TEXT,
            output_contoh  TEXT,
            xp_reward      INT  NOT NULL DEFAULT 10,
            urutan         INT  NOT NULL DEFAULT 0,
            dipublikasi    TINYINT(1) NOT NULL DEFAULT 0,
            created_at     DATETIME   NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── challenges ────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            judul          VARCHAR(200) NOT NULL,
            deskripsi      TEXT,
            kode_awal      TEXT,
            contoh_input   TEXT,
            contoh_output  TEXT,
            tingkat        VARCHAR(20) NOT NULL DEFAULT 'mudah',
            xp_reward      INT  NOT NULL DEFAULT 20,
            coin_reward    INT  NOT NULL DEFAULT 0,
            dipublikasi    TINYINT(1) NOT NULL DEFAULT 0,
            created_at     DATETIME   NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    cur.execute("ALTER TABLE challenges ADD COLUMN IF NOT EXISTS coin_reward INT NOT NULL DEFAULT 0")

    # ── user_lessons ──────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_lessons (
            user_id      INT NOT NULL,
            lesson_id    INT NOT NULL,
            selesai      TINYINT(1) NOT NULL DEFAULT 0,
            completed_at DATETIME DEFAULT NULL,
            PRIMARY KEY (user_id, lesson_id),
            FOREIGN KEY (user_id)   REFERENCES users(id)   ON DELETE CASCADE,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── user_challenges ───────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_challenges (
            user_id      INT NOT NULL,
            challenge_id INT NOT NULL,
            selesai      TINYINT(1) NOT NULL DEFAULT 0,
            completed_at DATETIME DEFAULT NULL,
            PRIMARY KEY (user_id, challenge_id),
            FOREIGN KEY (user_id)      REFERENCES users(id)      ON DELETE CASCADE,
            FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── posts ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            user_id        INT  NOT NULL,
            judul          VARCHAR(300) NOT NULL,
            konten         TEXT,
            kode_snippet   TEXT,
            output_preview TEXT,
            is_hidden      TINYINT(1) NOT NULL DEFAULT 0,
            created_at     DATETIME   NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── komentar ──────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS komentar (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            post_id    INT  NOT NULL,
            user_id    INT  NOT NULL,
            isi        TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id)  ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)  ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── likes ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id      INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NOT NULL,
            UNIQUE KEY uq_user_post (user_id, post_id),
            FOREIGN KEY (user_id) REFERENCES users(id)  ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id)  ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ════════════════════════════════════════
    # STEP 2 — Badge & Cosmetic
    # ════════════════════════════════════════

    cur.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            kode        VARCHAR(50)  NOT NULL UNIQUE,
            nama        VARCHAR(100) NOT NULL,
            deskripsi   VARCHAR(255) NOT NULL,
            ikon        VARCHAR(10)  NOT NULL DEFAULT '🏅',
            created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_badges (
            user_id     INT      NOT NULL,
            badge_id    INT      NOT NULL,
            earned_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, badge_id),
            FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
            FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── cosmetics: UNIQUE pada kolom nama agar tidak bisa duplikat ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cosmetics (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            nama        VARCHAR(100) NOT NULL UNIQUE,
            deskripsi   VARCHAR(255) NOT NULL,
            tipe        VARCHAR(30)  NOT NULL DEFAULT 'title',
            nilai       VARCHAR(100) NOT NULL,
            harga_coins INT          NOT NULL DEFAULT 50,
            ikon        VARCHAR(10)  NOT NULL DEFAULT '🏷️',
            created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # Jika tabel sudah ada sebelumnya (tanpa UNIQUE), tambahkan constraint-nya
    try:
        cur.execute("""
            ALTER TABLE cosmetics
            ADD UNIQUE KEY uq_cosmetics_nama (nama)
        """)
    except Exception:
        pass  # Constraint sudah ada, abaikan error

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_cosmetics (
            user_id      INT      NOT NULL,
            cosmetic_id  INT      NOT NULL,
            dibeli_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, cosmetic_id),
            FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
            FOREIGN KEY (cosmetic_id) REFERENCES cosmetics(id)  ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ════════════════════════════════════════
    # STEP 3 — Friend System
    # ════════════════════════════════════════

    cur.execute("""
        CREATE TABLE IF NOT EXISTS friends (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            user_id     INT         NOT NULL,
            friend_id   INT         NOT NULL,
            status      VARCHAR(10) NOT NULL DEFAULT 'pending',
            created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_friend_pair (user_id, friend_id),
            FOREIGN KEY (user_id)   REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ════════════════════════════════════════
    # STEP 4 — Duel Challenge 1v1
    # ════════════════════════════════════════

    cur.execute("""
        CREATE TABLE IF NOT EXISTS duel_soal (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            pertanyaan    TEXT         NOT NULL,
            pilihan_a     VARCHAR(300) NOT NULL,
            pilihan_b     VARCHAR(300) NOT NULL,
            pilihan_c     VARCHAR(300) NOT NULL,
            pilihan_d     VARCHAR(300) NOT NULL,
            jawaban_benar CHAR(1)      NOT NULL,
            penjelasan    TEXT,
            tingkat       VARCHAR(20)  NOT NULL DEFAULT 'mudah',
            created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS duel_matches (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            player1_id   INT         NOT NULL,
            player2_id   INT         NOT NULL,
            status       VARCHAR(10) NOT NULL DEFAULT 'waiting',
            soal_ids     TEXT        NOT NULL,
            score1       INT         NOT NULL DEFAULT 0,
            score2       INT         NOT NULL DEFAULT 0,
            winner_id    INT                  DEFAULT NULL,
            created_at   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            finished_at  DATETIME             DEFAULT NULL,
            FOREIGN KEY (player1_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (player2_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS duel_jawaban (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            match_id    INT      NOT NULL,
            user_id     INT      NOT NULL,
            soal_id     INT      NOT NULL,
            jawaban     CHAR(1)           DEFAULT NULL,
            benar       TINYINT(1)        DEFAULT NULL,
            waktu_jawab DATETIME          DEFAULT NULL,
            UNIQUE KEY uq_match_user_soal (match_id, user_id, soal_id),
            FOREIGN KEY (match_id) REFERENCES duel_matches(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id)  REFERENCES users(id)        ON DELETE CASCADE,
            FOREIGN KEY (soal_id)  REFERENCES duel_soal(id)    ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ════════════════════════════════════════
    # STEP 5 — Daily Challenge
    # ════════════════════════════════════════

    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenges (
            id           INT  AUTO_INCREMENT PRIMARY KEY,
            tanggal      DATE NOT NULL UNIQUE,
            challenge_id INT  NOT NULL,
            xp_bonus     INT  NOT NULL DEFAULT 50,
            coin_bonus   INT  NOT NULL DEFAULT 25,
            created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_daily_challenges (
            user_id      INT  NOT NULL,
            tanggal      DATE NOT NULL,
            completed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, tanggal),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ════════════════════════════════════════
    # SEED — Badges
    # ════════════════════════════════════════

    badges_default = [
        # Step 1-2
        ("first_challenge", "Tantangan Pertama",   "Selesaikan tantangan pertamamu",            "⚡"),
        ("streak_3",        "3 Hari Berturut",     "Aktif belajar 3 hari berturut-turut",       "🔥"),
        ("streak_7",        "Seminggu Penuh",      "Aktif belajar 7 hari berturut-turut",       "🔥"),
        ("lesson_5",        "Python Explorer",     "Selesaikan 5 pelajaran Python",             "📚"),
        ("challenge_5",     "Challenger",          "Selesaikan 5 tantangan",                    "⚔️"),
        ("challenge_10",    "Challenge Hunter",    "Selesaikan 10 tantangan",                   "🎯"),
        ("challenge_20",    "Challenge Master",    "Selesaikan semua 20 tantangan",             "🏆"),
        ("xp_100",          "XP 100",              "Kumpulkan 100 XP",                          "💯"),
        ("xp_500",          "XP 500",              "Kumpulkan 500 XP",                          "💎"),
        ("xp_1000",         "XP 1000",             "Kumpulkan 1000 XP",                         "👑"),
        ("first_post",      "Kontributor",         "Buat postingan pertama di komunitas",       "💬"),
        ("coins_100",       "Kaya Coins",          "Kumpulkan 100 coins",                       "🪙"),
        # Step 3
        ("first_friend",    "Punya Teman",         "Tambahkan teman pertamamu",                 "🤝"),
        # Step 4
        ("first_duel_win",  "Duel Pertama",        "Menangkan duel pertamamu",                  "⚔️"),
        ("duel_win_5",      "Duel Master",         "Menangkan 5 duel",                          "🏅"),
        # Step 5
        ("daily_3",         "Daily 3 Hari",        "Selesaikan daily challenge 3 hari berturut","☀️"),
        ("daily_7",         "Daily 7 Hari",        "Selesaikan daily challenge 7 hari berturut","🌟"),
        ("daily_30",        "Daily 30 Hari",       "Selesaikan daily challenge 30 hari berturut","🔱"),
    ]
    for kode, nama, desc, ikon in badges_default:
        cur.execute(
            "INSERT IGNORE INTO badges (kode, nama, deskripsi, ikon) VALUES (%s, %s, %s, %s)",
            (kode, nama, desc, ikon)
        )

    # ════════════════════════════════════════
    # SEED — Cosmetics
    # Hapus duplikat dulu, sisakan id terkecil per nama
    # ════════════════════════════════════════

    cur.execute("""
        DELETE FROM cosmetics
        WHERE id NOT IN (
            SELECT id FROM (
                SELECT MIN(id) AS id FROM cosmetics GROUP BY nama
            ) AS tmp
        )
    """)

    cosmetics_default = [
        ("Rookie Coder",    "Gelar pemula yang baru mulai coding",        "title", "Rookie Coder",    30,  "🌱"),
        ("Bug Hunter",      "Pemburu bug yang tangguh",                   "title", "Bug Hunter",      50,  "🐛"),
        ("Pythonista",      "Pecinta Python sejati",                      "title", "Pythonista",      80,  "🐍"),
        ("Stack Overflow",  "Master tanya jawab programming",             "title", "Stack Overflow",  100, "📚"),
        ("Code Ninja",      "Ahli coding yang gesit dan presisi",         "title", "Code Ninja",      150, "🥷"),
        ("Debug Lord",      "Penguasa debugging",                         "title", "Debug Lord",      200, "👾"),
        ("Algorithm King",  "Raja algoritma dan struktur data",           "title", "Algorithm King",  300, "👑"),
        ("10x Developer",   "Developer yang produktivitasnya luar biasa", "title", "10x Developer",   500, "⚡"),
        ("Duel Champion",   "Juara duel di JastCodeLab",                  "title", "Duel Champion",   200, "⚔️"),
        ("Daily Warrior",   "Tak pernah melewatkan daily challenge",      "title", "Daily Warrior",   200, "☀️"),
    ]
    for nama, desc, tipe, nilai, harga, ikon in cosmetics_default:
        cur.execute(
            "INSERT IGNORE INTO cosmetics (nama, deskripsi, tipe, nilai, harga_coins, ikon) VALUES (%s, %s, %s, %s, %s, %s)",
            (nama, desc, tipe, nilai, harga, ikon)
        )

    # ════════════════════════════════════════
    # SEED — Bank Soal Duel (30 soal Python multiple choice)
    # ════════════════════════════════════════

    soal_duel = [
        # ── MUDAH ──
        ("Apa output dari: print(type(42))?",
         "<class 'float'>", "<class 'int'>", "<class 'str'>", "<class 'num'>", "B",
         "42 adalah integer, jadi type() mengembalikan <class 'int'>", "mudah"),

        ("Manakah cara yang benar untuk membuat list kosong di Python?",
         "list = {}", "list = []", "list = ()", "list = <>", "B",
         "[] adalah sintaks untuk list kosong. {} untuk dict, () untuk tuple.", "mudah"),

        ("Apa hasil dari: 10 % 3?",
         "3", "1", "0", "3.33", "B",
         "% adalah operator modulo. 10 dibagi 3 = 3 sisa 1.", "mudah"),

        ("Fungsi mana yang digunakan untuk mengubah string menjadi integer?",
         "str()", "float()", "int()", "num()", "C",
         "int() mengkonversi nilai ke tipe integer.", "mudah"),

        ("Apa output dari: len('Python')?",
         "5", "6", "7", "Error", "B",
         "'Python' memiliki 6 karakter: P-y-t-h-o-n.", "mudah"),

        ("Manakah yang merupakan komentar valid di Python?",
         "// ini komentar", "/* ini komentar */", "# ini komentar", "-- ini komentar", "C",
         "Python menggunakan # untuk komentar satu baris.", "mudah"),

        ("Apa output dari: print(2 ** 3)?",
         "6", "8", "9", "5", "B",
         "** adalah operator pangkat. 2^3 = 8.", "mudah"),

        ("Manakah tipe data yang TIDAK ada di Python?",
         "int", "float", "char", "str", "C",
         "Python tidak punya tipe 'char'. Karakter tunggal tetap bertipe str.", "mudah"),

        ("Apa hasil dari: bool(0)?",
         "True", "False", "None", "Error", "B",
         "Nilai 0 dianggap falsy di Python, sehingga bool(0) = False.", "mudah"),

        ("Bagaimana cara mengakses elemen pertama dari list lst = [10, 20, 30]?",
         "lst[1]", "lst(0)", "lst[0]", "lst.first()", "C",
         "Indexing di Python dimulai dari 0. lst[0] mengakses elemen pertama.", "mudah"),

        # ── MENENGAH ──
        ("Apa output dari: [x**2 for x in range(4)]?",
         "[1, 4, 9, 16]", "[0, 1, 4, 9]", "[0, 1, 2, 3]", "[1, 2, 3, 4]", "B",
         "range(4) menghasilkan 0,1,2,3. Dikuadratkan: 0,1,4,9.", "menengah"),

        ("Apa perbedaan list dan tuple di Python?",
         "Tidak ada perbedaan", "List mutable, tuple immutable",
         "Tuple lebih lambat", "List tidak bisa diiterasi", "B",
         "List bisa diubah setelah dibuat (mutable), tuple tidak bisa (immutable).", "menengah"),

        ("Apa output dari: 'hello'.upper()[:3]?",
         "'hel'", "'HEL'", "'HEllo'", "Error", "B",
         ".upper() mengubah jadi 'HELLO', kemudian [:3] mengambil 3 karakter pertama: 'HEL'.", "menengah"),

        ("Manakah yang benar tentang dictionary di Python?",
         "Key harus berupa integer", "Key harus unik",
         "Value harus berupa string", "Dictionary tidak bisa di-loop", "B",
         "Setiap key dalam dictionary harus unik. Jika duplikat, value terakhir yang dipakai.", "menengah"),

        ("Apa output dari kode berikut?\nx = [1,2,3]\ny = x\ny.append(4)\nprint(len(x))",
         "3", "4", "Error", "None", "B",
         "y = x tidak membuat salinan. y dan x menunjuk list yang sama. Setelah append, len(x) = 4.", "menengah"),

        ("Apa fungsi dari keyword 'pass' di Python?",
         "Menghentikan loop", "Placeholder untuk blok kosong",
         "Mengembalikan None", "Skip iterasi saat ini", "B",
         "'pass' digunakan sebagai placeholder ketika blok kode tidak melakukan apa-apa.", "menengah"),

        ("Apa output dari: sorted([3,1,4,1,5], reverse=True)?",
         "[1,1,3,4,5]", "[5,4,3,1,1]", "[3,1,4,1,5]", "Error", "B",
         "sorted() dengan reverse=True mengurutkan dari besar ke kecil.", "menengah"),

        ("Manakah cara benar untuk memeriksa apakah key 'nama' ada dalam dict d?",
         "d.has('nama')", "'nama' in d", "d.contains('nama')", "d.exists('nama')", "B",
         "Operator 'in' digunakan untuk mengecek keberadaan key dalam dictionary.", "menengah"),

        ("Apa output dari: list(range(2, 10, 3))?",
         "[2, 5, 8]", "[2, 4, 6, 8]", "[2, 3, 4, 5]", "[2, 5, 8, 11]", "A",
         "range(2,10,3) dimulai dari 2, step 3: 2, 5, 8. 11 sudah melebihi 10.", "menengah"),

        ("Apa yang dilakukan fungsi zip()?",
         "Mengompres file", "Menggabungkan dua iterable menjadi tuple berpasangan",
         "Mengurutkan list", "Menghapus duplikat", "B",
         "zip([1,2], ['a','b']) menghasilkan [(1,'a'), (2,'b')].", "menengah"),

        # ── SULIT ──
        ("Apa output dari kode berikut?\ndef f(x=[]):\n    x.append(1)\n    return x\nprint(f())\nprint(f())",
         "[1] [1]", "[1] [1, 1]", "[1] [2]", "Error", "B",
         "Default argument list bersifat mutable dan dibuat sekali. Setiap panggilan memodifikasi list yang sama.", "sulit"),

        ("Manakah yang benar tentang generator di Python?",
         "Generator menyimpan semua nilai di memory", "Generator menggunakan keyword yield",
         "Generator tidak bisa diiterasi", "Generator sama dengan list comprehension", "B",
         "Generator menggunakan yield dan menghasilkan nilai satu per satu, hemat memory.", "sulit"),

        ("Apa output dari: (lambda x, y: x if x > y else y)(5, 3)?",
         "3", "5", "True", "Error", "B",
         "Lambda ini mengembalikan nilai terbesar. 5 > 3 sehingga return 5.", "sulit"),

        ("Apa yang dimaksud dengan decorator di Python?",
         "Fungsi untuk menghias output teks",
         "Fungsi yang membungkus fungsi lain untuk menambah fungsionalitas",
         "Class khusus untuk styling", "Modul untuk animasi", "B",
         "Decorator adalah higher-order function yang menerima fungsi dan mengembalikan fungsi baru.", "sulit"),

        ("Apa output dari: {x: x**2 for x in range(3)}?",
         "{0:0, 1:1, 2:4}", "{1:1, 2:4, 3:9}", "{0, 1, 4}", "Error", "A",
         "Dict comprehension membuat {0:0, 1:1, 2:4} dari range(3) yang menghasilkan 0,1,2.", "sulit"),

        ("Apa perbedaan antara deepcopy dan copy biasa di Python?",
         "Tidak ada perbedaan",
         "deepcopy menyalin objek beserta semua objek nested-nya",
         "copy lebih lambat dari deepcopy", "deepcopy hanya untuk list", "B",
         "copy.copy() membuat salinan shallow. copy.deepcopy() menyalin rekursif termasuk objek di dalamnya.", "sulit"),

        ("Apa output dari: next(filter(lambda x: x%2==0, [1,3,4,6,7]))?",
         "1", "4", "3", "6", "B",
         "filter mengambil elemen yang genap. Pertama yang genap adalah 4. next() mengambil elemen pertama.", "sulit"),

        ("Manakah yang benar tentang *args dan **kwargs?",
         "*args untuk named args, **kwargs untuk positional",
         "*args untuk positional args, **kwargs untuk keyword args",
         "Keduanya sama saja", "*args hanya bisa digunakan di class", "B",
         "*args menampung argumen posisional dalam tuple, **kwargs menampung keyword argument dalam dict.", "sulit"),

        ("Apa output dari: [1,2,3][::-1]?",
         "[1,2,3]", "[3,2,1]", "[-1,-2,-3]", "Error", "B",
         "Slice [::-1] membalik urutan list. [1,2,3] menjadi [3,2,1].", "sulit"),

        ("Apa yang terjadi jika memanggil list.sort() pada list yang berisi tipe data campuran?",
         "List diurutkan berdasarkan tipe",
         "TypeError karena tidak bisa membandingkan tipe berbeda",
         "List tidak berubah", "Elemen non-angka dihapus", "B",
         "Python 3 tidak bisa membandingkan int dengan str, sehingga melempar TypeError.", "sulit"),
    ]

    for pertanyaan, pa, pb, pc, pd, jawaban, penjelasan, tingkat in soal_duel:
        cur.execute("""
            INSERT IGNORE INTO duel_soal
                (pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d,
                 jawaban_benar, penjelasan, tingkat)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (pertanyaan, pa, pb, pc, pd, jawaban, penjelasan, tingkat))

    conn.commit()
    conn.close()
    print("✅ Database MySQL siap — semua tabel berhasil dibuat/diverifikasi.")