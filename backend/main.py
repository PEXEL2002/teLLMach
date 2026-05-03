from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, API_TITLE
from database import engine
from models import Base, User, Place
from routers import (
    auth_router,
    users_router,
    chat_router,
    tools_router,
    health_router,
)
from services import ensure_qdrant_collection
from config.semantic_search_config import ensure_seed_places


# Create tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title=API_TITLE)

# Add routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
app.include_router(tools_router)
app.include_router(health_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize services on startup"""
    ensure_qdrant_collection()
    ensure_seed_places()

