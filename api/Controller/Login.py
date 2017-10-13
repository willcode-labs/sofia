import traceback
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.Auth import Auth as BusinessAuth
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
@BusinessDecoratorAuth(profile=('root','merchant',),client=False)
def verify(request,model_login,model_login_client):
    try:
        session_identifier = transaction.savepoint()

        business_auth = BusinessAuth(request)

        model_login_client = business_auth.verify(model_login)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        message = 'Erro de verificação do login![27]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'client_token': model_login_client.token,
        'client_date_expired': model_login_client.date_expired,
    }

    return JsonResponse(result, status=200)

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
@BusinessDecoratorAuth(profile=('merchant',),client=False)
def auth(request,model_login,model_login_client):
    try:
        session_identifier = transaction.savepoint()

        business_auth = BusinessAuth(request)

        model_login_client = business_auth.auth(model_login)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        message = 'Erro de autenticação do login![28]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'client_token': model_login_client.token,
        'client_date_expired': model_login_client.date_expired,
    }

    return JsonResponse(result, status=200)
