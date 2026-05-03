from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core import get_db
from utils import get_health_status
from models import User

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", status_code=200)
def health_check(db: Session = Depends(get_db)) -> dict:
    """Health check endpoint - verify database and services are online"""
    return get_health_status(db)


@router.get("/", status_code=200)
def root() -> dict:
    """Root endpoint"""
    return {
        "message": "Welcome to teLLMach API",
        "status": "connected",
        "version": "1.0.0",
    }
