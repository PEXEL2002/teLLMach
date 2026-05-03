from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import relationship
from core.encryption import encrypt_data, decrypt_data
from .base import Base


class User(Base):
    __tablename__ = "uzytkownik"

    id: int = Column(Integer, primary_key=True, index=True)
    imie: str = Column(String, nullable=False)
    nazwisko: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)

    places = relationship("Place", back_populates="user")

    def decrypt_fields(self) -> None:
        """Manually decrypt fields - used after refresh"""
        if self.imie:
            self.imie = decrypt_data(self.imie)
        if self.nazwisko:
            self.nazwisko = decrypt_data(self.nazwisko)


@event.listens_for(User, "before_insert")
def encrypt_user_before_insert(mapper, connection, target: User) -> None:
    """Encrypt imie and nazwisko before inserting to database"""
    if target.imie:
        target.imie = encrypt_data(target.imie)
    if target.nazwisko:
        target.nazwisko = encrypt_data(target.nazwisko)


@event.listens_for(User, "before_update")
def encrypt_user_before_update(mapper, connection, target: User) -> None:
    """Encrypt imie and nazwisko before updating database"""
    if target.imie and not target.imie.startswith("gAAAAAB"):
        target.imie = encrypt_data(target.imie)
    if target.nazwisko and not target.nazwisko.startswith("gAAAAAB"):
        target.nazwisko = encrypt_data(target.nazwisko)


@event.listens_for(User, "load")
def decrypt_user_after_load(target: User, context) -> None:
    """Decrypt imie and nazwisko after fetching from database"""
    if target.imie:
        target.imie = decrypt_data(target.imie)
    if target.nazwisko:
        target.nazwisko = decrypt_data(target.nazwisko)
