from munch import DefaultMunch
from requests import Response

from text_metrics.modules.models.utilities.server_response import ServerResponse

api_base_url = 'http://localhost:5000/api'


def handle_response(response: Response) -> ServerResponse:
    if 200 <= response.status_code < 300:
        if response.text == '':
            return None

        result = DefaultMunch.fromDict(response.json())
        return result
    elif response.status_code == 400:
        # Check if the response.json has an errors key
        if 'errors' not in response.json():
            raise Exception("Bad Request")

        errors = response.json()['errors']
        if isinstance(errors, list):
            # If it is a list, join the errors together
            raise Exception(" ".join(errors))
        else:
            raise Exception(errors)
    elif response.status_code == 401:
        raise Exception("Unauthorized")
    elif response.status_code == 403:
        raise Exception("Forbidden")
    elif response.status_code == 404:
        raise Exception("Not Found")
    elif response.status_code == 500:
        raise Exception("Internal Server Error")
    else:
        raise Exception("Unknown Error: " + str(response.status_code))
