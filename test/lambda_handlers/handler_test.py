import json

from lambda_handlers import handler


def test_hello():
    response = handler.hello({}, {})
    body = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert body == {"message": "Hello AMA HØI!"}
