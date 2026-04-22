import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "places")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))
QDRANT_DISTANCE = os.getenv("QDRANT_DISTANCE", "cosine").lower()

distance_map = {
    "cosine": Distance.COSINE,
    "dot": Distance.DOT,
    "euclidean": Distance.EUCLID,
}
distance = distance_map.get(QDRANT_DISTANCE, Distance.COSINE)

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def ensure_qdrant_collection() -> None:
    existing = {c.name for c in qdrant.get_collections().collections}
    if QDRANT_COLLECTION in existing:
        return

    qdrant.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=distance),
    )
    qdrant.create_payload_index(QDRANT_COLLECTION, "type", PayloadSchemaType.KEYWORD)
    qdrant.create_payload_index(QDRANT_COLLECTION, "city", PayloadSchemaType.KEYWORD)
    qdrant.create_payload_index(QDRANT_COLLECTION, "country", PayloadSchemaType.KEYWORD)
    qdrant.create_payload_index(QDRANT_COLLECTION, "rating", PayloadSchemaType.FLOAT)
    qdrant.create_payload_index(QDRANT_COLLECTION, "price_level", PayloadSchemaType.INTEGER)
