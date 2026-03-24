"""
JastCodeLab — Backend API (FastAPI)
Jalankan: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import router

app = FastAPI(title="JastCodeLab API", version="1.0.0")

# CORS — FIX: tidak bisa pakai allow_origins=["*"] + allow_credentials=True bersamaan
# Harus sebutkan origin secara eksplisit
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",    # Live Server VS Code
        "http://localhost:5500",     # Live Server (localhost)
        "http://127.0.0.1:5501",    # Live Server port alternatif
        "http://localhost:5501",
        "http://127.0.0.1:3000",    # Kalau pakai port 3000
        "http://localhost:3000",
        "http://127.0.0.1:8080",    # Kalau pakai port 8080
        "http://localhost:8080",
        "null",                      # Buka langsung dari file (file://)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi database saat startup
@app.on_event("startup")
async def startup():
    init_db()

# Daftarkan semua routes
app.include_router(router)

@app.get("/")
def root():
    return {"pesan": "JastCodeLab API aktif 🚀"}