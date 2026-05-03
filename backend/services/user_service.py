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
        # Normalize email
        email = user_data.email.strip().lower()
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError("Email already registered")

        hashed_pwd = hash_password(user_data.password.strip())
        print(f"[REGISTER] Creating user: email={email}, hashed_pwd={hashed_pwd[:20]}...")
        
        new_user = User(
            imie=user_data.imie,
            nazwisko=user_data.nazwisko,
            email=email,
            hashed_password=hashed_pwd,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"[REGISTER] User saved: id={new_user.id}, email={new_user.email}")
        new_user.decrypt_fields()
        return new_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        # Normalize email
        email = email.strip().lower()
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> Optional[dict]:
        """Authenticate user and return token data"""
        # Normalize email
        email_normalized = email.strip().lower()
        user = UserService.get_user_by_email(db, email_normalized)

        if not user:
            print(f"[AUTH] User not found for email: {email_normalized}")
            return None
        
        password_valid = verify_password(password.strip(), user.hashed_password)
        print(f"[AUTH] Email: {email_normalized}, Password valid: {password_valid}, Hashed in DB: {user.hashed_password[:20]}...")
        
        if not password_valid:
            return None

        access_token = create_access_token(user.id, user.email)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
        }
