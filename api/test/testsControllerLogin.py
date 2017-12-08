import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin

class TestControllerLogin(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        self.model_person_root = ModelPerson(
            parent_id=None,
            name='William Borba',
            cpf='00000000000',
            cnpj='00000000000',
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
            date_expired=datetime.datetime(3000,1,1),)

        self.model_login_root.save()

        self.model_person_director = ModelPerson(
            parent=self.model_person_root,
            name='Director test',
            cpf='00000000002',
            cnpj='00000000000',
            email='emaildirector@test.com',
            phone1='99123456785',
            phone2=None,)

        self.model_person_director.save()

        token = str(uuid.uuid4())
        director_date_expired = datetime.datetime.now() + datetime.timedelta(days=30)

        self.model_login_director = ModelLogin(
            person=self.model_person_director,
            profile_id=ModelLogin.PROFILE_DIRECTOR,
            username=self.model_person_director.email,
            password=123456,
            verified=True,
            token=token,
            ip='127.0.0.8',
            date_expired=director_date_expired,)

        self.model_login_director.save()

        self.model_person_client = ModelPerson(
            parent=self.model_person_director,
            name='Client de teste',
            cpf='00000000001',
            cnpj='00000000000',
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
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=None,
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'IP não encontrado![1]')

    def test_login_verify_apikey_not_found(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Api key não encontrado![11]')

    def test_login_verify_root_apikey_login_not_authorized(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_root.token,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_login_verify_director_apikey_login_not_authorized(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Perfil não autorizado![14]')

    def test_login_verify_client_apikey_ip_error(self):
        self.model_login_client.verified = True
        self.model_login_client.save()

        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login já está verificado![12]')

    def test_login_verify_client_ok(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.9',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expired'])

        self.assertEqual(1,ModelLogin.objects.filter(
            token=response.json()['token'],
            verified=True,
            ip='127.0.0.9').count())

    def test_login_auth_http_not_allowed(self):
        response = self.client.get('/api/v1/login/auth/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_login_auth_param_missing(self):
        data_post = {
            'username':'',
            'password':'',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Dados insuficientes![19]')

    def test_login_auth_param_error(self):
        data_post = {
            'username':'error',
            'password':'error',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login ou senha inválidos![20]')

    def test_login_auth_profile_incorrect(self):
        self.model_login_root.profile_id = 4
        self.model_login_root.save()

        data_post = {
            'username':'emailroot@test.com',
            'password':'123456',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Tipo de login não autorizado![22]')

    def test_login_auth_login_not_verified(self):
        self.model_login_root.verified = False
        self.model_login_root.save()

        data_post = {
            'username':'emailroot@test.com',
            'password':'123456',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'Login não verificado![21]')

    def test_login_auth_root_ok(self):
        data_post = {
            'username':'emailroot@test.com',
            'password':'123456',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expired'])

        self.assertEqual(1,ModelLogin.objects.filter(
            token=response.json()['token'],
            verified=True,
            ip='127.0.0.1').count())

    def test_login_auth_director_ok(self):
        data_post = {
            'username':'emaildirector@test.com',
            'password':'123456',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expired'])

        self.assertEqual(1,ModelLogin.objects.filter(
            token=response.json()['token'],
            verified=True,
            ip='127.0.0.8').count())

    def test_login_auth_client_ok(self):
        self.model_login_client.verified = True
        self.model_login_client.save()

        data_post = {
            'username':'emailclient@test.com',
            'password':'123456',
        }

        response = self.client.post('/api/v1/login/auth/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.9',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['date_expired'])

        self.assertEqual(1,ModelLogin.objects.filter(
            token=response.json()['token'],
            verified=True,
            ip='127.0.0.9').count())
