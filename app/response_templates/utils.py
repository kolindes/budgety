import json


class BaseResponseStatus:
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"


def get_base_response() -> dict:
    with open('app/response_templates/base_response.json') as f:
        return json.loads(f.read())
