from sqlalchemy import Column, Integer, String, Date, ForeignKey, event
from sqlalchemy.orm import relationship
from database import Base
from encryption import encrypt_data, decrypt_data


class User(Base):
    __tablename__ = "uzytkownik"

    id = Column(Integer, primary_key=True, index=True)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    miejsca = relationship("Miejsca", back_populates="user")

    def decrypt_fields(self):
        """Manually decrypt fields - used after refresh"""
        if self.imie:
            self.imie = decrypt_data(self.imie)
        if self.nazwisko:
            self.nazwisko = decrypt_data(self.nazwisko)


class Miejsca(Base):
    __tablename__ = "miejsca"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("uzytkownik.id"), nullable=False)
    miejsce = Column(String, nullable=False)
    pobyt_od = Column(Date, nullable=False)
    pobyt_do = Column(Date, nullable=False)

    user = relationship("User", back_populates="miejsca")


# Event listeners for encryption/decryption
@event.listens_for(User, "before_insert")
def encrypt_user_before_insert(mapper, connection, target):
    """Encrypt imie and nazwisko before inserting to database"""
    if target.imie:
        target.imie = encrypt_data(target.imie)
    if target.nazwisko:
        target.nazwisko = encrypt_data(target.nazwisko)


@event.listens_for(User, "before_update")
def encrypt_user_before_update(mapper, connection, target):
    """Encrypt imie and nazwisko before updating database"""
    if target.imie and not target.imie.startswith("gAAAAAB"):  # Check if already encrypted
        target.imie = encrypt_data(target.imie)
    if target.nazwisko and not target.nazwisko.startswith("gAAAAAB"):  # Check if already encrypted
        target.nazwisko = encrypt_data(target.nazwisko)


@event.listens_for(User, "load")
def decrypt_user_after_load(target, context):
    """Decrypt imie and nazwisko after fetching from database"""
    if target.imie:
        target.imie = decrypt_data(target.imie)
    if target.nazwisko:
        target.nazwisko = decrypt_data(target.nazwisko)


