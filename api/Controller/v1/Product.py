import json,re
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db import transaction
from api.apps import ApiConfig
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth
from api.Model.Product import Product as ModelProduct

class EndPoint(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        page = request.GET.get('page',None)
        limit = request.GET.get('limit',None)
        name = request.GET.get('name',None)
        product_id = request.GET.get('product_id',None)

        if product_id:
            try:
                model_product = ModelProduct.objects.get(
                    product_id=product_id)

            except Exception as error:
                return JsonResponse({'message': 'Nenhum registro encontrado para este product_id[87]'}, status=400)

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
                'quantity': model_product.quantity,
                'published': model_product.published,
            }

            return JsonResponse(result, safe=False,status=200)

        if page and re.match(r'^[0-9]+$', str(page)) and int(page) >= 1:
            page = int(page)

        else:
            page = 1

        if limit and re.match(r'^[0-9]+$', str(limit)) and int(limit) >= 1:
            limit = int(limit)

        else:
            limit = ApiConfig.query_row_limit

        try:
            model_product = ModelProduct.objects.filter()

            if name:
                model_product = model_product.filter(name__icontains=name)

        except Exception as error:
            return JsonResponse({'message': 'Erro na consulta de produto[88]'}, status=400)

        paginator = Paginator(model_product, limit)

        try:
            product = paginator.page(page)
            product_total = model_product.count()
            product_has_next = product.has_next()
            product_has_previous = product.has_previous()

            product_data = product.object_list
            product_data = list(product_data.values(
                'product_id','name','description','code','compound','unit_weight',
                'weight','width','length','height','origin','gtin','published','quantity'))

        except Exception as error:
            return JsonResponse({'message': 'Nenhum registro encontrado![80]'}, status=400)

        result = {
            'total': product_total,
            'limit': limit,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': product_has_next,
            'has_previous': product_has_previous,
            'data': product_data,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_product = ModelProduct.objects.create(
                request,
                model_login)

        except Exception as error:
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
            'quantity': model_product.quantity,
            'published': model_product.published,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(self,request,model_login,*args,**kwargs):
        try:
            model_product = ModelProduct.objects.update(
                request,
                model_login)

        except Exception as error:
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
            'quantity': model_product.quantity,
            'published': model_product.published,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def delete(self,request,model_login,*args,**kwargs):
        try:
            model_product = ModelProduct.objects.delete(
                request,
                model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'result': True
        }

        return JsonResponse(result,status=200)

class Publish(View):
    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(self,request,model_login,*args,**kwargs):
        try:
            model_product = ModelProduct.objects.publish(
                request,
                model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'result': True
        }

        return JsonResponse(result,status=200)
