import json
from pydantic import BaseModel
from typing import List

import shortuuid


class OrganizationMembers(BaseModel):
    role: str
    username: str


class Organization(BaseModel):
    name: str
    id: str = None
    members: List[OrganizationMembers] = []

    def set_id(self):
        self.id = f"org-{shortuuid.random(length=5).lower()}"

    def to_dynamodb_item(self):
        item = self.dict()
        item["type"] = "organization"
        return json.dumps(item)


class Office(BaseModel):
    name: str
    id: str = None
    img_url: str = ""
    description: str = ""
    capacity: int = 0
    available_seats: int = 0
    facilities: List[str] = []
    members: List[str] = []

    def set_id(self, organization_id):
        self.id = f"{organization_id}/org-{shortuuid.random(length=5).lower()}"

    def to_dynamodb_item(self):
        item = self.dict()
        item["type"] = "office"
        return json.dumps(item)


class RadarData(BaseModel):
    id: str
    office_id: str
    data: dict
