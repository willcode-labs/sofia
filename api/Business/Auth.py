import datetime,traceback
from django.http import JsonResponse
from django.db import transaction
from api.apps import ApiConfig
from api.Model.Login import Login as ModelLogin
from api.Model.Merchant import Merchant as ModelMerchant
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog

class Auth():
    def __init__(self,request,**kwargs):
        self.request = request
        self.ip = request.META.get('REMOTE_ADDR',None)
        self.api_key = request.META.get('HTTP_API_KEY',None)
        self.client_api_key = request.META.get('HTTP_CLIENT_API_KEY',None)
        self.client_ip = request.META.get('HTTP_CLIENT_IP',None)
        self.profile_tuple = None
        self.client_verify = True

        if not self.ip:
            raise Exception('IP não encontrado![1]')

        if not self.api_key:
            raise Exception('Api key não encontrado![2]')

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.api_config = ApiConfig

    def authorize(self):
        try:
            model_login = ModelLogin.objects.get(
                token=self.api_key,)

        except Exception as error:
            raise Exception('Api key não autorizado![3]')

        if model_login.ip != self.ip:
            raise Exception('Ip de acesso do login difere de seu ip de origem![4]')

        if not model_login.verified:
            raise Exception('Login não verificado![5]')

        if model_login.profile_id not in (ModelLogin.PROFILE_ROOT,ModelLogin.PROFILE_MERCHANT,):
            raise Exception('Perfil não permitido![6]')

        if dict(ModelLogin.PROFILE_TUPLE)[model_login.profile_id] not in self.profile_tuple:
            raise Exception('Perfil não autorizado![7]')

        if model_login.date_expired < datetime.datetime.now().replace(tzinfo=None):
            raise Exception('Api key expirado![9]')

        model_login_client = None

        if self.client_verify:
            if not self.client_api_key or not self.client_ip:
                raise Exception('Dados insuficientes![36]')

            try:
                try:
                    model_login_client = ModelLogin.objects.get(
                        token=self.client_api_key,)

                except Exception as error:
                    raise Exception('Api key do cliente não encontrado![37]')

                if model_login_client.ip != self.client_ip:
                    raise Exception('Ip de acesso do login de cliente difere de seu ip de origem![38]')

                if not model_login_client.verified:
                    raise Exception('Login de cliente não verificado![39]')

                if model_login_client.person.parent_id != model_login.person_id:
                    raise Exception('Cliente não relacionado![40]')

                if model_login_client.profile_id not in (ModelLogin.PROFILE_CLIENT,):
                    raise Exception('Perfil de cliente não autorizado![41]')

                if model_login_client.date_expired.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
                    ModelLogin.objects.update(self.request,model_login,model_login_client,
                        token=None,
                        ip=None,
                        date_expired=None,)

                    raise Exception('Api key do cliente expirado![42]')

                date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

                model_login_client = ModelLogin.objects.update(self.request,model_login,model_login_client,
                    date_expired=date_expired,)

            except Exception as error:
                raise error

        return {
            'model_login': model_login,
            'model_login_client': model_login_client,
        }

    def auth(self,model_login):
        username = self.request.POST.get('username',None)
        password = self.request.POST.get('password',None)

        if not username or not password or not self.client_ip:
            raise Exception('Dados insuficientes![19]')

        try:
            model_login_client = ModelLogin.objects.get(
                username=username,
                password=password)

        except Exception as error:
            raise Exception('Login ou senha inválidos![20]')

        if model_login_client.verified != True:
            raise Exception('Login não verificado![21]')

        if model_login_client.profile_id not in (ModelLogin.PROFILE_CLIENT,):
            raise Exception('Tipo de login não autorizado![22]')

        try:
            token = ModelLogin.objects.tokenRecursive(self.ip)
            date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

            model_login_client = ModelLogin.objects.update(self.request,model_login,model_login_client,
                token=token,
                ip=self.client_ip,
                date_expired=date_expired,)

        except Exception as error:
            raise error

        return model_login_client

    def verify(self,model_login):
        if not self.client_api_key or not self.client_ip:
            raise Exception('Dados de cliente insuficientes![10]')

        try:
            model_login_client = ModelLogin.objects.get(
                token=self.client_api_key,)

        except Exception as error:
            raise Exception('Api key do cliente não encontrado![11]')

        if model_login_client.verified == True:
            raise Exception('Login de cliente já está verificado![12]')

        if model_login_client.person.parent_id != model_login.person_id:
            raise Exception('Cliente não relacionado![13]')

        if model_login_client.profile_id not in (ModelLogin.PROFILE_MERCHANT,ModelLogin.PROFILE_CLIENT,):
            raise Exception('Perfil de cliente não autorizado![14]')

        if model_login_client.profile_id in (ModelLogin.PROFILE_MERCHANT,ModelLogin.PROFILE_CLIENT,):
            try:
                token = ModelLogin.objects.tokenRecursive(self.client_ip)

                if model_login_client.profile_id == ModelLogin.PROFILE_MERCHANT:
                    try:
                        model_merchant = ModelMerchant.objects.filter(login=model_login_client).order_by('-login_id')[:1]
                        model_merchant = model_merchant[0]

                    except Exception as error:
                        raise Exception('Não há um registro de controle para este comerciante![17]')

                    if model_merchant.date_expired < datetime.datetime.now():
                        raise Exception('Comerciante expirado![18]')

                    date_expired = model_merchant.date_expired

                if model_login_client.profile_id == ModelLogin.PROFILE_CLIENT:
                    date_expired = datetime.datetime.now() + datetime.timedelta(minutes=self.api_config.login_time_duration_in_minutes)

                model_login_client = ModelLogin.objects.update(self.request,model_login,model_login_client,
                    token=token,
                    ip=self.client_ip,
                    date_expired=date_expired,
                    verified=True)

            except Exception as error:
                raise error

        return model_login_client

class DecoratorAuth(object):
    def __init__(self, **kwargs):
        self.profile = None
        self.client = True

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if self.client is None or not isinstance(self.client,bool):
            return JsonResponse(
                {'message': 'Tipo de valor invalido para validação de cliente![23]'},
                status=400)

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
                session_identifier = transaction.savepoint()

                business_auth = Auth(request,
                    profile_tuple=self.profile,
                    client_verify=self.client,)

                model_login_and_client = business_auth.authorize()

                transaction.savepoint_commit(session_identifier)

            except Exception as error:
                transaction.savepoint_rollback(session_identifier)

                return JsonResponse({'message': str(error)}, status=400)

            model_login = model_login_and_client['model_login']
            model_login_client = model_login_and_client['model_login_client']

            return function(request, model_login, model_login_client, *args, **kwargs)

        return wrap
