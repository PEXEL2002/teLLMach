from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserOut, Token
from core import get_db, get_current_user
from services import UserService
from utils import UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserOut:
    """Register new user with email and password"""
    try:
        user = UserService.create_user(db, user_data)
        return user
    except ValueError as e:
        raise UserAlreadyExistsException()


@router.post("/login", response_model=Token)
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db),
) -> Token:
    """Login with email and password - returns JWT token"""
    token_data = UserService.authenticate_user(db, email, password)

    if not token_data:
        raise InvalidCredentialsException()

    return Token(**token_data)


@router.get("/me", response_model=UserOut)
def get_current_user_info(
    current_user = Depends(get_current_user),
) -> UserOut:
    """Get current authenticated user info (requires valid JWT token)"""
    return current_user
