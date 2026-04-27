from fastapi import APIRouter, HTTPException
from schemas.search_schema import IndexDocumentsRequest, SearchRequest, SearchResponse
from services.retrieval import index_documents, semantic_search

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/index-documents")
def index_documents_endpoint(req: IndexDocumentsRequest):
    try:
        count = index_documents([d.model_dump() for d in req.documents])
        return {"status": "ok", "indexed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semantic-search", response_model=SearchResponse)
def semantic_search_endpoint(req: SearchRequest):
    try:
        hits = semantic_search(req.query, req.top_k, req.filters)
        return SearchResponse(query=req.query, top_k=req.top_k, hits=hits)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

