import json


def hello(event, context):
    headers = {}
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({"message": "Hello AMA HØI!"}),
    }
