from sqlalchemy.orm import Session
from typing import Optional
from models import User
from schemas import UserCreate, UserOut
from core import hash_password, verify_password, create_access_token


class UserService:
    """Service for user operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user with hashed password"""
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Email already registered")

        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            imie=user_data.imie,
            nazwisko=user_data.nazwisko,
            email=user_data.email,
            hashed_password=hashed_pwd,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_user.decrypt_fields()
        return new_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> Optional[dict]:
        """Authenticate user and return token data"""
        user = UserService.get_user_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(user.id, user.email)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
        }
