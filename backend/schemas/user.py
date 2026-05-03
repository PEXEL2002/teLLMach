from pydantic import BaseModel, EmailStr


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

    model_config = {"from_attributes": True}
