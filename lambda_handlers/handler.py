import json


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


def list_organizations(event, context):
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(organizations),
    }


def get_organization(event, context):
    organization_id = event["pathParameters"]["organization_id"]

    for organization in organizations:

        if organization["id"] == organization_id:
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(organization),
            }
    else:
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": "Not found"}),
        }


def list_offices(event, context):
    username = event["queryStringParameters"].get("username")
    if not username:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "Required param 'username' missing"}),
        }
    organization_ids = organization_members.get(username, [])
    user_offices = []
    for o in office_list:
        if o["organization_id"] in organization_ids:
            user_offices.append(o)
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(user_offices),
    }


def get_office(event, context):
    import json

    print(json.dumps(event, indent=2))
    username = event["queryStringParameters"].get("username")
    if not username:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "Required param 'username' missing"}),
        }
    office_id = event["pathParameters"]["office_id"]

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
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": "User does not have access to this office"}),
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(office),
    }
