import re

from django.http.request import QueryDict

from api.services.connectors import connectors_all
from api.services.base.response import ErrorResponse, Response
from importlib import import_module

c2s_pattern = re.compile(r'(?<!^)(?=[A-Z])')


async def process_api_call(endpoint: str, params: QueryDict) -> Response:
    if endpoint not in connectors_all:
        return ErrorResponse(f'Connector "{endpoint}" not found')

    conn_module = import_module(f'api.services.connectors.{endpoint}.connector')
    connector = conn_module.Connector(params)

    return await connector.process_request()


def camel_to_snake(string: str) -> str:
    return c2s_pattern.sub('_', string).lower()

