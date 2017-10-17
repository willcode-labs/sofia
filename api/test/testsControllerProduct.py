import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed,HttpResponseNotFound
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Merchant import Merchant as ModelMerchant
from api.Model.Address import Address as ModelAddress
from api.Model.Product import Product as ModelProduct

class TestControllerProduct(TransactionTestCase):
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

    def test_product_add_http_not_allowed(self):
        response = self.client.get('/api/v1/product/add/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    def test_product_add_param_missing(self):
        data_post = {
            'name': '',
            'description': '',
            'code': '',
            'compound': '',
            'unit_weight': '',
            'weight': '',
            'width': '',
            'length': '',
            'height': '',
            'origin': '',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de produto![58]'}, response.json())

    def test_product_add_param_unit_weight_error(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '',
            'unit_weight': 'test',
            'weight': '',
            'width': '',
            'length': '',
            'height': '',
            'origin': 'test',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Unidade de medida recusada![59]'}, response.json())

    def test_product_add_param_origin_error(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '',
            'unit_weight': '1',
            'weight': '',
            'width': '',
            'length': '',
            'height': '',
            'origin': 'test',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Origen recusada![60]'}, response.json())

    def test_product_add_error_compound(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': 'test',
            'unit_weight': '1',
            'weight': '',
            'width': '',
            'length': '',
            'height': '',
            'origin': '1',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro composto incorreto![63]'}, response.json())

    def test_product_add_error_weight(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '1',
            'unit_weight': '1',
            'weight': 'test',
            'width': '',
            'length': '',
            'height': '',
            'origin': '1',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro peso incorreto![64]'}, response.json())

    def test_product_add_error_width(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '1',
            'unit_weight': '1',
            'weight': '9999,99',
            'width': 'test',
            'length': '',
            'height': '',
            'origin': '1',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro largura incorreto![65]'}, response.json())

    def test_product_add_error_length(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '1',
            'unit_weight': '1',
            'weight': '9999,99',
            'width': '9999,99',
            'length': 'test',
            'height': '',
            'origin': '1',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro comprimento incorreto![66]'}, response.json())

    def test_product_add_error_height(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '1',
            'unit_weight': '1',
            'weight': '9999,99',
            'width': '9999,99',
            'length': '9999,99',
            'height': 'test',
            'origin': '1',
            'gtin': '',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro altura incorreto![67]'}, response.json())

    def test_product_add(self):
        data_post = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '0',
            'unit_weight': '1',
            'weight': '9999,99',
            'width': '9999,99',
            'length': '9999,99',
            'height': '9999,99',
            'origin': '1',
            'gtin': 'a1b2c3d4e5f6',
        }

        response = self.client.post('/api/v1/product/add/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'product_id': response.json()['product_id'],
            'name': data_post['name'],
            'description': data_post['description'],
            'code': data_post['code'],
            'compound': False,
            'unit_weight': 1,
            'weight': 9999.99,
            'width': 9999.99,
            'length': 9999.99,
            'height': 9999.99,
            'origin': 1,
            'gtin': 'a1b2c3d4e5f6',
            'published': False,
            'date_create': response.json()['date_create'],
        }, response.json())

        self.assertEqual(1,ModelProduct.objects.filter(product_id=response.json()['product_id']).count())

    def test_product_add_duplicate(self):
        data_post_a = {
            'name': 'product name test',
            'description': 'product description test',
            'code': '1234567890',
            'compound': '0',
            'unit_weight': '1',
            'weight': '9999,99',
            'width': '9999,99',
            'length': '9999,99',
            'height': '9999,99',
            'origin': '1',
            'gtin': 'a1b2c3d4e5f6',
        }

        response_a = self.client.post('/api/v1/product/add/',data_post_a,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        response_b = self.client.post('/api/v1/product/add/',data_post_a,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_merchant.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response_b.status_code,400)
        self.assertIsNotNone(response_b.json())
        self.assertIsInstance(response_b.json(), dict)
        self.assertEqual({'message': 'Existe produto cadastrado com este mesmo codigo![62]'}, response_b.json())

        self.assertEqual(1,ModelProduct.objects.filter().count())