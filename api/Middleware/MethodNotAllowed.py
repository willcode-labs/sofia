from django.http import JsonResponse,HttpResponseNotAllowed
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi

class MethodNotAllowed:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response,HttpResponseNotAllowed):
            error = ExceptionApi('Método de requisição incorreto![209]')

            ApiConfig.loggerWarning(error)

            return JsonResponse({'message': str(error)},status=405)

        return response
