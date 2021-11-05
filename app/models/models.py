from pydantic import BaseModel
from typing import List


class Organization(BaseModel):
    name: str
    id: str


class Office(BaseModel):
    name: str
    id: str
    organization_id: str
    img_url: str = ""
    description: str
    capacity: int
    available_seats: int
    facilities: List[str]
