import os
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google/embeddinggemma-300m")

HF_TOKEN = os.getenv("HF_TOKEN")

_model = SentenceTransformer(
    EMBEDDING_MODEL,
    token=HF_TOKEN,
)

def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = _model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()

def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]