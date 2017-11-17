import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed,HttpResponseNotFound
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Address import Address as ModelAddress

class TestControllerPerson(TransactionTestCase):
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
            verified=True,
            token=token,
            ip='127.0.0.9',
            date_expired=datetime.datetime.now() + datetime.timedelta(hours=24),)

        self.model_login_client.save()

    def test_person_api_key_not_found(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.99',
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Api key não encontrado![2]',}, response.json())

    def test_person_api_key_not_authorized(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.99',
            HTTP_API_KEY='xxxxxxxxxxx',)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Api key não autorizado![3]',}, response.json())

    def test_person_api_key_not_verified(self):
        self.model_login_client.verified = False
        self.model_login_client.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.99',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Login não verificado![5]',}, response.json())

    def test_person_ip_error(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.88',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Ip de acesso do login difere de seu ip de origem![4]',}, response.json())

    def test_person_profile_error(self):
        self.model_login_client.profile_id = 999
        self.model_login_client.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.99',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não permitido![6]',}, response.json())

    def test_person_profile_not_authorized(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.9',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não autorizado![7]',}, response.json())

    def test_person_api_key_expired(self):
        self.model_login_director.date_expired = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        self.model_login_director.save()

        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Api key expirado![9]',}, response.json())

    def test_person_get_error(self):
        data_get = {
            'person_id': 'xxxxxxxxxxx'
        }

        response = self.client.get('/api/v1/person/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message':'Nenhum registro de pessoa encontrado com este ID[76]'}, response.json())

    def test_person_get(self):
        data_get = {
            'person_id': self.model_login_client.person_id
        }

        response = self.client.get('/api/v1/person/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'person_id': self.model_person_client.person_id,
            'parent_id': self.model_person_client.parent_id,
            'name': self.model_person_client.name,
            'cpf': self.model_person_client.cpf,
            'cnpj': self.model_person_client.cnpj,
            'email': self.model_person_client.email,
            'phone1': self.model_person_client.phone1,
            'phone2': self.model_person_client.phone2,
            'address': [],
        }, response.json())

    def test_person_filter_without_param(self):
        response = self.client.get('/api/v1/person/',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 2,
            'limit': ApiConfig.query_row_limit,
            'count': 2,
            'num_pages': 1,
            'has_next': False,
            'has_previous': False,
            'data': [{
                'person_id': self.model_person_client.person_id,
                'name': self.model_person_client.name,
                'cpf': self.model_person_client.cpf,
                'cnpj': self.model_person_client.cnpj,
                'email': self.model_person_client.email,
                'phone1': self.model_person_client.phone1,
                'phone2': self.model_person_client.phone2
            },{
                'person_id': self.model_person_director.person_id,
                'name': self.model_person_director.name,
                'cpf': self.model_person_director.cpf,
                'cnpj': self.model_person_director.cnpj,
                'email': self.model_person_director.email,
                'phone1': self.model_person_director.phone1,
                'phone2': self.model_person_director.phone2
            }]
        }, response.json())

    def test_person_filter_with_param_page(self):
        response = self.client.get('/api/v1/person/?page=2&limit=1',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 2,
            'limit': 1,
            'count': 2,
            'num_pages': 2,
            'has_next': False,
            'has_previous': True,
            'data': [{
                'person_id': self.model_person_director.person_id,
                'name': self.model_person_director.name,
                'cnpj': self.model_person_director.cnpj,
                'cpf': self.model_person_director.cpf,
                'email': self.model_person_director.email,
                'phone1': self.model_person_director.phone1,
                'phone2': self.model_person_director.phone2
            }]
        }, response.json())

    def test_person_filter_with_param_page_error(self):
        response = self.client.get('/api/v1/person/?page=3',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Erro na consulta de pessoa![25]',}, response.json())

    def test_person_add_profile_not_authorized(self):
        data_post = {}

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.9',
            HTTP_API_KEY=self.model_login_client.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não autorizado![7]',}, response.json())

    def test_person_add_param_missing(self):
        data_post = {
            'profile_id': '',
            'name': '',
            'cpf': '',
            'cnpj': '',
            'email': '',
            'phone1': '',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de pessoa![30]',}, response.json())

    def test_person_add_param_cpf_or_cnpf(self):
        data_post = {
            'profile_id': '3',
            'name': 'test',
            'cpf': '',
            'cnpj': '',
            'email': 'teste@teste.com',
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Um dos campos deve estar preenchido, CPF ou CNPJ![74]',}, response.json())

    def test_person_add_merchant_profile_not_can_create_up(self):
        data_post = {
            'profile_id': '1',
            'name': 'test',
            'cpf': '00000000000',
            'cnpj': '00000000000000',
            'email': 'teste@teste.com',
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Perfil não pode criar este tipo de pessoa![72]',}, response.json())

    def test_person_add_cpf_exist(self):
        data_post = {
            'profile_id': '3',
            'name': 'test',
            'cpf': self.model_person_client.cpf,
            'cnpj': '00000000000000',
            'email': 'teste@teste.com',
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Já existe uma pessoa cadastrada com este mesmo CPF![32]',}, response.json())

    def test_person_add_cnpj_exist(self):
        data_post = {
            'profile_id': '3',
            'name': 'test',
            'cpf': '0000000000000',
            'cnpj': self.model_person_client.cnpj,
            'email': 'teste@teste.com',
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Já existe uma pessoa cadastrada com este mesmo CNPJ![77]',}, response.json())

    def test_person_add_email_exist(self):
        data_post = {
            'profile_id': '3',
            'name': 'test',
            'cpf': '0000000000000',
            'cnpj': '000000000000000',
            'email': self.model_person_client.email,
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Já existe uma pessoa cadastrada com este mesmo E-mail![33]',}, response.json())

    def test_person_add(self):
        data_post = {
            'profile_id': '3',
            'name': 'test',
            'cpf': '0000000000000',
            'cnpj': '000000000000000',
            'email': 'email@teste.com',
            'phone1': '99999999',
            'phone2': '',
        }

        response = self.client.post('/api/v1/person/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'person_id': response.json()['person_id'],
            'parent_id': self.model_login_director.person_id,
            'name': data_post['name'],
            'cpf': data_post['cpf'],
            'cnpj': data_post['cnpj'],
            'email': data_post['email'],
            'phone1': data_post['phone1'],
            'phone2': None,
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
