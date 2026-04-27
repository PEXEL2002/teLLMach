from typing import List, Optional
from pydantic import BaseModel, Field


class PlacePayload(BaseModel):
    name: str
    city: str
    country: str
    tags: List[str] = Field(default_factory=list)
    rating: Optional[float] = None
    price_level: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    source_id: Optional[str] = None
    updated_at: Optional[str] = None


class UpsertPlaceItem(BaseModel):
    id: Optional[str] = None
    vector: List[float]
    payload: PlacePayload


class UpsertPlacesRequest(BaseModel):
    points: List[UpsertPlaceItem]


class SearchPlacesRequest(BaseModel):
    query_vector: List[float]
    limit: int = 10
    city: Optional[str] = None
    country: Optional[str] = None
    min_rating: Optional[float] = None
    max_price_level: Optional[int] = None
