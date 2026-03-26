from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/tellmach")

engine = create_engine(
    DB_URL, 
    pool_pre_ping=True,  
    connect_args={"connect_timeout": 10} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="teLLMach API")

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
        db.execute("SELECT 1")
        return {"database": "online", "qdrant": "check http://tellmach_vector:6333/dashboard"}
    except Exception as e:
        return {"database": "offline", "error": str(e)}