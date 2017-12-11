import traceback
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db import transaction
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.Auth import Auth as BusinessAuth

class Verify(View):
    @csrf_exempt
    @transaction.atomic
    def post(self,request,*args,**kwargs):
        try:
            business_auth = BusinessAuth(request)

            model_login = business_auth.verify()

        except Exception as error:
            BusinessExceptionLog(request,None,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'token': model_login.token,
            'date_expired': model_login.date_expired,
        }

        return JsonResponse(result, status=200)

class Auth(View):
    @csrf_exempt
    @transaction.atomic
    def post(self,request,*args,**kwargs):
        try:
            business_auth = BusinessAuth(request)

            model_login = business_auth.auth()

        except Exception as error:
            BusinessExceptionLog(request,None,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'token': model_login.token,
            'date_expired': model_login.date_expired,
        }

        return JsonResponse(result, status=200)
