from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_health_status(db: Session) -> Dict[str, Any]:
    """Get health status of database and services"""
    try:
        db.execute(text("SELECT 1"))
        return {
            "database": "online",
            "qdrant": "check http://tellmach_vector:6333/dashboard",
        }
    except Exception as e:
        return {"database": "offline", "error": str(e)}
