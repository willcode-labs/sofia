import json
from django.http import QueryDict
from django.http import HttpResponseBadRequest
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi

class RestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('POST','PUT','DELETE') and request.content_type != 'application/json':
            error = ExceptionApi('Tipo de request requer formato JSON[203]')

            ApiConfig.loggerWarning(error)

            return HttpResponseBadRequest(str(error))

        else:
            try:
                if request.method == 'POST':
                    request.POST = json.loads(request.body.decode('utf-8'))

                if request.method == 'PUT':
                    request.PUT = json.loads(request.body.decode('utf-8'))

                if request.method == 'DELETE':
                    request.DELETE = json.loads(request.body.decode('utf-8'))

            except Exception as error:
                ApiConfig.loggerCritical(error)

                return HttpResponseBadRequest('Erro em parsear dados de request[204]')

        response = self.get_response(request)

        return response