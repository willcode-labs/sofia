import json
from django.http import QueryDict
from django.http import HttpResponseBadRequest

class RestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('POST','PUT') and request.content_type == 'application/json':
            try:
                if request.method == 'POST':
                    request.POST = json.loads(request.body.decode('utf-8'))

                if request.method == 'PUT':
                    request.PUT = json.loads(request.body.decode('utf-8'))

            except Exception as error:
                return HttpResponseBadRequest('Unable to parse JSON data. Error : {0}[83]'.format(error))

        response = self.get_response(request)

        return response