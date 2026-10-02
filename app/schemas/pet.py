from datetime import date

from pydantic import BaseModel, ConfigDict


class PetCreate(BaseModel):
    name: str
    species: str | None = None
    breed: str | None = None
    birth_date: date | None = None


class PetOut(BaseModel):
    id: int
    name: str
    species: str | None
    breed: str | None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
