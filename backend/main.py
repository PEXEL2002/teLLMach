from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from typing import Optional

from database import engine, SessionLocal, Base
from models import User, Miejsca
from schemas import UserCreate, UserOut, PlaceCreate, PlaceOut, Token
from auth import hash_password, verify_password, create_access_token, verify_token

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


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    """Extract and validate JWT token from Authorization header"""
    print(f"DEBUG: Authorization header: {authorization}")

    if not authorization or not authorization.startswith("Bearer "):
        print("DEBUG: Missing/invalid auth header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )

    token = authorization.split(" ")[1]
    print(f"DEBUG: Token extracted: {token[:50]}...")
    payload = verify_token(token)
    print(f"DEBUG: Token payload: {payload}")

    if payload is None:
        print("DEBUG: Token verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


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
    new_user.decrypt_fields()  # Decrypt for response

    return new_user


@app.post("/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login with email and password - returns JWT token"""
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user.id, user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@app.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info (requires valid JWT token)"""
    return current_user


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
