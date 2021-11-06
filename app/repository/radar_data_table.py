import json
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

from app.models.models import RadarData


class RadarDataTable:

    table_name = "office-radar-data"
    hash_key = "id"
    range_key = "office_id"

    def __init__(self):
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        self.table = dynamodb.Table(self.table_name)

    def put_radar_data(self, radar_data: RadarData):
        self.table.put_item(Item=json.loads(radar_data.json()))

    def list_office_radar_data(self, office_id: str) -> List[RadarData]:
        query_response = self.table.query(
            IndexName="IdByOfficeIdIndex",
            KeyConditionExpression=Key(self.range_key).eq(office_id),
        )
        items = query_response["Items"]
        return [RadarData.parse_obj(item) for item in items]
