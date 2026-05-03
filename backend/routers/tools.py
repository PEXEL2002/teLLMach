from fastapi import APIRouter, HTTPException, status
from schemas import IndexDocumentsRequest, SearchRequest, SearchResponse
from services import index_documents, semantic_search

router = APIRouter(prefix="/api/v1/tools", tags=["tools"])


@router.post("/index-documents", status_code=status.HTTP_200_OK)
def index_documents_endpoint(req: IndexDocumentsRequest):
    """Index documents into Qdrant collection"""
    try:
        count = index_documents([d.model_dump() for d in req.documents])
        return {"status": "ok", "indexed": count}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semantic-search", response_model=SearchResponse)
def semantic_search_endpoint(req: SearchRequest) -> SearchResponse:
    """Perform semantic search in Qdrant collection"""
    try:
        hits = semantic_search(req.query, req.top_k, req.filters)
        return SearchResponse(query=req.query, top_k=req.top_k, hits=hits)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
