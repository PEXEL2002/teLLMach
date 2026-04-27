from qdrant_setup import qdrant, QDRANT_COLLECTION
from services.retrieval import index_documents

SEED_PLACES = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "text": "Pizzeria Roma w centrum Warszawy, dobra pizza i przystepne ceny.",
        "metadata": {"type": "restaurant", "city": "Warsaw", "country": "PL", "rating": 4.6, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "text": "Bistro Zielony Talerz na Mokotowie, swieze obiady i szybka obsluga.",
        "metadata": {"type": "restaurant", "city": "Warsaw", "country": "PL", "rating": 4.4, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "text": "Kawiarnia Rzemieslnicza na Kazimierzu z dobra kawa specialty.",
        "metadata": {"type": "cafe", "city": "Krakow", "country": "PL", "rating": 4.7, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "text": "Sushi Point w Gdansku, swieze zestawy i dostawa wieczorna.",
        "metadata": {"type": "restaurant", "city": "Gdansk", "country": "PL", "rating": 4.5, "price_level": 3},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "text": "Burger House w Poznaniu, duze porcje i dobre ceny.",
        "metadata": {"type": "restaurant", "city": "Poznan", "country": "PL", "rating": 4.3, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440006",
        "text": "Fine Dining Riverside we Wroclawiu, kuchnia autorska i wysoki standard.",
        "metadata": {"type": "restaurant", "city": "Wroclaw", "country": "PL", "rating": 4.8, "price_level": 4},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440007",
        "text": "Kawiarnia Slow Brew w Warszawie, cicha atmosfera do pracy.",
        "metadata": {"type": "cafe", "city": "Warsaw", "country": "PL", "rating": 4.5, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440008",
        "text": "Pierogarnia Domowa w Lublinie, tradycyjne pierogi i zupy.",
        "metadata": {"type": "restaurant", "city": "Lublin", "country": "PL", "rating": 4.6, "price_level": 1},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440009",
        "text": "Vegan Spot w Krakowie, roslinne burgery i bowle.",
        "metadata": {"type": "restaurant", "city": "Krakow", "country": "PL", "rating": 4.4, "price_level": 2},
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440010",
        "text": "Breakfast Club w Warszawie, sniadania calodzienne i kawa.",
        "metadata": {"type": "restaurant", "city": "Warsaw", "country": "PL", "rating": 4.5, "price_level": 2},
    },
]


def ensure_seed_places() -> None:
    seed_ids = [p["id"] for p in SEED_PLACES]

    existing_points = qdrant.retrieve(
        collection_name=QDRANT_COLLECTION,
        ids=seed_ids,
        with_payload=False,
        with_vectors=False,
    )

    existing_ids = {str(p.id) for p in existing_points}
    missing = [p for p in SEED_PLACES if str(p["id"]) not in existing_ids]

    if not missing:
        return

    index_documents(missing)