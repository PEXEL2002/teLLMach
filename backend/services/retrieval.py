from typing import Any, Dict, List, Optional
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from .qdrant_service import qdrant, QDRANT_COLLECTION


def _build_filter(filters: Optional[Dict[str, Any]]) -> Optional[Filter]:
    """Build Qdrant filter from filter dict"""
    if not filters:
        return None

    must = []
    for key, value in filters.items():
        must.append(FieldCondition(key=key, match=MatchValue(value=value)))
    return Filter(must=must)


def index_documents(documents: List[Dict[str, Any]]) -> int:
    """Index documents into Qdrant collection"""
    from .embeddings import embed_texts

    texts = [doc["text"] for doc in documents]
    vectors = embed_texts(texts)

    points = []
    for doc, vector in zip(documents, vectors):
        payload = {"text": doc["text"], **doc.get("metadata", {})}
        points.append(
            PointStruct(
                id=doc["id"],
                vector=vector,
                payload=payload,
            )
        )

    qdrant.upsert(collection_name=QDRANT_COLLECTION, points=points)
    return len(points)


def semantic_search(
    query: str,
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Perform semantic search in Qdrant collection"""
    from .embeddings import embed_query

    vector = embed_query(query)
    qdrant_filter = _build_filter(filters)

    results = qdrant.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=vector,
        query_filter=qdrant_filter,
        limit=top_k,
        with_payload=True,
    )

    hits = []
    for r in results:
        payload = r.payload or {}
        hits.append(
            {
                "id": str(r.id),
                "score": float(r.score),
                "text": payload.get("text"),
                "metadata": {k: v for k, v in payload.items() if k != "text"},
            }
        )
    return hits
