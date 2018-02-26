import datetime,traceback,logging
from django.http import JsonResponse
from django.db import transaction
from api.apps import ApiConfig
from api.Model.Login import Login as ModelLogin

LOGGER = logging.getLogger('sofia.api.error')

class Auth():
    def __init__(self,request,**kwargs):
        LOGGER.debug('########## Auth.__init__ ##########')

        self.request = request
        self.ip = request.META.get('REMOTE_ADDR',None)
        self.api_key = request.META.get('HTTP_API_KEY',None)
        self.profile_tuple = None

        if not self.ip:
            LOGGER.error('IP não encontrado![1]')

            raise Exception('IP não encontrado![1]')

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.api_config = ApiConfig

    def authorize(self):
        if not self.api_key:
            raise Exception('Api key não encontrado![2]')

        try:
            model_login = ModelLogin.objects.get(
                token=self.api_key,)

        except Exception as error:
            raise Exception('Api key não autorizado![3]')

        if not model_login.verified:
            raise Exception('Login não verificado![5]')

        if model_login.profile_id in (ModelLogin.PROFILE_ROOT,ModelLogin.PROFILE_DIRECTOR,):
            if model_login.ip != self.ip:
                raise Exception('Ip de acesso do login difere de seu ip de origem![4]')

        if model_login.profile_id not in (ModelLogin.PROFILE_ROOT,ModelLogin.PROFILE_DIRECTOR,ModelLogin.PROFILE_CLIENT,):
            raise Exception('Perfil não permitido![6]')

        if dict(ModelLogin.PROFILE_TUPLE)[model_login.profile_id] not in self.profile_tuple:
            raise Exception('Perfil não autorizado![7]')

        if model_login.date_expired.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
            raise Exception('Api key expirado![9]')

        if model_login.profile_id in (ModelLogin.PROFILE_CLIENT,):
            date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

            model_login = ModelLogin.objects.update(self.request,model_login,
                date_expired=date_expired,)

        return model_login

    def auth(self):
        username = self.request.POST.get('username',None)
        password = self.request.POST.get('password',None)

        if not username or not password:
            raise Exception('Dados insuficientes![19]')

        try:
            model_login = ModelLogin.objects.get(
                username=username,
                password=password)

        except Exception as error:
            raise Exception('Login ou senha inválidos![20]')

        if model_login.profile_id not in (ModelLogin.PROFILE_ROOT,ModelLogin.PROFILE_DIRECTOR,ModelLogin.PROFILE_CLIENT,):
            raise Exception('Tipo de login não autorizado![22]')

        if model_login.verified != True:
            raise Exception('Login não verificado![21]')

        token = ModelLogin.objects.tokenRecursive(self.ip)
        date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

        model_login = ModelLogin.objects.update(self.request,model_login,
            token=token,
            ip=self.ip,
            date_expired=date_expired,)

        return model_login

    def verify(self):
        api_key = self.request.GET.get('api_key',None)

        try:
            model_login = ModelLogin.objects.get(
                token=self.api_key,)

        except Exception as error:
            raise Exception('Api key não encontrado![11]')

        if model_login.profile_id not in (ModelLogin.PROFILE_CLIENT,):
            raise Exception('Perfil não autorizado![14]')

        if model_login.verified == True:
            raise Exception('Login já está verificado![12]')

        token = ModelLogin.objects.tokenRecursive(self.ip)
        date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

        model_login = ModelLogin.objects.update(self.request,model_login,
            token=token,
            ip=self.ip,
            date_expired=date_expired,
            verified=True)

        return model_login

class DecoratorAuth(object):
    def __init__(self, **kwargs):
        self.profile = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

    def __call__(self, function):
        @transaction.atomic
        def wrap(request, *args, **kwargs):
            if not self.profile or not isinstance(self.profile,tuple):
                return JsonResponse(
                    {'message': 'Perfil não configurado![15]'},
                    status=400)

            for item in self.profile:
                if item not in dict(ModelLogin.PROFILE_TUPLE).values():
                    return JsonResponse(
                        {'message': 'Perfil não identificado![16]'},
                        status=400)

            try:
                business_auth = Auth(request,profile_tuple=self.profile)

                model_login = business_auth.authorize()

            except Exception as error:
                return JsonResponse({'message': str(error)}, status=400)

            return function(request, model_login, *args, **kwargs)

        return wrap
