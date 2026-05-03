import os
from typing import List

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@postgres:5432/tellmach",
)

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode()

# CORS
CORS_ORIGINS: List[str] = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

# API
API_VERSION = "v1"
API_TITLE = "teLLMach API"

# Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "places")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))
QDRANT_DISTANCE = os.getenv("QDRANT_DISTANCE", "cosine").lower()

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google/embeddinggemma-300m")
HF_TOKEN = os.getenv("HF_TOKEN")
