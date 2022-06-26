from django.http.request import QueryDict
from yaml import load
from pathlib import Path
from urllib.parse import urlparse
import aiohttp
import re

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from api.services.base.connector import BaseConnector
from api.services.base.response import ErrorResponse, SuccessResponse, Response
from api.services.base.utils import camel_to_snake

endpoints = load(open(Path(__file__).parent / 'endpoints.yaml'), Loader)


class Connector(BaseConnector):
    """newsapi.org API connector.

    Uses v2 version.
    """

    BASE_URL = 'https://newsapi.org/v2/'

    def __init__(self, params: QueryDict):
        self._params = params
        self._session = aiohttp.ClientSession()

    async def _make_service_call(self, endpoint: str) -> dict:
        async with self._session:
            async with self._session.get(self.BASE_URL + endpoint, params=dict(**self._params)) as resp:
                return await resp.json()

    @staticmethod
    def _format_article(article: dict):
        """Format article item retrieved"""
        source = article.get('source', {})
        if source:
            article['source'] = source.get('name', None)

        url = article.get('url', '')
        parts = urlparse(url)
        host = f'{parts.scheme}://{parts.netloc}'
        article['url'] = url.lstrip(host)

        article['url_to_image'] = article.get('urlToImage', '')
        content = article.get('content', '')
        if content:
            article['content'] = re.sub(r'\r?\n', '', content)

        for key in list(article.keys()):
            new_key = camel_to_snake(key)
            if key != new_key:
                article[new_key] = article.pop(key)

    def _process_service_response(self, resp) -> Response:
        if resp.get('status', '') != 'ok' or 'articles' not in resp:
            return ErrorResponse(f'bad service api response: '
                                 f'{resp.get("status", "")} - {resp.get("message", "")}')

        articles = resp['articles']

        for article in articles:
            self._format_article(article)

        return SuccessResponse(articles)

    async def process_request(self) -> Response:
        endpoint = self._params.get('endpoint', None)
        if not endpoint:
            return ErrorResponse('no service endpoint found in request')
        if endpoint not in endpoints:
            return ErrorResponse(f'provided service endpoint "{endpoint}" is not supported')

        params = set(self._params)
        req_fields = set(endpoints[endpoint]['required_fields'] + ['endpoint'])
        if req_fields > params:
            return ErrorResponse('required fields not filled: ' + ', '.join(req_fields.difference(params)))

        all_fields = req_fields.union(set(endpoints[endpoint]['optional_fields']))
        if params > all_fields:
            return ErrorResponse('excessive fields in request: ' + ', '.join(params.difference(all_fields)))

        service_resp = await self._make_service_call(endpoint)

        # return SuccessResponse(service_resp['articles'])
        return self._process_service_response(service_resp)
