from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from database import engine, SessionLocal, Base
from models import User, Miejsca
from schemas import UserCreate, UserOut, PlaceCreate, PlaceOut
from auth import hash_password, verify_password

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="teLLMach API")

# CORS configuration
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


@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user with email and password"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        imie=user_data.imie,
        nazwisko=user_data.nazwisko,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=dict)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login with email and password"""
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
        "imie": user.imie,
        "nazwisko": user.nazwisko
    }


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
