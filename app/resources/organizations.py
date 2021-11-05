from typing import List

from fastapi import APIRouter, status

from app.errors import error_message_models
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
    responses=error_message_models(status.HTTP_404_NOT_FOUND),
)
def get_organization(organization_id: str):
    return db.get_organization(organization_id)
