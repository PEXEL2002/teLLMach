from .user_service import UserService
from .chat_service import ChatService
from .qdrant_service import ensure_qdrant_collection

# Lazy imports - embeddings i retrieval ładują się tylko gdy potrzebne
def index_documents(documents):
    from .retrieval import index_documents as _index_documents
    return _index_documents(documents)

def semantic_search(query, top_k=5, filters=None):
    from .retrieval import semantic_search as _semantic_search
    return _semantic_search(query, top_k, filters)

__all__ = [
    "UserService",
    "ChatService",
    "ensure_qdrant_collection",
    "index_documents",
    "semantic_search",
]
