import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.App import App as ModelApp
from api.Model.Token import Token as ModelToken

class TestControllerAuth(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        # Person ROOT
        self.model_person_root = ModelPerson(
            profile_id=ModelApp.PROFILE_ROOT,
            name='William Borba ROOT',
            cpf='00000000001',
            cnpj='00000000001',
            email='emailroot@test.com',
            phone1='99123456789',
            phone2=None,
            username='wborba_root',
            password='12345678',
            verified=True)

        self.model_person_root.save()

        self.model_app_root = ModelApp(
            profile_id=ModelApp.PROFILE_ROOT,
            apikey='apikey-root',
            name='ROOT APIKEY',
            describe='APIKEY for ROOT',
            active=True)

        self.model_app_root.save()

        self.model_token_root = ModelToken(
            person=self.model_person_root,
            app=self.model_app_root,
            token='token-root',
            ip='127.0.0.1',
            date_expire=datetime.datetime.now() + datetime.timedelta(days=30))

        self.model_token_root.save()

        # Person DIRECTOR
        self.model_person_director = ModelPerson(
            profile_id=ModelApp.PROFILE_DIRECTOR,
            name='William Borba DIRECTOR',
            cpf='00000000002',
            cnpj='00000000002',
            email='emaildirector@test.com',
            phone1='99123456788',
            phone2=None,
            username='wborba_director',
            password='12345678',
            verified=True)

        self.model_person_director.save()

        self.model_app_director = ModelApp(
            profile_id=ModelApp.PROFILE_DIRECTOR,
            apikey='apikey-director',
            name='DIRECTOR APIKEY',
            describe='APIKEY for DIRECTOR',
            active=True)

        self.model_app_director.save()

        self.model_token_director = ModelToken(
            person=self.model_person_director,
            app=self.model_app_director,
            token='token-director',
            ip='127.0.0.2',
            date_expire=datetime.datetime.now() + datetime.timedelta(days=30))

        self.model_token_director.save()

        # Person CLIENT
        self.model_person_client = ModelPerson(
            profile_id=ModelPerson.PROFILE_CLIENT,
            name='William Borba CLIENT',
            cpf='00000000003',
            cnpj='00000000003',
            email='emailclient@test.com',
            phone1='99123456788',
            phone2=None,
            username='wborba_client',
            password='12345678',
            verified=True)

        self.model_person_client.save()

        self.model_app_client = ModelApp(
            profile_id=ModelApp.PROFILE_CLIENT,
            apikey='apikey-client',
            name='CLIENT APIKEY',
            describe='APIKEY for CLIENT',
            active=True)

        self.model_app_client.save()

        self.model_token_client = ModelToken(
            person=self.model_person_client,
            app=self.model_app_client,
            token='token-client',
            ip='127.0.0.3',
            date_expire=datetime.datetime.now() + datetime.timedelta(minutes=ApiConfig.token_time_client))

        self.model_token_client.save()

    def test_auth_verify_ip_not_found(self):
        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=None,
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'IP não encontrado![1]')

    def test_auth_verify_token_not_found(self):
        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não encontrado![166]')

    def test_auth_verify_token_unauthorized(self):
        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN='1')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![11]')

    def test_auth_root_verify_profile_unauthorized(self):
        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_root.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_auth_director_verify_profile_unauthorized(self):
        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_auth_client_verify_token_unauthorized_date_expire(self):
        self.model_token_client.date_expire = datetime.datetime.now() - datetime.timedelta(seconds=1)
        self.model_token_client.save()

        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![11]')

    def test_auth_client_verify_profile_unauthorized(self):
        self.model_app_client.active = False
        self.model_app_client.save()

        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey desativada![167]')

    def test_auth_client_verify_user_authorized(self):
        self.model_person_client.verified = True
        self.model_person_client.save()

        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário já verificado![12]')

    def test_auth_client_verify_ok(self):
        self.model_person_client.verified = False
        self.model_person_client.save()

        ip = '127.0.0.3';

        response = self.client.post('/api/v1/client/auth/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expire'])

        self.assertEqual(1,
            ModelToken.objects.filter(
                token=response.json()['token'],
                date_expire__gte=datetime.datetime.now(),
                ip=ip,
                app__app_id=self.model_app_client.app_id,
                person__person_id=self.model_person_client.person_id,
                person__verified=True).count())

    def test_auth_client_auth_apikey_not_found(self):
        ip = '0';

        response = self.client.post('/api/v1/auth/login/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey não encontrado![172]')

    def test_auth_client_auth_param_not_found(self):
        ip = '0';

        response = self.client.post('/api/v1/auth/login/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY='1',
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados insuficientes![19]')

    def test_auth_client_auth_apikey_invalid(self):
        ip = '0';

        data = {
            'username':'wborba',
            'password':'123456789'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY='1',
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Apikey inválida![20]')

    def test_auth_root_auth_apikey_inactive(self):
        self.model_app_root.active = False
        self.model_app_root.save()

        ip = '0';

        data = {
            'username':'wborba',
            'password':'123456789'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey dasativada![175]')

    def test_auth_director_auth_apikey_inactive(self):
        self.model_app_director.active = False
        self.model_app_director.save()

        ip = '0';

        data = {
            'username':'wborba',
            'password':'123456789'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey dasativada![175]')

    def test_auth_client_auth_apikey_inactive(self):
        self.model_app_client.active = False
        self.model_app_client.save()

        ip = '0';

        data = {
            'username':'wborba',
            'password':'123456789'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey dasativada![175]')

    def test_auth_client_auth_user_not_found(self):
        ip = '0';

        data = {
            'username':'wborba',
            'password':'123456789'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário não encontrado![173]')

    def test_auth_client_auth_user_not_verified(self):
        self.model_person_client.verified = False
        self.model_person_client.save()

        ip = '0';

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário não verificado![21]')

    def test_auth_root_auth_token_ip_duplicate(self):
        model_token_root = ModelToken(
            person=self.model_person_root,
            app=self.model_app_root,
            token='token-client-2',
            ip=self.model_token_root.ip,
            date_expire=self.model_token_root.date_expire)

        model_token_root.save()

        ip = self.model_token_root.ip;

        data = {
            'username':'wborba_root',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Erro crítico![174]')

    def test_auth_director_auth_token_ip_duplicate(self):
        model_token_director = ModelToken(
            person=self.model_person_director,
            app=self.model_app_director,
            token='token-client-2',
            ip=self.model_token_director.ip,
            date_expire=self.model_token_director.date_expire)

        model_token_director.save()

        ip = self.model_token_director.ip;

        data = {
            'username':'wborba_director',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Erro crítico![174]')

    def test_auth_client_auth_token_ip_duplicate(self):
        model_token_client = ModelToken(
            person=self.model_person_client,
            app=self.model_app_client,
            token='token-client-2',
            ip=self.model_token_client.ip,
            date_expire=self.model_token_client.date_expire)

        model_token_client.save()

        ip = self.model_token_client.ip;

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Erro crítico![174]')

    def test_auth_root_auth_ok_same_ip(self):
        ip = self.model_token_root.ip;

        data = {
            'username':'wborba_root',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['token'],self.model_token_root.token)
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_director_auth_ok_same_ip(self):
        ip = self.model_token_director.ip;

        data = {
            'username':'wborba_director',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['token'],self.model_token_director.token)
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_client_auth_ok_same_ip(self):
        ip = self.model_token_client.ip;

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['token'],self.model_token_client.token)
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_root_auth_ok_other_ip(self):
        ip = '127.0.0.1';

        data = {
            'username':'wborba_root',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_director_auth_ok_other_ip(self):
        ip = '127.0.0.2';

        data = {
            'username':'wborba_director',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_client_auth_ok_other_ip(self):
        ip = '127.0.0.3';

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expire'])

    def test_auth_root_restricted_access_1(self):
        self.model_person_root.username = 'wborba_root'
        self.model_person_root.password = '12345678'
        self.model_person_root.profile_id = ModelApp.PROFILE_ROOT
        self.model_person_root.save()

        ip = '127.0.0.1';

        data = {
            'username':'wborba_root',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_auth_root_restricted_access_2(self):
        self.model_person_root.username = 'wborba_root'
        self.model_person_root.password = '12345678'
        self.model_person_root.profile_id = ModelApp.PROFILE_ROOT
        self.model_person_root.save()

        ip = '127.0.0.1';

        data = {
            'username':'wborba_root',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_auth_director_restricted_access_3(self):
        self.model_person_director.username = 'wborba_director'
        self.model_person_director.password = '12345678'
        self.model_person_director.profile_id = ModelApp.PROFILE_DIRECTOR
        self.model_person_director.save()

        ip = '127.0.0.2';

        data = {
            'username':'wborba_director',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_auth_director_restricted_access_4(self):
        self.model_person_director.username = 'wborba_director'
        self.model_person_director.password = '12345678'
        self.model_person_director.profile_id = ModelApp.PROFILE_DIRECTOR
        self.model_person_director.save()

        ip = '127.0.0.2';

        data = {
            'username':'wborba_director',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_auth_root_restricted_access_5(self):
        self.model_person_client.username = 'wborba_client'
        self.model_person_client.password = '12345678'
        self.model_person_client.profile_id = ModelPerson.PROFILE_CLIENT
        self.model_person_client.save()

        ip = '127.0.0.1';

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_auth_root_restricted_access_6(self):
        self.model_person_client.username = 'wborba_client'
        self.model_person_client.password = '12345678'
        self.model_person_client.profile_id = ModelPerson.PROFILE_CLIENT
        self.model_person_client.save()

        ip = '127.0.0.1';

        data = {
            'username':'wborba_client',
            'password':'12345678'
        }

        response = self.client.post('/api/v1/auth/login/',json.dumps(data),
            content_type='application/json',
            REMOTE_ADDR=ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Acesso restrito![179]')

    def test_authorize_apikey_not_found(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey não encontrado![164]')

    def test_authorize_token_not_found(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.0',
            HTTP_APIKEY='0',
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não encontrado![2]')

    def test_authorize_apikey_not_authorized(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.0',
            HTTP_APIKEY='0',
            HTTP_TOKEN='0')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Apikey não autorizado![165]')

    def test_authorize_root_token_not_authorized(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.1',
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN='0')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![3]')

    def test_authorize_director_token_not_authorized(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.2',
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN='0')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![3]')

    def test_authorize_client_token_not_authorized(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.3',
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN='0')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![3]')

    def test_authorize_root_user_not_authorized(self):
        self.model_person_root.verified = False
        self.model_person_root.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.1',
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=self.model_token_root.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário não verificado![5]')

    def test_authorize_director_user_not_authorized(self):
        self.model_person_director.verified = False
        self.model_person_director.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.2',
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário não verificado![5]')

    def test_authorize_client_user_not_authorized(self):
        self.model_person_client.verified = False
        self.model_person_client.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.3',
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário não verificado![5]')

    def test_authorize_root_profile_id_not_allowed(self):
        self.model_app_root.profile_id = 99
        self.model_app_root.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.1',
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=self.model_token_root.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não permitido![6]')

    def test_authorize_director_profile_id_not_allowed(self):
        self.model_app_director.profile_id = 99
        self.model_app_director.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.2',
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não permitido![6]')

    def test_authorize_client_profile_id_not_allowed(self):
        self.model_app_client.profile_id = 99
        self.model_app_client.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.3',
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não permitido![6]')

    def test_authorize_root_ip_origin_error(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.11',
            HTTP_APIKEY=self.model_app_root.apikey,
            HTTP_TOKEN=self.model_token_root.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Ip de acesso difere de seu ip de origem![4]')

    def test_authorize_director_ip_origin_error(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.22',
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Ip de acesso difere de seu ip de origem![4]')

    def test_authorize_client_ip_origin_error(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR='127.0.0.33',
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Ip de acesso difere de seu ip de origem![4]')

    def test_authorize_client_profile_id_not_authorized(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![7]')

    def test_authorize_director_token_expired(self):
        self.model_token_director.date_expire = datetime.datetime.now() - datetime.timedelta(seconds=1)
        self.model_token_director.save()

        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR=self.model_token_director.ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token expirado![9]')

    def test_authorize_director_ok(self):
        data_get = {}

        response = self.client.get('/api/v1/director/person/',data_get,
            REMOTE_ADDR=self.model_token_director.ip,
            HTTP_APIKEY=self.model_app_director.apikey,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,200)
