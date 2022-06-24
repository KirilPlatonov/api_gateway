from django.http import JsonResponse


def api_call(request, endpoint):
    return JsonResponse({endpoint: 'Hello world!'})
