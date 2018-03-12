from django.http import JsonResponse
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi

def bad_request(request,exception,template_name='400.html'):
    error = ExceptionApi('Acesso negado HTTP 400![208]',exception)

    ApiConfig.loggerWarning(error)

    return JsonResponse({'message': str(error)},status=400)

def permission_denied(request,exception,template_name='403.html'):
    error = ExceptionApi('Permissão negada HTTP 403![206]',exception)

    ApiConfig.loggerWarning(error)

    return JsonResponse({'message': str(error)},status=403)

def page_not_found(request,exception,template_name='404.html'):
    error = ExceptionApi('Página não encontrada HTTP 404![205]',exception)

    ApiConfig.loggerWarning(error)

    return JsonResponse({'message': str(error)},status=404)

def server_error(request,template_name='500.html'):
    error = ExceptionApi('Erro interno HTTP 500![207]')

    ApiConfig.loggerWarning(error)

    return JsonResponse({'message': str(error)},status=500)
