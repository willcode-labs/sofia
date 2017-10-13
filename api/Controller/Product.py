import json,traceback
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from api.apps import ApiConfig
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.DecoratorAuthRequired import decoratorAuthRequired as BusinessDecoratorAuthRequired
from api.Model.Product import Product as ModelProduct

@require_http_methods(['GET'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def filter(request,model_login):
    page = request.GET.get('page',None)
    name = request.GET.get('name',None)

    if not page:
        page = 1

    try:
        model_product = ModelProduct.objects.filter()

        if name:
            model_product = model_product.filter(name__contains=name)

    except Exception as error:
        BusinessExceptionLog(request,model_login,
            description='Erro de consulta para produto',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    paginator = Paginator(model_product, ApiConfig.query_row_limit)

    product = paginator.page(page)

    result = serializers.serialize('json', product)

    return JsonResponse(json.loads(result), safe=False,status=200)

@require_http_methods(['GET'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def getById(request,model_user):
    product_id = request.GET.get('product_id',None)

    try:
        model_product = ModelProduct.objects.get(
            product_id=product_id)

    except Exception as error:
        BusinessExceptionLog(request,
            user_id=model_user.user_id,
            description='Produto não encontrado',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'product_id': model_product.product_id,
        'name': model_product.name,
        'description': model_product.description,
        'code': model_product.code,
        'compound': model_product.compound,
        'unit_weight': model_product.unit_weight,
        'weight': model_product.weight,
        'width': model_product.width,
        'length': model_product.length,
        'height': model_product.height,
        'origin': model_product.origin,
        'gtin': model_product.gtin,
        'published': model_product.published,
    }

    return JsonResponse(result, safe=False,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def add(request,model_user):
    name = request.POST.get('name',None)
    description = request.POST.get('description',None)
    code = request.POST.get('code',None)
    compound = request.POST.get('compound',None)
    unit_weight = request.POST.get('unit_weight',None)
    weight = request.POST.get('weight',None)
    width = request.POST.get('width',None)
    length = request.POST.get('length',None)
    height = request.POST.get('height',None)
    origin = request.POST.get('origin',None)
    gtin = request.POST.get('gtin',None)

    try:
        session_identifier = transaction.savepoint()

        model_product = ModelProduct.objects.create(request,model_user,
            name=name,
            description=description,
            code=code,
            compound=compound,
            unit_weight=unit_weight,
            weight=weight,
            width=width,
            length=length,
            height=height,
            origin=origin,
            gtin=gtin,)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,
            user_id=model_user.user_id,
            description='Erro no cadastro de produto',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'product_id': model_product.product_id,
        'name': model_product.name,
        'description': model_product.description,
        'code': model_product.code,
        'compound': model_product.compound,
        'unit_weight': model_product.unit_weight,
        'weight': model_product.weight,
        'width': model_product.width,
        'length': model_product.length,
        'height': model_product.height,
        'origin': model_product.origin,
        'gtin': model_product.gtin,
        'published': model_product.published,
    }

    return JsonResponse(result, safe=False,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def update(request,model_user,product_id):
    name = request.POST.get('name',None)
    description = request.POST.get('description',None)
    code = request.POST.get('code',None)
    compound = request.POST.get('compound',None)
    unit_weight = request.POST.get('unit_weight',None)
    weight = request.POST.get('weight',None)
    width = request.POST.get('width',None)
    length = request.POST.get('length',None)
    height = request.POST.get('height',None)
    origin = request.POST.get('origin',None)
    gtin = request.POST.get('gtin',None)

    try:
        session_identifier = transaction.savepoint()

        model_product = ModelProduct.objects.update(request,model_user,
            product_id=product_id,
            name=name,
            description=description,
            code=code,
            compound=compound,
            unit_weight=unit_weight,
            weight=weight,
            width=width,
            length=length,
            height=height,
            origin=origin,
            gtin=gtin,)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,
            user_id=model_user.user_id,
            description='Erro na atualização de produto',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'product_id': model_product.product_id,
        'name': model_product.name,
        'description': model_product.description,
        'code': model_product.code,
        'compound': model_product.compound,
        'unit_weight': model_product.unit_weight,
        'weight': model_product.weight,
        'width': model_product.width,
        'length': model_product.length,
        'height': model_product.height,
        'origin': model_product.origin,
        'gtin': model_product.gtin,
        'published': model_product.published,
    }

    return JsonResponse(result, safe=False,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def delete(request,model_user,product_id):
    try:
        session_identifier = transaction.savepoint()

        model_product = ModelProduct.objects.delete(request,model_user,
            product_id=product_id,)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,
            user_id=model_user.user_id,
            description='Erro na remoção de produto',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'result': True
    }

    return JsonResponse(result, safe=False,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@BusinessDecoratorAuthRequired
def published(request,model_user):
    try:
        session_identifier = transaction.savepoint()

        model_product = ModelProduct.objects.published(request,model_user,
            product_id=product_id,)

        transaction.savepoint_commit(session_identifier)

    except Exception as error:
        transaction.savepoint_rollback(session_identifier)

        BusinessExceptionLog(request,
            user_id=model_user.user_id,
            description='Erro na publicação de produto',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'product_id': model_product.product_id,
        'name': model_product.name,
        'description': model_product.description,
        'code': model_product.code,
        'compound': model_product.compound,
        'unit_weight': model_product.unit_weight,
        'weight': model_product.weight,
        'width': model_product.width,
        'length': model_product.length,
        'height': model_product.height,
        'origin': model_product.origin,
        'gtin': model_product.gtin,
        'published': model_product.published,
    }

    return JsonResponse(result, safe=False,status=200)
