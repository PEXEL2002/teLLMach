from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Place(Base):
    __tablename__ = "miejsca"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("uzytkownik.id"), nullable=False)
    miejsce: str = Column(String, nullable=False)
    pobyt_od: object = Column(Date, nullable=False)
    pobyt_do: object = Column(Date, nullable=False)

    user = relationship("User", back_populates="places")
