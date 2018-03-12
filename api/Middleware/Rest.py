import json
from django.http import JsonResponse
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi

class Rest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('POST','PUT','DELETE') and request.content_type != 'application/json':
            error = ExceptionApi('Tipo de request requer formato JSON[203]')

            ApiConfig.loggerWarning(error)

            return JsonResponse({'message': str(error)},status=400)

        else:
            try:
                if request.method == 'POST':
                    request.POST = json.loads(request.body.decode('utf-8'))

                if request.method == 'PUT':
                    request.PUT = json.loads(request.body.decode('utf-8'))

                if request.method == 'DELETE':
                    request.DELETE = json.loads(request.body.decode('utf-8'))

            except Exception as error:
                error = ExceptionApi('Erro em parsear dados de request[204]',error)

                ApiConfig.loggerCritical(error)

                return JsonResponse({'message': str(error)},status=500)

        response = self.get_response(request)

        return response
