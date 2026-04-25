from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    imie: str
    nazwisko: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    imie: str
    nazwisko: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


class PlaceCreate(BaseModel):
    miejsce: str
    pobyt_od: date
    pobyt_do: date


class PlaceOut(BaseModel):
    id: int
    user_id: int
    miejsce: str
    pobyt_od: date
    pobyt_do: date

    class Config:
        from_attributes = True
