from typing import List

from fastapi import APIRouter, status, Depends

from app.errors import error_message_models
from app.repository.dynamodb import OfficeDataTable
from app.models.models import Organization, OrganizationMembers, Office

router = APIRouter()


def office_data_table():
    return OfficeDataTable()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Organization,
)
def create_organization(
    username: str,
    organization: Organization,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    organization.set_id()
    organization.members.append(OrganizationMembers(role="admin", username=username))
    office_data_table.put_organization(organization)
    return organization


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Organization],
)
def list_organizations(office_data_table: OfficeDataTable = Depends(office_data_table)):
    return office_data_table.list_organizations()


@router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    response_model=Organization,
    responses=error_message_models(status.HTTP_404_NOT_FOUND),
)
def get_organization(
    organization_id: str,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    return office_data_table.get_organization(organization_id)


@router.post(
    "/{organization_id}/offices",
    status_code=status.HTTP_200_OK,
    response_model=Office,
)
def create_office(
    organization_id,
    username: str,
    office: Office,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    office.set_id(organization_id)
    office_data_table.put_organization(office)
    return office


@router.get(
    "/{organization_id}/offices",
    status_code=status.HTTP_200_OK,
    response_model=List[Office],
)
def list_offices(
    organization_id,
    username: str,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    return office_data_table.list_offices(organization_id)


@router.get(
    "/{organization_id}/offices/{office_id}",
    status_code=status.HTTP_200_OK,
    response_model=Office,
)
def get_office(
    organization_id,
    office_id,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    return office_data_table.get_office(organization_id, office_id)


@router.patch(
    "/{organization_id}/offices/{office_id}",
    status_code=status.HTTP_200_OK,
    response_model=Office,
)
def update_office(
    organization_id,
    office_id,
    office: Office,
    office_data_table: OfficeDataTable = Depends(office_data_table),
):
    stored_office = office_data_table.get_office(organization_id, office_id)
    update_data = office.dict(exclude_unset=True)
    updated_office = stored_office.copy(update=update_data)
    office_data_table.put_office(updated_office)
    return updated_office
