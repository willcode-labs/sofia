import datetime,logging
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist
from api.apps import ApiConfig
from api.Exception.Api import Api as ExceptionApi
from api.Model.App import App as ModelApp
from api.Model.Token import Token as ModelToken
from api.Model.Person import Person as ModelPerson

class Auth():
    def __init__(self,request,**kwargs):
        self.request = request
        self.ip = request.META.get('REMOTE_ADDR',None)
        self.token = request.META.get('HTTP_TOKEN',None)
        self.apikey = request.META.get('HTTP_APIKEY',None)
        self.profile_tuple = None

        if not self.ip:
            raise ExceptionApi('IP não encontrado![1]')

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.api_config = ApiConfig

    def authorize(self) -> ModelToken:
        if not self.apikey:
            raise ExceptionApi('ApiKey não encontrado![164]')

        if not self.token:
            raise ExceptionApi('Token não encontrado![2]')

        try:
            model_app = ModelApp.objects.get(
                apikey=self.apikey,
                active=True)

        except Exception as error:
            raise ExceptionApi('Apikey não autorizado![165]',error)

        try:
            model_token = ModelToken.objects.get(
                token=self.token,
                app=model_app,)

        except Exception as error:
            raise ExceptionApi('Token não autorizado![3]',error)

        if not model_token.person.verified:
            raise ExceptionApi('Usuário não verificado![5]')

        if model_app.profile_id not in (ModelApp.PROFILE_ROOT,ModelApp.PROFILE_DIRECTOR,ModelApp.PROFILE_CLIENT,):
            raise ExceptionApi('Perfil não permitido![6]')

        if model_token.ip != self.ip:
            raise ExceptionApi('Ip de acesso difere de seu ip de origem![4]')

        if dict(ModelApp.PROFILE_TUPLE)[model_app.profile_id] not in self.profile_tuple:
            raise ExceptionApi('Perfil não autorizado![7]')

        if model_token.date_expire.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
            raise ExceptionApi('Token expirado![9]')

        if model_app.profile_id in (ModelApp.PROFILE_CLIENT,):
            date_expire = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.token_time_client)

            model_token.date_expire = date_expire
            model_token.save()

        return model_token

    def auth(self) -> ModelToken:
        if not self.apikey:
            raise ExceptionApi('ApiKey não encontrado![172]')

        username = self.request.POST.get('username',None)
        password = self.request.POST.get('password',None)

        if not username or not password:
            raise ExceptionApi('Dados insuficientes![19]')

        try:
            model_app = ModelApp.objects.get(
                apikey=self.apikey,
                profile_id__in=[
                    ModelApp.PROFILE_ROOT,
                    ModelApp.PROFILE_DIRECTOR,
                    ModelApp.PROFILE_CLIENT])

        except Exception as error:
            raise ExceptionApi('Apikey inválida![20]',error)

        if model_app.active != True:
            raise ExceptionApi('ApiKey dasativada![175]')

        try:
            model_person = ModelPerson.objects.get(
                username=username,
                password=password)

        except Exception as error:
            raise ExceptionApi('Usuário não encontrado![173]',error)

        if model_person.verified != True:
            raise ExceptionApi('Usuário não verificado![21]')

        try:
            model_token = ModelToken.objects.get(
                person=model_person,
                app=model_app,
                ip=self.ip)

        except MultipleObjectsReturned as error:
            raise ExceptionApi('Erro crítico![174]',error)

        except ObjectDoesNotExist as error:
            model_token = None

        if model_app.profile_id in (ModelApp.PROFILE_CLIENT,):
            date_expire = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.token_time_client)

        if model_app.profile_id in (ModelApp.PROFILE_ROOT,ModelApp.PROFILE_DIRECTOR,):
            date_expire = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.token_time_admin)

        if not model_token:
            model_token = ModelToken(
                token=ModelToken.objects.tokenRecursive(),
                person=model_person,
                app=model_app,
                ip=self.ip)

        model_token.date_expire = date_expire

        model_token = ModelToken.objects.auth(self.request,model_token)

        return model_token

    def verify(self) -> ModelToken:
        if not self.token:
            raise ExceptionApi('Token não encontrado![166]')

        try:
            model_token = ModelToken.objects.get(
                token=self.token,
                date_expire__gte=datetime.datetime.now(),)

        except Exception as error:
            raise ExceptionApi('Token não autorizado![11]',error)

        if model_token.app.profile_id not in (ModelApp.PROFILE_CLIENT,):
            raise ExceptionApi('Perfil não autorizado![14]')

        if model_token.app.active == False:
            raise ExceptionApi('ApiKey desativada![167]')

        if model_token.person.verified == True:
            raise ExceptionApi('Usuário já verificado![12]')

        token = ModelToken.objects.tokenRecursive()
        date_expire = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.token_time_client)

        model_token.token = token
        model_token.ip = self.ip
        model_token.date_expire = date_expire

        model_token = ModelToken.objects.verify(
            self.request,
            model_token)

        model_token.person.verified = True

        model_person = ModelPerson.objects.verify(
            self.request,
            model_token,
            model_token.person)

        return model_token

class DecoratorAuth(object):
    def __init__(self, **kwargs):
        self.profile = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

    def __call__(self, function):
        @transaction.atomic
        def wrap(request, *args, **kwargs):
            if not self.profile or not isinstance(self.profile,tuple):
                error = 'Perfil não configurado![15]'

                ApiConfig.loggerWarning(error)

                return JsonResponse(
                    {'message': error},
                    status=400)

            for item in self.profile:
                if item not in dict(ModelApp.PROFILE_TUPLE).values():
                    error = 'Perfil não identificado![16]'

                    ApiConfig.loggerWarning(error)

                    return JsonResponse(
                        {'message': error},
                        status=400)

            try:
                business_auth = Auth(
                    request,
                    profile_tuple=self.profile)

                model_token = business_auth.authorize()

            except ExceptionApi as error:
                ApiConfig.loggerWarning(error)

                return JsonResponse({'message': str(error)},status=400)

            except Exception as error:
                ApiConfig.loggerCritical(error)

                return JsonResponse({'message': 'Erro interno![178]'},status=400)

            return function(request,model_token,*args,**kwargs)

        return wrap
