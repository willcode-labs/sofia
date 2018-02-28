import json,re
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db import transaction
from api.apps import ApiConfig
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth
from api.Model.Package import Package as ModelPackage

class EndPoint(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        page = request.GET.get('page',None)
        limit = request.GET.get('limit',None)
        package_id = request.GET.get('package_id',None)
        name = request.GET.get('name',None)
        status = request.GET.get('status',None)

        if package_id:
            try:
                model_package = ModelPackage.objects.get(
                    package_id=package_id,)

            except Exception as error:
                return JsonResponse({'message': 'Registro de entrega não encontrado![130]'}, status=400)

            result = {
                'delivery_id': model_delivery.delivery_id,
                'name': model_delivery.name,
                'description': model_delivery.description,
                'rate': model_delivery.rate,
                'status': model_delivery.status,
            }

            return JsonResponse(result,status=200)

        if page and re.match(r'^[0-9]+$', str(page)) and int(page) >= 1:
            page = int(page)

        else:
            page = 1

        if limit and re.match(r'^[0-9]+$', str(limit)) and int(limit) >= 1:
            limit = int(limit)

        else:
            limit = ApiConfig.query_row_limit

        if status and status not in dict(Delivery.STATUS_LIST).keys():
            raise Exception('Status incorreto![133]')

        try:
            model_delivery = ModelDelivery.objects.filter()

            if name:
                model_delivery = model_delivery.filter(name__icontains=name)

            if status:
                model_delivery = model_delivery.filter(status=status)

        except Exception as error:
            return JsonResponse({'message': 'Registros de entrega não encontrado![131]'}, status=400)

        paginator = Paginator(model_delivery, limit)

        try:
            delivery = paginator.page(page)
            delivery_total = model_delivery.count()
            delivery_has_next = delivery.has_next()
            delivery_has_previous = delivery.has_previous()

            delivery_data = delivery.object_list
            delivery_data = list(delivery_data.values(
                'delivery_id','name','description','rate','status',))

        except Exception as error:
            return JsonResponse({'message': 'Nenhum registro encontrado![132]'}, status=400)

        result = {
            'total': delivery_total,
            'limit': limit,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': delivery_has_next,
            'has_previous': delivery_has_previous,
            'data': delivery_data,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.create(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'delivery_id': model_delivery.delivery_id,
            'name': model_delivery.name,
            'description': model_delivery.description,
            'rate': model_delivery.status,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.update(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'delivery_id': model_delivery.delivery_id,
            'name': model_delivery.name,
            'description': model_delivery.description,
            'rate': model_delivery.status,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def delete(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.delete(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'result': True
        }

        return JsonResponse(result,status=200)
