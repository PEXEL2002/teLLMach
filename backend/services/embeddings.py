import os
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google/embeddinggemma-300m")
HF_TOKEN = os.getenv("HF_TOKEN")
LOAD_EMBEDDINGS_MODEL = os.getenv("LOAD_EMBEDDINGS_MODEL", "false").lower() == "true"

_model: Optional[object] = None
_model_error: Optional[Exception] = None


def _get_model():
    """Lazy load model on first use with error handling"""
    global _model, _model_error

    if not LOAD_EMBEDDINGS_MODEL:
        raise RuntimeError(
            "Embedding model is disabled. Set LOAD_EMBEDDINGS_MODEL=true to enable semantic search."
        )

    if _model_error:
        raise _model_error

    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
            _model = SentenceTransformer(
                EMBEDDING_MODEL,
                token=HF_TOKEN,
            )
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            _model_error = e
            logger.error(f"Failed to load embedding model: {e}")
            raise

    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Encode multiple texts to embeddings"""
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Encode single query string to embedding"""
    return embed_texts([query])[0]
