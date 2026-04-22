from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from qdrant_setup import ensure_qdrant_collection

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/tellmach")

engine = create_engine(
    DB_URL, 
    pool_pre_ping=True,  
    connect_args={"connect_timeout": 10} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI(title="teLLMach API")

@app.on_event("startup")
def startup_event():
    ensure_qdrant_collection()


allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to teLLMach API", "status": "connected"}

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "online", "qdrant": "check http://tellmach_vector:6333/dashboard"}
    except Exception as e:
        return {"database": "offline", "error": str(e)}

@app.get("/api/test-connection")
async def test_connection():
    return {
        "status": "success",
        "message": "Connection to teLLMach API successful",
        "version": "1.0.0"
    }

