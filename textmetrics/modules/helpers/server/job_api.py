import requests

from textmetrics.modules.helpers.server import api_base_url, handle_response
from textmetrics.modules.models.job import Job
from textmetrics.modules.models.utilities.server_response import ServerResponse


def get_jobs() -> ServerResponse[list[Job]]:
    response = requests.get(f'{api_base_url}/Jobs')
    return handle_response(response)


def get_dispatched_jobs() -> ServerResponse[list[Job]]:
    response = requests.get(f'{api_base_url}/Jobs?status=Pending&dispatch=true')
    return handle_response(response)
