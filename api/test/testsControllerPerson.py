import uuid,datetime
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Merchant import Merchant as ModelMerchant

class TestControllerPerson(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        self.model_person_root = ModelPerson(
            parent_id=None,
            name='William Borba',
            cpf='00000000000',
            email='emailroot@test.com',
            phone1='99123456789',
            phone2=None,)

        self.model_person_root.save()

        token = str(uuid.uuid4())

        self.model_login_root = ModelLogin(
            person=self.model_person_root,
            profile_id=ModelLogin.PROFILE_ROOT,
            username=self.model_person_root.email,
            password=123456,
            verified=True,
            token=token,
            ip='127.0.0.1',
            date_expired=datetime.datetime(3000,1,1))

        self.model_login_root.save()

        self.model_person_merchant = ModelPerson(
            parent=self.model_person_root,
            name='Merchant test',
            cpf='00000000002',
            email='emailmerchant@test.com',
            phone1='99123456785',
            phone2=None,)

        self.model_person_merchant.save()

        token = str(uuid.uuid4())
        merchant_date_expired = datetime.datetime.now() + datetime.timedelta(days=30)

        self.model_login_merchant = ModelLogin(
            person=self.model_person_merchant,
            profile_id=ModelLogin.PROFILE_MERCHANT,
            username=self.model_person_merchant.email,
            password=123456,
            verified=True,
            token=token,
            ip='127.0.0.8',
            date_expired=merchant_date_expired)

        self.model_login_merchant.save()

        self.model_merchant = ModelMerchant(
            login=self.model_login_merchant,
            date_expired=merchant_date_expired)

        self.model_merchant.save()

        self.model_person_client = ModelPerson(
            parent=self.model_person_merchant,
            name='Client de teste',
            cpf='00000000001',
            email='emailclient@test.com',
            phone1='99123456782',
            phone2=None,)

        self.model_person_client.save()

        token = str(uuid.uuid4())

        self.model_login_client = ModelLogin(
            person=self.model_person_client,
            profile_id=ModelLogin.PROFILE_CLIENT,
            username=self.model_person_client.email,
            password=123456,
            verified=True,
            token=token,
            ip='127.0.0.9',
            date_expired=datetime.datetime.now() + datetime.timedelta(minutes=10))

        self.model_login_client.save()

    def test_filter_http_not_allowed(self):
        response = self.client.post('/api/v1/person/filter/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_filter_without_param(self):
        response = self.client.get('/api/v1/person/filter/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 1,
            'limit': ApiConfig.query_row_limit,
            'count': 1,
            'num_pages': 1,
            'has_next': False,
            'has_previous': False,
            'data': [{
                'person_id': self.model_person_client.person_id,
                'name': self.model_person_client.name,
                'cpf': self.model_person_client.cpf,
                'email': self.model_person_client.email,
                'phone1': self.model_person_client.phone1,
                'phone2': self.model_person_client.phone2
            }]
        }, response.json())

    def test_filter_with_param_page(self):
        response = self.client.get('/api/v1/person/filter/?page=1',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 1,
            'limit': ApiConfig.query_row_limit,
            'count': 1,
            'num_pages': 1,
            'has_next': False,
            'has_previous': False,
            'data': [{
                'person_id': self.model_person_client.person_id,
                'name': self.model_person_client.name,
                'cpf': self.model_person_client.cpf,
                'email': self.model_person_client.email,
                'phone1': self.model_person_client.phone1,
                'phone2': self.model_person_client.phone2
            }]
        }, response.json())

    def test_filter_with_param_page_error(self):
        response = self.client.get('/api/v1/person/filter/?page=2',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Erro na consulta de pessoa![25]',}, response.json())

    def test_getbyid_http_not_allowed(self):
        response = self.client.post('/api/v1/person/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_getbyid_client_missing(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes![36]',}, response.json())

    def test_getbyid_client_api_key_not_found(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY='xxxxxxxxxxxxxxxxxxxx',
            HTTP_CLIENT_IP='xxxxxx')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Api key do cliente não encontrado![37]',}, response.json())

    def test_getbyid_client_ip_error(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='xxxxxx')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Ip de acesso do login de cliente difere de seu ip de origem![38]',}, response.json())

    def test_getbyid_client_not_verified(self):
        self.model_login_client.verified = False
        self.model_login_client.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Login de cliente não verificado![39]',}, response.json())

    def test_getbyid_client_not_related(self):
        self.model_login_client.person = self.model_person_root
        self.model_login_client.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Cliente não relacionado![40]',}, response.json())

    def test_getbyid_client_profile_error(self):
        self.model_login_client.profile_id = ModelLogin.PROFILE_MERCHANT
        self.model_login_client.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil de cliente não autorizado![41]',}, response.json())

    def test_getbyid_client_expired(self):
        self.model_login_client.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        self.model_login_client.save()


        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Api key do cliente expirado![42]',}, response.json())

    def test_getbyid(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'person_id': self.model_person_client.person_id,
            'parent_id': self.model_person_client.parent_id,
            'name': self.model_person_client.name,
            'cpf': self.model_person_client.cpf,
            'email': self.model_person_client.email,
            'phone1': self.model_person_client.phone1,
            'phone2': self.model_person_client.phone2,
            'address': [],
        }, response.json())

        self.assertEqual(1,ModelLogin.objects.filter(
            person_id=self.model_person_client.person_id).exclude(
                date_expired=self.model_login_client.date_expired).count())

    def test_add_http_not_allowed(self):
        response = self.client.get('/api/v1/person/add/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_add_profile_incorrect(self):
        data_post = {}

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.9',
            HTTP_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não permitido![6]',}, response.json())

    def test_add_profile_unauthorized(self):
        data_post = {}

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não autorizado![7]',}, response.json())

    def test_add_data_missing(self):
        data_post = {}

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de pessoa![30]',}, response.json())

    def test_add_cpf_exist(self):
        data_post = {
            'name': 'sofia',
            'cpf': '00000000001',
            'email': 'sofia@test.com',
            'phone1': '1234567890',
        }

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Já existe uma pessoa cadastrada com este mesmo CPF![32]',}, response.json())

    def test_add_email_exist(self):
        data_post = {
            'name': 'sofia',
            'cpf': '00000000011',
            'email': 'emailclient@test.com',
            'phone1': '1234567890',
        }

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Já existe uma pessoa cadastrada com este mesmo E-mail![33]',}, response.json())

    def test_add(self):
        data_post = {
            'name': 'sofia',
            'cpf': '00000000011',
            'email': 'emailclient2@test.com',
            'phone1': '1234567890',
            'phone2': '5556668899',
        }

        response = self.client.post('/api/v1/person/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'person_id': response.json()['person_id'],
            'parent_id': self.model_login_merchant.person_id,
            'name': data_post['name'],
            'cpf': data_post['cpf'],
            'email': data_post['email'],
            'phone1': data_post['phone1'],
            'phone2': data_post['phone2'],
            'login': {
                'username': data_post['email'],
                'verified': False,
            }
        }, response.json())

        self.assertIsNotNone(ModelLogin.objects.get(
            username=data_post['email']))

        login = ModelLogin.objects.get(
            username=data_post['email'])

        self.assertEqual(login.person_id,response.json()['person_id'])
        self.assertEqual(login.profile_id,ModelLogin.PROFILE_CLIENT)
        self.assertEqual(login.password,None)
        self.assertEqual(login.verified,False)
        self.assertEqual(login.ip,None)
        self.assertEqual(login.date_expired,None)
