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
        name = request.GET.get('name',None)

        if person_id:
            try:
                try:
                    model_person = ModelPerson.objects.get(person_id=person_id)

                except Exception as error:
                    raise Exception('Nenhum registro de pessoa encontrado com este ID[76]')

                model_address = ModelAddress.objects.filter(person_id=model_person.person_id)

            except Exception as error:
                BusinessExceptionLog(request,model_login,
                    message=error,
                    trace=traceback.format_exc())

                return JsonResponse({'message': str(error)}, status=400)

            result = {
                'person_id': model_person.person_id,
                'parent_id': model_person.parent_id,
                'name': model_person.name,
                'cpf': model_person.cpf,
                'cnpj': model_person.cnpj,
                'email': model_person.email,
                'phone1': model_person.phone1,
                'phone2': model_person.phone2,
                'address': list(model_address.values(
                    'address_id','state','city','number','complement','invoice','delivery','date_create')),
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

        try:
            model_person = ModelPerson.objects.filter(
                login__profile_id__in=[
                    ModelLogin.PROFILE_DIRECTOR,
                    ModelLogin.PROFILE_CLIENT,]).order_by('-person_id')

            if name:
                model_person = model_person.filter(name__contains=name)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        paginator = Paginator(model_person, limit)

        try:
            person = paginator.page(page)
            person_total = model_person.count()
            person_has_next = person.has_next()
            person_has_previous = person.has_previous()

            person_data = person.object_list
            person_data = list(person_data.values(
                'person_id','name','cpf','cnpj','email','phone1','phone2'))

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': 'Erro na consulta de pessoa![25]'}, status=400)

        result = {
            'total': person_total,
            'limit': limit,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': person_has_next,
            'has_previous': person_has_previous,
            'data': person_data,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_person = ModelPerson.objects.create(request,model_login)

            model_login = ModelLogin.objects.create(request,model_login,model_person)

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                message=error,
                trace=traceback.format_exc())

            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'person_id': model_person.person_id,
            'parent_id': model_person.parent_id,
            'name': model_person.name,
            'cpf': model_person.cpf,
            'cnpj': model_person.cnpj,
            'email': model_person.email,
            'phone1': model_person.phone1,
            'phone2': model_person.phone2,
            'login': {
                'username': model_login.username,
                'verified': model_login.verified,
            }
        }

        return JsonResponse(result,status=200)
