#!/bin/bash
# =====================================================
# JastCodeLab — Jalankan Project Secara Lokal
# =====================================================
# Cara pakai: bash start.sh

set -e

echo ""
echo "======================================"
echo "  JastCodeLab — Setup & Jalankan     "
echo "======================================"
echo ""

# ── 1. Cek Python ──
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Install Python 3.9+ terlebih dahulu."
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# ── 2. Masuk ke folder backend ──
cd backend

# ── 3. Buat virtual environment jika belum ada ──
if [ ! -d "venv" ]; then
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
fi

# ── 4. Aktifkan venv ──
source venv/bin/activate

# ── 5. Install dependensi ──
echo "📥 Menginstall dependensi..."
pip install -r requirements.txt -q

echo ""
echo "✅ Setup selesai!"
echo ""
echo "🚀 Menjalankan JastCodeLab API..."
echo "   URL: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📁 Untuk melihat frontend:"
echo "   Buka folder 'frontend/' di browser"
echo "   atau gunakan Live Server di VS Code"
echo ""
echo "Tekan Ctrl+C untuk menghentikan server"
echo "======================================"
echo ""

# ── 6. Jalankan FastAPI ──
uvicorn main:app --reload --host 0.0.0.0 --port 8000
