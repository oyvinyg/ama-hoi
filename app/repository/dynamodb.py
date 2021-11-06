import json
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

from app.models.models import Organization, Office
from app.errors import ErrorResponse


class OfficeDataTable:

    table_name = "office-data"
    hash_key = "id"
    range_key = "type"

    organization_type = "organization"
    office_type = "office"

    def __init__(self):
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        self.table = dynamodb.Table(self.table_name)

    def put_organization(self, organization: Organization):
        self.table.put_item(Item=json.loads(organization.to_dynamodb_item()))

    def put_office(self, office: Office):
        self.table.put_item(Item=json.loads(office.to_dynamodb_item()))

    def list_organizations(self) -> List[Organization]:
        query_response = self.table.query(
            IndexName="IdByTypeIndex",
            KeyConditionExpression=Key(self.range_key).eq(self.organization_type),
        )
        items = query_response["Items"]
        return [Organization.parse_obj(item) for item in items]

    def get_organization(self, organization_id: str) -> Organization:
        item = self.table.get_item(
            Key={self.hash_key: organization_id, self.range_key: self.organization_type}
        ).get("Item", None)
        if item:
            return Organization.parse_obj(item)
        raise ErrorResponse(404, f"Organization with id {organization_id} not found")

    def list_offices(self, organization_id: str) -> List[Office]:
        query_response = self.table.query(
            IndexName="IdByTypeIndex",
            KeyConditionExpression=Key(self.range_key).eq(self.office_type)
            # & Key(self.hash_key).begins_with(f"{organization_id}/"),
        )
        items = query_response["Items"]
        return [Office.parse_obj(item) for item in items]

    def get_office(self, organization_id, office_id) -> Office:
        item = self.table.get_item(
            Key={
                self.hash_key: f"{organization_id}/{office_id}",
                self.range_key: self.office_type,
            }
        ).get("Item", None)
        if item:
            return Office.parse_obj(item)
        raise ErrorResponse(404, f"Organization with id {organization_id} not found")
