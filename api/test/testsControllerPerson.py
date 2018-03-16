import datetime,json
from django.test import Client,TestCase,TransactionTestCase
from api.apps import ApiConfig
from api.Model.App import App as ModelApp
from api.Model.Token import Token as ModelToken
from api.Model.Person import Person as ModelPerson
from api.Model.Address import Address as ModelAddress

class TestControllerPerson(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        # Person ROOT
        self.model_person_root = ModelPerson(
            profile_id=ModelApp.PROFILE_ROOT,
            name='William Borba ROOT',
            cpf='00000000001',
            cnpj='00000000000001',
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
            cnpj='00000000000002',
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
            cnpj='00000000000003',
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

    def test_person_client_get_person_id_not_found(self):
        data_get = {}

        response = self.client.get('/api/v1/client/person/',data_get,
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'ID de pessoa não encontrado[181]')

    def test_person_client_get_person_not_found(self):
        data_get = {
            'person_id': '1234567890'
        }

        response = self.client.get('/api/v1/client/person/',data_get,
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Registro de pessoa não encontrado[182]')

    def test_person_client_get_ok(self):
        data_get = {
            'person_id': self.model_person_client.person_id
        }

        response = self.client.get('/api/v1/client/person/',data_get,
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
            'person_id': self.model_person_client.person_id,
            'profile_id': self.model_person_client.profile_id,
            'name': self.model_person_client.name,
            'cpf': self.model_person_client.cpf,
            'cnpj': self.model_person_client.cnpj,
            'email': self.model_person_client.email,
            'phone1': self.model_person_client.phone1,
            'phone2': self.model_person_client.phone2,
            'username': self.model_person_client.username,
            'verified': self.model_person_client.verified,
            'address': [],
        })

    def test_person_client_post_param_missing(self):
        data_post = {
            'name':'',
            'cpf':'',
            'cnpj':'',
            'email':'',
            'phone1':'',
            'phone2':'',
            'password':''
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados insuficientes para criação de pessoa![189]')

    def test_person_client_post_email_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'00000000000033',
            'email':'incorrect-email_test.com',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Formato do email incorreto![210]')

    def test_person_client_post_cpf_and_cnpj_missing(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Um dos campos deve estar preenchido, CPF ou CNPJ![190]')

    def test_person_client_post_cpf_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'incorrect',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'CPF incorreto![191]')

    def test_person_client_post_cnpj_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'incorrect',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'CNPJ incorreto![192]')

    def test_person_client_post_phone1_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'00000000000',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'incorrect',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Telefone 1 incorreto![193]')

    def test_person_client_post_phone2_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'00000000000',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'incorrect',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Telefone 2 incorreto![194]')

    def test_person_client_post_username_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'00000000000',
            'cnpj':'',
            'email':'email',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Username deve estar entre 6 e 150 caracteres![195]')

    def test_person_client_post_password_incorrect(self):
        data_post = {
            'name':'User*1',
            'cpf':'00000000003',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'7777777'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Password deve ter 8 caracteres![196]')

    def test_person_client_post_cpf_duplicate(self):
        data_post = {
            'name':'User*1',
            'cpf':'00000000003',
            'cnpj':'',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'88888888'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Existe uma pessoa cadastrada com este mesmo CPF![197]')

    def test_person_client_post_cnpj_duplicate(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'00000000000003',
            'email':'email@test.com',
            'phone1':'',
            'phone2':'',
            'password':'88888888'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Existe uma pessoa cadastrada com este mesmo CNPJ![198]')

    def test_person_client_post_email_duplicate(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'00000000000033',
            'email':self.model_person_client.email,
            'phone1':'',
            'phone2':'',
            'password':'88888888'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Existe uma pessoa cadastrada com este mesmo E-mail![199]')

    def test_person_client_post_username_duplicate(self):
        client = ModelPerson(
            profile_id=ModelPerson.PROFILE_CLIENT,
            name='XXXX',
            cpf='00000000099',
            cnpj='00000000000099',
            email='other_emailclient@test123.com',
            phone1=None,
            phone2=None,
            username='emailclient@test123.com',
            password='12345678',
            verified=True)
        client.save()

        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'00000000000033',
            'email':client.username,
            'phone1':'',
            'phone2':'',
            'password':'88888888'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Existe uma pessoa cadastrada com este mesmo username![200]')

    def test_person_client_post_ok(self):
        data_post = {
            'name':'User*1',
            'cpf':'',
            'cnpj':'00000000000033',
            'email':'newemail@test.com',
            'phone1':'',
            'phone2':'',
            'password':'88888888'
        }

        response = self.client.post('/api/v1/client/person/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR=self.model_token_client.ip,
            HTTP_APIKEY=self.model_app_client.apikey,
            HTTP_TOKEN=self.model_token_client.token)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Existe uma pessoa cadastrada com este mesmo username![200]')
