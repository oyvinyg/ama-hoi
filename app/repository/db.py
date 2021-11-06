import json

from app.errors import ErrorResponse
from app.models.models import Organization, Office


headers = {}
organizations = [{"name": "org A", "id": "1"}, {"name": "org B", "id": "2"}]
organization_members = {"user-a": ["1", "2"], "user-b": ["1", "2"]}

office_list = [
    {
        "name": "NAV",
        "id": "1",
        "organization_id": "1",
        "img_url": "https://gowork.no/wp-content/uploads/2019/01/privat-kontor-coworking-gowork-kontorplasser-e1549274728285.jpg",
        "description": "Hyggelig kontor plassert på Carl Berner",
        "capacity": 40,
        "available_seats": 10,
        "facilities": ["Solskjerming", "Balkong", "Kantine", "Café"],
    },
    {
        "name": "Skatteetaten",
        "id": "2",
        "organization_id": "1",
        "img_url": "https://www.kinnarps.no/globalassets/images/articles/design-for-wellbeing-and-brand-building/design_branding_02.jpg?preset=article-maxLg1x",
        "description": "Moderne bygg med god ventilasjon",
        "capacity": 60,
        "available_seats": 20,
        "facilities": ["Opplegg for remote møter", "Planter"],
    },
    {
        "name": "Utdanningsetaten",
        "id": "3",
        "organization_id": "2",
        "img_url": "https://leiekontor.no/web_images/direkteopplastet/5bfe80464a017_LeieKontor.jpeg",
        "description": "Flott lokale på Helsfyr",
        "capacity": 50,
        "available_seats": 3,
        "facilities": ["Ergonomiske stoler", "Dockingstasjoner"],
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
        raise ErrorResponse(403, "You do not have access ")

    return Office.parse_obj(office)
