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
            date_expire=datetime.datetime.now() + datetime.timedelta(minutes=ApiConfig.login_time_duration_in_minutes))

        self.model_token_client.save()

    def test_auth_verify_ip_not_found(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=None,
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'IP não encontrado![1]')

    def test_auth_verify_token_not_found(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não encontrado![166]')

    def test_auth_verify_token_unauthorized(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN='1')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![11]')

    def test_auth_root_verify_profile_unauthorized(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_root.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_auth_director_verify_profile_unauthorized(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_director.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_auth_client_verify_token_unauthorized_date_expire(self):
        self.model_token_client.date_expire = datetime.datetime.now() - datetime.timedelta(seconds=1)
        self.model_token_client.save()

        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Token não autorizado![11]')

    def test_auth_client_verify_profile_unauthorized(self):
        self.model_app_client.active = False
        self.model_app_client.save()

        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ApiKey desativada![167]')

    def test_auth_client_verify_user_authorized(self):
        self.model_person_client.verified = True
        self.model_person_client.save()

        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='0',
            HTTP_APIKEY=None,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Usuário já verificado![12]')

    def test_auth_client_verify_ok(self):
        self.model_person_client.verified = False
        self.model_person_client.save()

        ip = '0';

        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
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
