import json,traceback,re
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
from api.Model.Login import Login as ModelLogin
from api.Model.Person import Person as ModelPerson
from api.Model.Address import Address as ModelAddress

class EndPoint(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        page = request.GET.get('page',None)
        limit = request.GET.get('limit',None)
        person_id = request.GET.get('person_id',None)
        state = request.GET.get('state',None)
        city = request.GET.get('city',None)
        number = request.GET.get('number',None)
        complement = request.GET.get('complement',None)
        invoice = request.GET.get('invoice',None)
        delivery = request.GET.get('delivery',None)

        if person_id:
            try:
                model_address = ModelAddress.objects.get(
                    address_id=address_id,)

            except Exception as error:
                BusinessExceptionLog(request,model_login,
                    message=error,
                    trace=traceback.format_exc())

                return JsonResponse({'message': str(error)}, status=400)

            result = {
                'address_id': model_address.address_id,
                'person_id': model_address.person_id,
                'state': model_address.state,
                'city': model_address.city,
                'number': model_address.number,
                'complement': model_address.complement,
                'invoice': model_address.invoice,
                'delivery': model_address.delivery,
                'date_create': model_address.date_create,
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

        if invoice not in ['0','1'] or delivery not in ['0','1']:
            error = Exception('Valor incorreto![55]')

            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        if invoice == '0':
            invoice = False

        else:
            invoice = True

        if delivery == '0':
            delivery = False

        else:
            delivery = True

        try:
            model_address = ModelAddress.objects.filter()

            if person_id:
                model_address = model_address.filter(person_id=person_id)

            if city:
                model_address = model_address.filter(city__contains=city)

            if state:
                model_address = model_address.filter(state__contains=state)

            if number:
                model_address = model_address.filter(number__contains=number)

            if complement:
                model_address = model_address.filter(complement__contains=complement)

            if invoice:
                model_address = model_address.filter(invoice=invoice)

            if delivery:
                model_address = model_address.filter(delivery=delivery)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        paginator = Paginator(model_address, limit)

        try:
            address = paginator.page(page)
            address_total = model_address.count()
            address_has_next = address.has_next()
            address_has_previous = address.has_previous()

            address_data = address.object_list
            address_data = list(address_data.values(
                'address_id','person_id','state','city','number',
                'complement','invoice','delivery','date_create'))

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'total': address_total,
            'limit': limit,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': address_has_next,
            'has_previous': address_has_previous,
            'data': address_data,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_address = ModelAddress.objects.create(request,model_login)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'address_id': model_address.address_id,
            'person_id': model_address.person.person_id,
            'state': model_address.state,
            'city': model_address.city,
            'number': model_address.number,
            'complement': model_address.complement,
            'invoice': model_address.invoice,
            'delivery': model_address.delivery,
            'date_create': model_address.date_create,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(request,model_login):
        try:
            model_address = ModelAddress.objects.update(request,model_login)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'address_id': model_address.address_id,
            'person_id': model_address.person.person_id,
            'state': model_address.state,
            'city': model_address.city,
            'number': model_address.number,
            'complement': model_address.complement,
            'invoice': model_address.invoice,
            'delivery': model_address.delivery,
            'date_create': model_address.date_create,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def delete(request,model_login):
        try:
            model_address = ModelAddress.objects.delete(request,model_login)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'result': True
        }

        return JsonResponse(result,status=200)
