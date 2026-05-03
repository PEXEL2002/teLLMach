from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
