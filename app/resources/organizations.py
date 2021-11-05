from typing import List

from fastapi import APIRouter, status

from app.repository import db
from app.models.models import Organization

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Organization],
)
def list_organizations():
    return db.list_organizations()


@router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    response_model=Organization,
)
def get_organization(organization_id: str):
    return db.get_organization(organization_id)
