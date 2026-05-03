from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IndexDocumentsRequest(BaseModel):
    documents: List[DocumentIn]


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None


class SearchHit(BaseModel):
    id: str
    score: float
    text: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    top_k: int
    hits: List[SearchHit]
