from django.http import JsonResponse
from django.http.request import HttpRequest
from api.services.base import utils


async def api_call(request: HttpRequest, endpoint: str):
    """Retrieve GET parameters and process request with utilities"""
    res = await utils.process_api_call(endpoint, request.GET)
    return JsonResponse(res.dict())
