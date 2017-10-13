import uuid,datetime
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Merchant import Merchant as ModelMerchant

class TestControllerLogin(TransactionTestCase):
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
            verified=False,
            token=token,
            ip='127.0.0.1',
            date_expired=datetime.datetime(3000,1,1),)

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
            verified=False,
            token=token,
            ip='127.0.0.8',
            date_expired=merchant_date_expired,)

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
            verified=False,
            token=token,
            ip='127.0.0.9',
            date_expired=datetime.datetime.now() + datetime.timedelta(hours=24),)

        self.model_login_client.save()

    def test_login_verify_http_not_allowed(self):
        response = self.client.get('/api/v1/login/verify/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_login_verify_ip_not_found(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR=None,
            HTTP_API_KEY=None,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'IP não encontrado![1]')

    def test_login_verify_apikey_not_found(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key não encontrado![2]')

    def test_login_verify_apikey_login_not_authorized(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY='9999999',
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key não autorizado![3]')

    def test_login_verify_root_apikey_ip_error(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='999.9.9.9',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Ip de acesso do login difere de seu ip de origem![4]')

    def test_login_verify_merchant_apikey_ip_error(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='999.9.9.9',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Ip de acesso do login difere de seu ip de origem![4]')

    def test_login_verify_root_apikey_login_not_verified(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login não verificado![5]')

    def test_login_verify_merchant_apikey_login_not_verified(self):
        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login não verificado![5]')

    def test_login_verify_root_apikey_profile_not_allowed(self):
        self.model_login_root.profile_id = 3
        self.model_login_root.verified = True
        self.model_login_root.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não permitido![6]')

    def test_login_verify_merchant_apikey_profile_not_allowed(self):
        self.model_login_merchant.profile_id = 3
        self.model_login_merchant.verified = True
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não permitido![6]')

    def test_login_verify_root_apikey_expired(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime(2017,1,1)
        self.model_login_root.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key expirado![9]')

    def test_login_verify_merchant_apikey_expired(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime(2017,1,1)
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key expirado![9]')

    def test_login_verify_root_apikey_client_missing(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados de cliente insuficientes![10]')

    def test_login_verify_merchant_apikey_client_missing(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP=None)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados de cliente insuficientes![10]')

    def test_login_verify_root_apikey_client_apikey_missing(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY='999999',
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key do cliente não encontrado![11]')

    def test_login_verify_merchant_apikey_client_apikey_missing(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY='999999',
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key do cliente não encontrado![11]')

    def test_login_verify_root_apikey_client_apikey_verified(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        self.model_login_merchant.verified = True
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login de cliente já está verificado![12]')

    def test_login_verify_merchant_apikey_client_apikey_verified(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        self.model_login_client.verified = True
        self.model_login_client.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login de cliente já está verificado![12]')

    def test_login_verify_root_apikey_client_not_related(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        self.model_login_client.verified = False
        self.model_login_client.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Cliente não relacionado![13]')

    def test_login_verify_merchant_apikey_client_not_related(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        self.model_login_root.verified = False
        self.model_login_root.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Cliente não relacionado![13]')

    def test_login_verify_root_apikey_client_without_merchant(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        self.model_login_merchant.verified = False
        self.model_login_merchant.save()

        self.model_merchant.delete()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Não há um registro de controle para este comerciante![17]')

    def test_login_verify_root_apikey_client_merchant_expired(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        self.model_login_merchant.verified = False
        self.model_login_merchant.save()

        self.model_merchant.date_expired = datetime.datetime.now() - datetime.timedelta(minutes=1)
        self.model_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Comerciante expirado![18]')

    def test_login_verify_root_apikey_client_success(self):
        self.model_login_root.verified = True
        self.model_login_root.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_root.save()

        self.model_login_merchant.verified = False
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,
            HTTP_CLIENT_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_IP='127.0.0.8')

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['client_token'])
        self.assertIsNotNone(response.json()['client_date_expired'])

    def test_login_verify_merchant_apikey_client_success(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        self.model_login_client.verified = False
        self.model_login_client.save()

        response = self.client.post('/api/v1/login/verify/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['client_token'])
        self.assertIsNotNone(response.json()['client_date_expired'])

    def test_login_auth_merchant_data_insufficient(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        response = self.client.post('/api/v1/login/auth/',{},
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados insuficientes![19]')

    def test_login_auth_merchant_login_or_password_invalid(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        data_post = {
            "username": "emailclient@test.com_incorrect",
            "password": "123456"}

        response = self.client.post('/api/v1/login/auth/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login ou senha inválidos![20]')

    def test_login_auth_merchant_login_not_verified(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        data_post = {
            "username": "emailclient@test.com",
            "password": "123456"}

        response = self.client.post('/api/v1/login/auth/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login não verificado![21]')

    def test_login_auth_merchant_login_profile_not_authorized(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        self.model_login_client.verified = True
        self.model_login_client.save()

        data_post = {
            "username": "emailmerchant@test.com",
            "password": "123456"}

        response = self.client.post('/api/v1/login/auth/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Tipo de login não autorizado![22]')

    def test_login_auth_merchant_login_success(self):
        self.model_login_merchant.verified = True
        self.model_login_merchant.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.model_login_merchant.save()

        self.model_login_client.verified = True
        self.model_login_client.save()

        data_post = {
            "username": "emailclient@test.com",
            "password": "123456"}

        response = self.client.post('/api/v1/login/auth/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=None,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['client_token'])
        self.assertIsNotNone(response.json()['client_date_expired'])
