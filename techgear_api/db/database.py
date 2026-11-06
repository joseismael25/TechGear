"""Configuración centralizada de MongoDB Atlas."""
import os
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGO_URI = os.getenv("MONGO_URI", "").strip()
client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=10000) if MONGO_URI else None
database = client.get_database("techgear_db") if client else None

def get_database():
    """Devuelve la base de datos o informa de una configuración ausente."""
    if database is None:
        raise RuntimeError("Falta configurar MONGO_URI en techgear_api/.env")
    return database
