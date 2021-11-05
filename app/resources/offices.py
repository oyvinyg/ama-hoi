from typing import List

from fastapi import APIRouter, status

from app.repository import db
from app.models.models import Office

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Office],
)
def list_offices(username: str):
    return db.list_offices(username)


@router.get(
    "/{office_id}",
    status_code=status.HTTP_200_OK,
    response_model=Office,
)
def get_office(office_id: str, username: str):
    return db.get_office(office_id, "")
