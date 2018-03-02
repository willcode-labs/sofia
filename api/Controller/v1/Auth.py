import traceback,logging
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db import transaction
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi
from api.Business.Auth import Auth as BusinessAuth

class VerifyClient(View):
    @csrf_exempt
    @transaction.atomic
    def post(self,request,*args,**kwargs):
        try:
            business_auth = BusinessAuth(request)

            model_token = business_auth.verify()

        except ExceptionApi as error:
            ApiConfig.loggerWarning(error)

            return JsonResponse({'message': str(error)},status=400)

        except Exception as error:
            ApiConfig.loggerCritical(error)

            return JsonResponse({'message': 'Erro interno![170]'},status=400)

        result = {
            'token': model_token.token,
            'date_expire': model_token.date_expire.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse(result,status=200)

class Auth(View):
    @csrf_exempt
    @transaction.atomic
    def post(self,request,*args,**kwargs):
        try:
            business_auth = BusinessAuth(request)

            model_token = business_auth.auth()

        except ExceptionApi as error:
            ApiConfig.loggerWarning(error)

            return JsonResponse({'message': str(error)},status=400)

        except Exception as error:
            ApiConfig.loggerCritical(error)

            return JsonResponse({'message': 'Erro interno![171]'},status=400)

        result = {
            'token': model_token.token,
            'date_expire': model_token.date_expire.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse(result,status=200)
