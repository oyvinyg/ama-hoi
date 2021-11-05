import json

from app.models.models import Organization, Office


headers = {}
organizations = [{"name": "org A", "id": "1"}, {"name": "org B", "id": "2"}]
organization_members = {"user-a": ["1"], "user-b": ["2"]}

office_list = [
    {
        "name": "off A",
        "id": "1",
        "organization_id": "1",
        "img_url": "",
        "description": "Lorem Ipsum",
        "capacity": 40,
        "available_seats": 10,
        "facilities": ["toilets"],
    },
    {
        "name": "off B",
        "id": "2",
        "organization_id": "1",
        "img_url": "",
        "description": "Lorem Ipsum",
        "capacity": 60,
        "available_seats": 20,
        "facilities": ["coffee machine"],
    },
    {
        "name": "off C",
        "id": "3",
        "organization_id": "2",
        "img_url": "",
        "description": "Lorem Ipsum",
        "capacity": 50,
        "available_seats": 3,
        "facilities": ["casual fridays"],
    },
]


def list_organizations():
    return [Organization.parse_obj(organization) for organization in organizations]


def get_organization(organization_id: str):

    for organization in organizations:

        if organization["id"] == organization_id:
            return Organization.parse_obj(organization)
    else:
        return []


def list_offices(username: str):
    organization_ids = organization_members.get(username, [])
    user_offices = []
    for o in office_list:
        if o["organization_id"] in organization_ids:
            user_offices.append(Office.parse_obj(o))
    return user_offices


def get_office(office_id: str, username: str):

    office = None
    for o in office_list:
        if o["id"] == office_id:
            office = o
    if not office:
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": "Not found"}),
        }

    if office["organization_id"] not in organization_members.get(username, []):
        raise ForbiddenException

    return Office.parse_obj(office)


class ForbiddenException(Exception):
    pass
