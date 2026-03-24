"""
JastCodeLab — Backend API (FastAPI)
Jalankan: uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (opsional, taruh cleanup di sini kalau ada)


app = FastAPI(title="JastCodeLab API", version="1.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan semua routes
app.include_router(router)


@app.get("/")
def root():
    return {"pesan": "JastCodeLab API aktif 🚀"}