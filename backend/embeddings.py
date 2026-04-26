import os
import httpx

HF_TOKEN = os.getenv("HF_TOKEN", "")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN environment variable")

HF_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMBEDDING_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def _embed_single(text: str) -> list[float]:
    with httpx.Client(timeout=60) as client:
        res = client.post(HF_URL, headers=HEADERS, json={"inputs": text})
        res.raise_for_status()
        data = res.json()
    if not data or not isinstance(data, list):
        return []

    dim = len(data[0])
    pooled = [0.0] * dim
    count = len(data)
    for token_vec in data:
        for i, v in enumerate(token_vec):
            pooled[i] += float(v)

    return [v / count for v in pooled]


def embed_texts(texts: list[str]) -> list[list[float]]:
    return [_embed_single(t) for t in texts]


def embed_query(query: str) -> list[float]:
    return _embed_single(query)