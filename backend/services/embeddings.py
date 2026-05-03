import os
from sentence_transformers import SentenceTransformer
from typing import List, Optional

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google/embeddinggemma-300m")
HF_TOKEN = os.getenv("HF_TOKEN")

_model: Optional[SentenceTransformer] = None


def _get_model() -> SentenceTransformer:
    """Lazy load model on first use"""
    global _model
    if _model is None:
        _model = SentenceTransformer(
            EMBEDDING_MODEL,
            token=HF_TOKEN,
        )
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Encode multiple texts to embeddings"""
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Encode single query string to embedding"""
    return embed_texts([query])[0]
