from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
import uuid
import json
import httpx

from qdrant_setup import ensure_qdrant_collection
from routers.semantic_tool import router as semantic_tool_router
from config.semantic_search_config import ensure_seed_places
from typing import Optional
from database import engine, SessionLocal, Base
from models import User, Miejsca, Message
from schemas import UserCreate, UserOut, PlaceCreate, PlaceOut, Token
from auth import hash_password, verify_password, create_access_token, verify_token

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="teLLMach API")
app.include_router(semantic_tool_router)

@app.on_event("startup")
def startup_event():
    ensure_qdrant_collection()
    ensure_seed_places()

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


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    id: str
    content: str


class MessageSaveRequest(BaseModel):
    messages: list[dict]  # [{role, content, timestamp}]


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

    class Config:
        from_attributes = True


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


N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

@app.post("/api/chat")
async def chat(chat_request: ChatRequest, current_user: User = Depends(get_current_user)):
    """AI Travel Assistant — streaming proxy do n8n webhook"""
    message = chat_request.message.strip()

    if not message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")

    if not N8N_WEBHOOK_URL:
        async def _fallback():
            yield f"data: {json.dumps({'output': 'Skonfiguruj N8N_WEBHOOK_URL.'})}\n\ndata: [DONE]\n\n"
        return StreamingResponse(_fallback(), media_type="text/event-stream")

    payload = {"message": message, "user_id": current_user.id, "email": current_user.email}

    async def _stream_n8n():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", N8N_WEBHOOK_URL, json=payload) as resp:
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes():
                    if chunk:
                        yield chunk

    return StreamingResponse(
        _stream_n8n(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/history", response_model=list[MessageOut])
def get_history(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Message)
        .filter(Message.user_id == current_user.id)
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )
    return [
        MessageOut(id=r.id, role=r.role, content=r.content, created_at=r.created_at.isoformat())
        for r in rows
    ]


@app.post("/api/history", status_code=201)
def save_messages(
    body: MessageSaveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for m in body.messages:
        db.add(Message(user_id=current_user.id, role=m["role"], content=m["content"]))
    db.commit()
    return {"saved": len(body.messages)}
