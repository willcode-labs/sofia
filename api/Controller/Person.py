import json,traceback,re
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from api.apps import ApiConfig
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth
from api.Model.Login import Login as ModelLogin
from api.Model.Person import Person as ModelPerson
from api.Model.Address import Address as ModelAddress

@require_http_methods(['GET'])
@csrf_exempt
@BusinessDecoratorAuth(profile=('merchant',),client=False)
def filter(request,model_login,model_login_client):
    page = request.GET.get('page',None)
    limit = request.GET.get('limit',None)
    name = request.GET.get('name',None)

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
            parent_id=model_login.person_id,
            login__profile_id__in=[ModelLogin.PROFILE_CLIENT,])

        if name:
            model_person = model_person.filter(name__contains=name)

    except Exception as error:
        message = 'Erro na consulta de pessoa![24]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': message}, status=400)

    paginator = Paginator(model_person, limit)

    try:
        person = paginator.page(page)
        person_total = model_person.count()
        perso_has_next = person.has_next()
        person_has_previous = person.has_previous()

        person_data = person.object_list
        person_data = list(person_data.values(
            'person_id','name','cpf','email','phone1','phone2'))

    except Exception as error:
        message = 'Erro na consulta de pessoa![25]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': message}, status=400)

    result = {
        'total': person_total,
        'limit': limit,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'has_next': perso_has_next,
        'has_previous': person_has_previous,
        'data': person_data,}

    return JsonResponse(result,status=200)

