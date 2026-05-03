from pydantic import BaseModel
from datetime import date


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

    model_config = {"from_attributes": True}
