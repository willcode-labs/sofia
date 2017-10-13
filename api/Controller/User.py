import traceback
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.Auth import Auth as BusinessAuth

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
def verify(request):
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)

    try:
        session_identifier = transaction.savepoint()

        business_auth = BusinessAuth(request,
            username=username,
            password=password,)

        model_user = business_auth.verify()

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,None,
            description='Erro de autenticação',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'token': model_user.token,
        'date_expired': model_user.date_expired,
    }

    return JsonResponse(result, status=200)

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
def auth(request):
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)

    try:
        session_identifier = transaction.savepoint()

        business_auth = BusinessAuth(request,
            username=username,
            password=password,)

        model_user = business_auth.auth()

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,None,
            description='Erro de autenticação',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'token': model_user.token,
        'date_expired': model_user.date_expired,
    }

    return JsonResponse(result, status=200)

@require_http_methods(['GET'])
@csrf_exempt
@transaction.atomic
def logout(request):
    try:
        session_identifier = transaction.savepoint()

        business_auth = BusinessAuth(request)
        business_auth.logout()

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,None,
            description='Erro na remoção do login',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'result': True
    }

    return JsonResponse(result, status=200)
