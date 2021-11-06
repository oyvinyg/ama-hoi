from typing import List

from fastapi import APIRouter, status, Depends

from app.errors import error_message_models
from app.repository.radar_data_table import RadarDataTable
from app.models.models import RadarData

router = APIRouter()


def radar_data_table():
    return RadarDataTable()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=RadarData,
)
def post_radar_data(
    radar_data: RadarData, radar_data_table: RadarDataTable = Depends(radar_data_table)
):
    radar_data_table.put_radar_data(radar_data)
    return radar_data


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[RadarData],
    responses=error_message_models(
        status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND
    ),
)
def get_office(
    office_id: str, radar_data_table: RadarDataTable = Depends(radar_data_table)
):
    return radar_data_table.list_office_radar_data(office_id)