@require_http_methods(['GET'])
@csrf_exempt
@BusinessDecoratorAuth(profile=('merchant',))
def getById(request,model_login,model_login_client):
    try:
        model_person = ModelPerson.objects.get(person_id=model_login_client.person_id)

        model_address = ModelAddress.objects.filter(person_id=model_person.person_id)

    except Exception as error:
        message = 'Erro ao tentar encontrar pessoa![26]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'person_id': model_person.person_id,
        'parent_id': model_person.parent_id,
        'name': model_person.name,
        'cpf': model_person.cpf,
        'email': model_person.email,
        'phone1': model_person.phone1,
        'phone2': model_person.phone2,
        'address': list(model_address.values(
            'address_id','state','city','number','complement','invoice','delivery')),
    }

    return JsonResponse(result,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
@BusinessDecoratorAuth(profile=('merchant',),client=False)
def add(request,model_login,model_login_client):
    name = request.POST.get('name',None)
    cpf = request.POST.get('cpf',None)
    email = request.POST.get('email',None)
    phone1 = request.POST.get('phone1',None)
    phone2 = request.POST.get('phone2',None)

    try:
        model_person = ModelPerson.objects.create(request,model_login,
            name=name,
            cpf=cpf,
            email=email,
            phone1=phone1,
            phone2=phone2)

        model_login_client = ModelLogin.objects.create(request,model_login,model_person)

    except Exception as error:
        message = 'Erro na criação de pessoa![29]'

        BusinessExceptionLog(request,model_login,model_login_client,
            description=message,
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'person_id': model_person.person_id,
        'parent_id': model_person.parent_id,
        'name': model_person.name,
        'cpf': model_person.cpf,
        'email': model_person.email,
        'phone1': model_person.phone1,
        'phone2': model_person.phone2,
        'login': {
            'username': model_login_client.username,
            'verified': model_login_client.verified,
        }
    }

    return JsonResponse(result,status=200)

@require_http_methods(['POST'])
@csrf_exempt
@transaction.atomic
@BusinessDecoratorAuth(profile=('merchant',))
def addressAdd(request,model_login,model_login_client):
    state = request.POST.get('state',None)
    city = request.POST.get('city',None)
    number = request.POST.get('number',None)
    complement = request.POST.get('complement',None)
    invoice = request.POST.get('invoice',None)
    delivery = request.POST.get('delivery',None)

    try:
        model_person = ModelPerson.objects.get(person_id=model_login_client.person_id)

        model_address = ModelAddress.objects.create(request,model_login,model_person,
            state=state,
            city=city,
            number=number,
            complement=complement,
            invoice=invoice,
            delivery=delivery)

    except Exception as error:
        BusinessExceptionLog(request,model_login,model_login_client,
            description='Erro na criação de endereço',
            message=error,
            trace=traceback.format_exc())

        return JsonResponse({'message': str(error)}, status=400)

    result = {
        'address_id': model_address.address_id,
        'person_id': model_person.person_id,
        'state': model_address.state,
        'city': model_address.city,
        'number': model_address.number,
        'complement': model_address.complement,
        'invoice': model_address.invoice,
        'delivery': model_address.delivery,
    }

    return JsonResponse(result,status=200)
#
# @require_http_methods(['GET'])
# @csrf_exempt
# @BusinessDecoratorAuthRequired
# def addressById(request,model_login,person_id,address_id):
#     try:
#         model_address = ModelAddress.objects.get(
#             address=address_id,)
#
#     except Exception as error:
#         BusinessExceptionLog(request,model_login,
#             description='Registro não encontrado',
#             message=error,
#             trace=traceback.format_exc())
#
#         return JsonResponse({'message': str(error)}, status=400)
#
#     result = {
#         'address_id': model_address.address_id,
#         'person_id': model_address.person_id,
#         'state': model_address.state,
#         'city': model_address.city,
#         'number': model_address.number,
#         'complement': model_address.complement,
#         'invoice': model_address.invoice,
#         'delivery': model_address.delivery
#     }
#
#     return JsonResponse(result, safe=False,status=200)
#
# @require_http_methods(['GET'])
# @csrf_exempt
# @BusinessDecoratorAuthRequired
# def addressFilter(request,model_login,person_id):
#     page = request.GET.get('page',None)
#     state = request.GET.get('state',None)
#     city = request.GET.get('city',None)
#     number = request.GET.get('number',None)
#     complement = request.GET.get('complement',None)
#     invoice = request.GET.get('invoice',None)
#     delivery = request.GET.get('delivery',None)
#
#     if not page:
#         page = 1
#
#     try:
#         model_address = ModelAddress.objects.filter(person=person_id)
#
#         if city:
#             model_address = model_address.filter(city__contains=city)
#
#         if state:
#             model_address = model_address.objects.filter(state__contains=state)
#
#         if number:
#             model_address = model_address.objects.filter(number__contains=number)
#
#         if complement:
#             model_address = model_address.objects.filter(complement__contains=complement)
#
#         if invoice:
#             model_address = model_address.objects.filter(invoice=invoice)
#
#         if delivery:
#             model_address = model_address.objects.filter(delivery=delivery)
#
#     except Exception as error:
#         BusinessExceptionLog(request,model_login,
#             description='Registro não encontrado',
#             message=error,
#             trace=traceback.format_exc())
#
#         return JsonResponse({'message': str(error)}, status=400)
#
#     paginator = Paginator(model_address, ApiConfig.query_row_limit)
#
#     address = paginator.page(page)
#
#     result = serializers.serialize('json', address)
#
#     return JsonResponse(json.loads(result), safe=False,status=200)
#
# @require_http_methods(['POST'])
# @csrf_exempt
# @transaction.atomic
# @BusinessDecoratorAuthRequired
# def addressUpdate(request,model_login,person_id,address_id):
#     state = request.GET.get('state',None)
#     city = request.GET.get('city',None)
#     number = request.GET.get('number',None)
#     complement = request.GET.get('complement',None)
#     invoice = request.GET.get('invoice',None)
#     delivery = request.GET.get('delivery',None)
#
#     try:
#         session_identifier = transaction.savepoint()
#
#         model_person = ModelPerson.objects.get(person_id=person_id)
#
#         model_address = ModelAddress.objects.update(request,model_login,model_person,
#             address_id=address_id,
#             state=state,
#             city=city,
#             number=number,
#             complement=complement,
#             invoice=invoice,
#             delivery=delivery)
#
#         transaction.savepoint_commit(session_identifier)
#
#     except Exception as error:
#         transaction.savepoint_rollback(session_identifier)
#
#         BusinessExceptionLog(request,model_login,
#             description='Erro na atualização de endereço',
#             message=error,
#             trace=traceback.format_exc())
#
#         return JsonResponse({'message': str(error)}, status=400)
#
#     result = {
#         'address_id': model_address.address_id,
#         'person_id': model_person.person_id,
#         'state': model_address.state,
#         'city': model_address.city,
#         'number': model_address.number,
#         'complement': model_address.complement,
#         'invoice': model_address.invoice,
#         'delivery': model_address.delivery,
#     }
#
#     return JsonResponse(result,safe=False,status=200)
#
# @require_http_methods(['POST'])
# @csrf_exempt
# @transaction.atomic
# @BusinessDecoratorAuthRequired
# def addressDelete(request,model_login,person_id,address_id):
#     try:
#         session_identifier = transaction.savepoint()
#
#         model_person = ModelPerson.objects.get(person_id=person_id)
#
#         model_address = ModelAddress.objects.delete(request,model_login,model_person,
#             address_id=address_id,)
#
#         transaction.savepoint_commit(session_identifier)
#
#     except Exception as error:
#         transaction.savepoint_rollback(session_identifier)
#
#         BusinessExceptionLog(request,model_login,
#             description='Erro na remoção de endereço',
#             message=error,
#             trace=traceback.format_exc())
#
#         return JsonResponse({'message': str(error)}, status=400)
#
#     result = {
#         'result': True
#     }
#
#     return JsonResponse(result,safe=False,status=200)
