from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "uzytkownik"

    id = Column(Integer, primary_key=True, index=True)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    miejsca = relationship("Miejsca", back_populates="user")


class Miejsca(Base):
    __tablename__ = "miejsca"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("uzytkownik.id"), nullable=False)
    miejsce = Column(String, nullable=False)
    pobyt_od = Column(Date, nullable=False)
    pobyt_do = Column(Date, nullable=False)

    user = relationship("User", back_populates="miejsca")
