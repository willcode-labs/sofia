import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed,HttpResponseNotFound
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Address import Address as ModelAddress
from api.Model.Product import Product as ModelProduct

class TestControllerProduct(TransactionTestCase):
    reset_sequences = True
    maxDiff = None

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

    def test_product_get_product_id_error(self):
        data_get = {
            'product_id': '123456789098765432',
            'page': '',
            'limit': '',
            'name': '',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Nenhum registro encontrado para este product_id[87]'}, response.json())

    def test_product_get_product_id_ok(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_get = {
            'product_id': model_product.product_id,
            'page': '',
            'limit': '',
            'name': '',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'product_id': model_product.product_id,
            'code': model_product.code,
            'compound': model_product.compound,
            'description': model_product.description,
            'gtin': model_product.gtin,
            'height': model_product.height,
            'length': model_product.length,
            'name': model_product.name,
            'origin': model_product.origin,
            'published': model_product.published,
            'unit_weight': model_product.unit_weight,
            'weight': model_product.weight,
            'width': model_product.width,
            'quantity': model_product.quantity,
        }, response.json())

    def test_product_filter_test_1(self):
        model_product_1 = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890123',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_1.save()

        model_product_2 = ModelProduct(
            name='produto teste 2',
            description='descrição de teste 2',
            code='1234567890321',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[1][0],
            weight=12.23,
            width=132.1,
            length=43.45,
            height=52.43,
            origin=ModelProduct.ORIGIN_LIST[1][0],
            gtin='333344455556667778899',
            quantity=1,
            published=True)

        model_product_2.save()

        data_get = {
            'product_id': '',
            'page': '1',
            'limit': '2',
            'name': '',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total':2,
            'limit':2,
            'count':2,
            'num_pages':1,
            'has_next':False,
            'has_previous':False,
            'data': [{
                'product_id': model_product_2.product_id,
                'code': model_product_2.code,
                'compound': model_product_2.compound,
                'description': model_product_2.description,
                'gtin': model_product_2.gtin,
                'height': model_product_2.height,
                'length': model_product_2.length,
                'name': model_product_2.name,
                'origin': model_product_2.origin,
                'published': model_product_2.published,
                'unit_weight': model_product_2.unit_weight,
                'weight': model_product_2.weight,
                'width': model_product_2.width,
                'quantity': model_product_2.quantity,
            },{
                'product_id': model_product_1.product_id,
                'code': model_product_1.code,
                'compound': model_product_1.compound,
                'description': model_product_1.description,
                'gtin': model_product_1.gtin,
                'height': model_product_1.height,
                'length': model_product_1.length,
                'name': model_product_1.name,
                'origin': model_product_1.origin,
                'published': model_product_1.published,
                'unit_weight': model_product_1.unit_weight,
                'weight': model_product_1.weight,
                'width': model_product_1.width,
                'quantity': model_product_1.quantity,
            }]
        }, response.json())

    def test_product_filter_test_2(self):
        model_product_1 = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890123',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_1.save()

        model_product_2 = ModelProduct(
            name='produto teste 2',
            description='descrição de teste 2',
            code='1234567890321',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[1][0],
            weight=12.23,
            width=132.1,
            length=43.45,
            height=52.43,
            origin=ModelProduct.ORIGIN_LIST[1][0],
            gtin='333344455556667778899',
            quantity=1,
            published=True)

        model_product_2.save()

        model_product_3 = ModelProduct(
            name='produto teste 3',
            description='descrição de teste 3',
            code='123456543234567',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[2][0],
            weight=82.23,
            width=732.1,
            length=903.45,
            height=1232.43,
            origin=ModelProduct.ORIGIN_LIST[2][0],
            gtin='2345234567dfghgfd',
            quantity=1,
            published=False)

        model_product_3.save()

        data_get = {
            'product_id': '',
            'page': '2',
            'limit': '1',
            'name': '',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total':3,
            'limit':1,
            'count':3,
            'num_pages':3,
            'has_next':True,
            'has_previous':True,
            'data': [{
                'product_id': model_product_2.product_id,
                'code': model_product_2.code,
                'compound': model_product_2.compound,
                'description': model_product_2.description,
                'gtin': model_product_2.gtin,
                'height': model_product_2.height,
                'length': model_product_2.length,
                'name': model_product_2.name,
                'origin': model_product_2.origin,
                'published': model_product_2.published,
                'unit_weight': model_product_2.unit_weight,
                'weight': model_product_2.weight,
                'width': model_product_2.width,
                'quantity': model_product_2.quantity,
            }]
        }, response.json())

    def test_product_filter_test_3(self):
        model_product_1 = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890123',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_1.save()

        model_product_2 = ModelProduct(
            name='produto teste 2',
            description='descrição de teste 2',
            code='1234567890321',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[1][0],
            weight=12.23,
            width=132.1,
            length=43.45,
            height=52.43,
            origin=ModelProduct.ORIGIN_LIST[1][0],
            gtin='333344455556667778899',
            quantity=1,
            published=True)

        model_product_2.save()

        model_product_3 = ModelProduct(
            name='produto teste 3',
            description='descrição de teste 3',
            code='123456543234567',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[2][0],
            weight=82.23,
            width=732.1,
            length=903.45,
            height=1232.43,
            origin=ModelProduct.ORIGIN_LIST[2][0],
            gtin='2345234567dfghgfd',
            quantity=1,
            published=False)

        model_product_3.save()

        data_get = {
            'product_id': '',
            'page': '4',
            'limit': '1',
            'name': '',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Nenhum registro encontrado![80]'}, response.json())

    def test_product_filter_test_4(self):
        model_product_1 = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890123',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_1.save()

        model_product_2 = ModelProduct(
            name='produto teste 2',
            description='descrição de teste 2',
            code='1234567890321',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[1][0],
            weight=12.23,
            width=132.1,
            length=43.45,
            height=52.43,
            origin=ModelProduct.ORIGIN_LIST[1][0],
            gtin='333344455556667778899',
            quantity=1,
            published=True)

        model_product_2.save()

        model_product_3 = ModelProduct(
            name='produto teste 3',
            description='descrição de teste 3',
            code='123456543234567',
            compound=True,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[2][0],
            weight=82.23,
            width=732.1,
            length=903.45,
            height=1232.43,
            origin=ModelProduct.ORIGIN_LIST[2][0],
            gtin='2345234567dfghgfd',
            quantity=1,
            published=False)

        model_product_3.save()

        data_get = {
            'product_id': '',
            'page': '1',
            'limit': '10',
            'name': 'produto teste 3',
        }

        response = self.client.get('/api/v1/product/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total':1,
            'limit':10,
            'count':1,
            'num_pages':1,
            'has_next':False,
            'has_previous':False,
            'data': [{
                'product_id': model_product_3.product_id,
                'code': model_product_3.code,
                'compound': model_product_3.compound,
                'description': model_product_3.description,
                'gtin': model_product_3.gtin,
                'height': model_product_3.height,
                'length': model_product_3.length,
                'name': model_product_3.name,
                'origin': model_product_3.origin,
                'published': model_product_3.published,
                'unit_weight': model_product_3.unit_weight,
                'weight': model_product_3.weight,
                'width': model_product_3.width,
                'quantity': model_product_3.quantity,
            }]
        }, response.json())

    def test_product_add_param_missing(self):
        data_post = {
            'name':'',
            'description':'',
            'code':'',
            'compound':'',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity': '',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de produto![58]'}, response.json())

    def test_product_add_param_compound_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'error',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro composto incorreto![63]'}, response.json())

    def test_product_add_param_weight_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'error',
            'width':'',
            'length':'',
            'height':'',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro peso incorreto![64]'}, response.json())

    def test_product_add_param_width_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'1.25',
            'width':'error',
            'length':'',
            'height':'',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro largura incorreto![65]'}, response.json())

    def test_product_add_param_length_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'1.25',
            'width':'3.75',
            'length':'error',
            'height':'',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro comprimento incorreto![66]'}, response.json())

    def test_product_add_param_height_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'1.25',
            'width':'3.75',
            'length':'45.65',
            'height':'error',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro altura incorreto![67]'}, response.json())

    def test_product_add_param_unit_weight_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':'error',
            'weight':'1.25',
            'width':'3.75',
            'length':'45.65',
            'height':'23.72',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Unidade de medida recusada![59]'}, response.json())

    def test_product_add_param_origin_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'1.25',
            'width':'3.75',
            'length':'45.65',
            'height':'27.87',
            'origin':'error',
            'gtin':'',
            'quantity': '1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Origen recusada![60]'}, response.json())

    def test_product_add_param_quantity_error(self):
        data_post = {
            'name':'product test 1',
            'description':'product test description 1',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[0][0],
            'weight':'1.25',
            'width':'3.75',
            'length':'45.65',
            'height':'27.87',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity': 'error',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Parametro quantidade incorreto![110]'}, response.json())

    def test_product_add_product_code_duplicate(self):
        model_product_1 = ModelProduct(
            name='product test 1',
            description='product test description 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.25,
            width=3.75,
            length=45.65,
            height=23.12,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False,
        )

        model_product_1.save()

        data_post_2 = {
            'name':'product test 2',
            'description':'product test description 2',
            'code':'1234567890',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'8.25',
            'width':'13.75',
            'length':'1.65',
            'height':'34.21',
            'origin':ModelProduct.ORIGIN_LIST[1][0],
            'gtin':'0987654321234567890987654321',
            'quantity':'1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post_2),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Existe um produto cadastrado com este mesmo codigo![62]'}, response.json())

    def test_product_add_ok(self):
        model_product_1 = ModelProduct(
            name='product test 1',
            description='product test description 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.25,
            width=3.75,
            length=45.65,
            height=23.12,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False,
        )

        model_product_1.save()

        data_post = {
            'name':'product test 2',
            'description':'product test description 2',
            'code':'0987654321',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'8.25',
            'width':'13.75',
            'length':'1.65',
            'height':'34.21',
            'origin':ModelProduct.ORIGIN_LIST[1][0],
            'gtin':'0987654321234567890987654321',
            'quantity':'1',
        }

        response = self.client.post('/api/v1/product/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'product_id': response.json()['product_id'],
            'name':'product test 2',
            'description':'product test description 2',
            'code':'0987654321',
            'compound':False,
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':8.25,
            'width':13.75,
            'length':1.65,
            'height':34.21,
            'origin':ModelProduct.ORIGIN_LIST[1][0],
            'gtin':'0987654321234567890987654321',
            'quantity':1,
            'published':False,
        }, response.json())

        self.assertEqual(ModelProduct.objects.filter().count(),2)

    def test_product_update_product_id_missing(self):
        data_put = {
            'product_id': '',
            'name':'',
            'description':'',
            'code':'',
            'compound':'',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':''
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para edição de produto![89]'}, response.json())

    def test_product_update_product_not_found(self):
        data_put = {
            'product_id': '1234567890',
            'name':'',
            'description':'',
            'code':'',
            'compound':'',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Produto não encontrado![99]'}, response.json())

    def test_product_update_product_published_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=True)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'',
            'description':'',
            'code':'',
            'compound':'',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Não é possível editar um produto publicado![101]'}, response.json())

    def test_product_update_data_insufficient(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'',
            'description':'',
            'code':'',
            'compound':'',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para edição de produto![90]'}, response.json())

    def test_product_update_data_compound_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'error',
            'unit_weight':'',
            'weight':'',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro composto incorreto![91]'}, response.json())

    def test_product_update_data_weight_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':'',
            'weight':'error',
            'width':'',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro peso incorreto![92]'}, response.json())

    def test_product_update_data_width_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':'',
            'weight':'123.54',
            'width':'error',
            'length':'',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro largura incorreto![93]'}, response.json())

    def test_product_update_data_length_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':'',
            'weight':'123.54',
            'width':'32.54',
            'length':'error',
            'height':'',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro comprimento incorreto![94]'}, response.json())

    def test_product_update_data_height_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':'',
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'error',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor do parâmetro comprimento incorreto![95]'}, response.json())

    def test_product_update_data_unit_weight_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':'error',
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'76.34',
            'origin':'',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Unidade de medida recusada![96]'}, response.json())

    def test_product_update_data_origin_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'76.34',
            'origin':'error',
            'gtin':'',
            'quantity':'',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Origen recusada![97]'}, response.json())

    def test_product_update_data_quantity_error(self):
        model_product = ModelProduct(
            name='produto teste',
            description='descrição de teste',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'76.34',
            'origin':ModelProduct.ORIGIN_LIST[0][0],
            'gtin':'',
            'quantity':'error',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Parametro quantidade incorreto![111]'}, response.json())

    def test_product_update_product_code_duplicate(self):
        model_product_1 = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_1.save()

        model_product_2 = ModelProduct(
            name='produto teste 2',
            description='descrição de teste 2',
            code='12345678901',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product_2.save()

        data_put = {
            'product_id': model_product_1.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'12345678901',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'76.34',
            'origin':ModelProduct.ORIGIN_LIST[1][0],
            'gtin':'',
            'quantity':'1',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Existe um outro produto cadastrado com este mesmo código![100]'}, response.json())

    def test_product_update_ok(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'name':'product teste updated 1',
            'description':'product teste description updated 1',
            'code':'12345678901',
            'compound':'0',
            'unit_weight':ModelProduct.UNIT_WEIGHT_LIST[1][0],
            'weight':'123.54',
            'width':'32.54',
            'length':'34.21',
            'height':'76.34',
            'origin':ModelProduct.ORIGIN_LIST[1][0],
            'gtin':'23456789oiuytrds',
            'quantity':'1',
        }

        response = self.client.put('/api/v1/product/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'product_id': data_put['product_id'],
            'name': data_put['name'],
            'description': data_put['description'],
            'code': data_put['code'],
            'compound': False,
            'unit_weight': data_put['unit_weight'],
            'weight': float(data_put['weight']),
            'width': float(data_put['width']),
            'length': float(data_put['length']),
            'height': float(data_put['height']),
            'origin': data_put['origin'],
            'gtin': data_put['gtin'],
            'quantity': int(data_put['quantity']),
            'published': False,
        }, response.json())

    def test_product_delete_data_product_id_not_found(self):
        data_delete = {
            'product_id': '',
        }

        response = self.client.delete('/api/v1/product/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message':'ID de produto não encontrado![102]'}, response.json())

    def test_product_delete_product_not_found(self):
        data_delete = {
            'product_id': '1234567890',
        }

        response = self.client.delete('/api/v1/product/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message':'Produto não encontrado![103]'}, response.json())

    def test_product_delete_published_error(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=True)

        model_product.save()

        data_delete = {
            'product_id': model_product.product_id,
        }

        response = self.client.delete('/api/v1/product/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message':'Não é possível remover um produto publicado![104]'}, response.json())

    def test_product_delete_ok(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_delete = {
            'product_id': model_product.product_id,
        }

        response = self.client.delete('/api/v1/product/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'result': True}, response.json())

    def test_product_published_param_missing(self):
        data_put = {
            'product_id': '',
            'published': ''
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Parâmetros insuficientes para este operação![105]'}, response.json())

    def test_product_published_param_published_error(self):
        data_put = {
            'product_id': '123456789',
            'published': 'error'
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor de parâmetro incorreto![106]'}, response.json())

    def test_product_published_product_not_found(self):
        data_put = {
            'product_id': '123456789098765432',
            'published': '0'
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Produto não encontrado![107]'}, response.json())

    def test_product_published_update_error_1(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=True)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'published': '1'
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Produto ja está publicado![108]'}, response.json())

    def test_product_published_update_error_2(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'published': '0'
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Produto não se encontra com status publicado![109]'}, response.json())

    def test_product_published_ok(self):
        model_product = ModelProduct(
            name='produto teste 1',
            description='descrição de teste 1',
            code='1234567890',
            compound=False,
            unit_weight=ModelProduct.UNIT_WEIGHT_LIST[0][0],
            weight=1.23,
            width=112.1,
            length=23.45,
            height=12.43,
            origin=ModelProduct.ORIGIN_LIST[0][0],
            gtin='1234567890987654321234567890',
            quantity=1,
            published=False)

        model_product.save()

        data_put = {
            'product_id': model_product.product_id,
            'published': '1'
        }

        response = self.client.put('/api/v1/product/published/',json.dumps(data_put),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'result': True}, response.json())

        self.assertEqual(ModelProduct.objects.filter(product_id=model_product.product_id,published=1).count(),1)