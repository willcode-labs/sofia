import json,traceback
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db import transaction
from api.apps import ApiConfig
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth
from api.Model.Product import Product as ModelProduct

class EndPoint(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        page = request.GET.get('page',None)
        name = request.GET.get('name',None)
        product_id = request.GET.get('product_id',None)

        if product_id:
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

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_product = ModelProduct.objects.create(
                request,
                model_login)

        except Exception as error:
            BusinessExceptionLog(request,model_login,model_login_client,
                description='Erro na cadastro de produto!',
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
            'date_create': model_product.date_create,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(self,request,model_login,*args,**kwargs):
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

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def delete(self,request,model_login,*args,**kwargs):
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

@require_http_methods(['PUT'])
@csrf_exempt
@transaction.atomic
@BusinessDecoratorAuth(profile=('root','director',))
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
