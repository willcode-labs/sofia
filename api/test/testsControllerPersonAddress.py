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

    def test_person_address_add_param_missing(self):
        data_post = {
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.post('/api/v1/person/address/',data_post,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,
            HTTP_CLIENT_API_KEY=self.model_login_client.token,
            HTTP_CLIENT_IP='127.0.0.9')

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de endereço![43]',}, response.json())

    # def test_person_address_add_param_error(self):
    #     data_post = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '3456',
    #         'complement': '',
    #         'invoice': False,
    #         'delivery': True,
    #     }

    #     response = self.client.post('/api/v1/person/address/add/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Valor incorreto![45]',}, response.json())

    # def test_person_address_add_duplicate(self):
    #     data_post = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '3456',
    #         'complement': '',
    #         'invoice': '0',
    #         'delivery': '0',
    #     }

    #     response = self.client.post('/api/v1/person/address/add/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     response = self.client.post('/api/v1/person/address/add/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Endereço duplicado![46]',}, response.json())

    # def test_person_address_add(self):
    #     data_post = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '57',
    #         'complement': '',
    #         'invoice': '0',
    #         'delivery': '0',
    #     }

    #     response = self.client.post('/api/v1/person/address/add/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,200)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({
    #         'address_id': response.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post['state'],
    #         'city': data_post['city'],
    #         'number': data_post['number'],
    #         'complement': data_post['complement'],
    #         'invoice': True,
    #         'delivery': True,
    #         'date_create': response.json()['date_create'],
    #     }, response.json())

    # def test_person_address_many_register(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '57',
    #         'complement': '',
    #         'invoice': '0',
    #         'delivery': '1',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_a.status_code,200)
    #     self.assertIsNotNone(response_a.json())
    #     self.assertIsInstance(response_a.json(), dict)
    #     self.assertEqual({
    #         'address_id': response_a.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post_a['state'],
    #         'city': data_post_a['city'],
    #         'number': data_post_a['number'],
    #         'complement': data_post_a['complement'],
    #         'invoice': True,
    #         'delivery': True,
    #         'date_create': response_a.json()['date_create'],
    #     }, response_a.json())

    #     data_post_b = {
    #         'state': 'SC',
    #         'city': 'Florianópolis',
    #         'number': '56',
    #         'complement': '',
    #         'invoice': '0',
    #         'delivery': '1',
    #     }

    #     response_b = self.client.post('/api/v1/person/address/add/',data_post_b,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_b.status_code,200)
    #     self.assertIsNotNone(response_b.json())
    #     self.assertIsInstance(response_b.json(), dict)
    #     self.assertEqual({
    #         'address_id': response_b.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post_b['state'],
    #         'city': data_post_b['city'],
    #         'number': data_post_b['number'],
    #         'complement': data_post_b['complement'],
    #         'invoice': False,
    #         'delivery': True,
    #         'date_create': response_b.json()['date_create'],
    #     }, response_b.json())

    #     data_post_c = {
    #         'state': 'SP',
    #         'city': 'São Paulo',
    #         'number': '99',
    #         'complement': '',
    #         'invoice': '1',
    #         'delivery': '0',
    #     }

    #     response_c = self.client.post('/api/v1/person/address/add/',data_post_c,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_c.status_code,200)
    #     self.assertIsNotNone(response_c.json())
    #     self.assertIsInstance(response_c.json(), dict)
    #     self.assertEqual({
    #         'address_id': response_c.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post_c['state'],
    #         'city': data_post_c['city'],
    #         'number': data_post_c['number'],
    #         'complement': data_post_c['complement'],
    #         'invoice': True,
    #         'delivery': False,
    #         'date_create': response_c.json()['date_create'],
    #     }, response_c.json())


    #     self.assertIsNotNone(ModelAddress.objects.get(
    #         address_id=response_a.json()['address_id'],
    #         invoice=False,
    #         delivery=False))

    #     self.assertIsNotNone(ModelAddress.objects.get(
    #         address_id=response_b.json()['address_id'],
    #         invoice=False,
    #         delivery=True))

    #     self.assertIsNotNone(ModelAddress.objects.get(
    #         address_id=response_c.json()['address_id'],
    #         invoice=True,
    #         delivery=False))

    # def test_person_address_update_http_not_found(self):
    #     response = self.client.get('/api/v1/person/address/update/')

    #     self.assertEqual(response.status_code,404)
    #     self.assertTrue(isinstance(response,HttpResponseNotFound),'Não é um objeto do tipo "HttpResponseNotFound"')

    # def test_person_address_update_http_not_allowed(self):
    #     response = self.client.get('/api/v1/person/address/123/update/')

    #     self.assertEqual(response.status_code,405)
    #     self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    # def test_person_address_update_param_missing(self):
    #     data_post = {
    #         'state': '',
    #         'city': '',
    #         'number': '',
    #         'complement': '',
    #         'invoice': '',
    #         'delivery': '',
    #     }

    #     response = self.client.post('/api/v1/person/address/123/update/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Nenhum dado para alterar![47]',}, response.json())

    # def test_person_address_update_param_incorrect(self):
    #     data_post = {
    #         'state': '',
    #         'city': '',
    #         'number': '',
    #         'complement': '',
    #         'invoice': 'test',
    #         'delivery': '123',
    #     }

    #     response = self.client.post('/api/v1/person/address/123/update/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Valor incorreto![48]',}, response.json())

    # def test_person_address_update_not_found(self):
    #     data_post = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '0',
    #         'delivery': '0',
    #     }

    #     response = self.client.post('/api/v1/person/address/123/update/',data_post,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Endereço não encontrado![50]',}, response.json())

    # def test_person_address_update(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '0',
    #         'delivery': '0',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     data_post_b = {
    #         'state': 'SC',
    #         'city': 'Florianópolis',
    #         'number': '456',
    #         'complement': 'apartamento',
    #         'invoice': '1',
    #         'delivery': '0',
    #     }

    #     response_b = self.client.post('/api/v1/person/address/add/',data_post_b,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     data_post_c = {
    #         'state': 'AC',
    #         'city': 'Rio Branco',
    #         'number': '123',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '1',
    #     }

    #     response_c = self.client.post('/api/v1/person/address/%s/update/' % (response_b.json()['address_id'],),data_post_c,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_c.status_code,200)
    #     self.assertIsNotNone(response_c.json())
    #     self.assertIsInstance(response_c.json(), dict)
    #     self.assertEqual({
    #         'address_id': response_c.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post_c['state'],
    #         'city': data_post_c['city'],
    #         'number': data_post_c['number'],
    #         'complement': data_post_c['complement'],
    #         'invoice': True,
    #         'delivery': True,
    #         'date_create': response_c.json()['date_create'],
    #     }, response_c.json())

    #     self.assertIsNotNone(ModelAddress.objects.get(
    #         address_id=response_a.json()['address_id'],
    #         invoice=False,
    #         delivery=False))

    #     self.assertIsNotNone(ModelAddress.objects.get(
    #         address_id=response_c.json()['address_id'],
    #         invoice=True,
    #         delivery=True))

    # def test_person_address_delete_http_not_allowed(self):
    #     response = self.client.get('/api/v1/person/address/123/update/')

    #     self.assertEqual(response.status_code,405)
    #     self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    # def test_person_address_delete_not_found(self):
    #     response = self.client.post('/api/v1/person/address/123/delete/',{},
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Endereço não encontrado![51]',}, response.json())

    # def test_person_address_delete_error_invoice(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '0',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     response_b = self.client.post('/api/v1/person/address/%s/delete/' % (response_a.json()['address_id'],),{},
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_b.status_code,400)
    #     self.assertIsNotNone(response_b.json())
    #     self.assertIsInstance(response_b.json(), dict)
    #     self.assertEqual({'message': 'Não é possível remover endereço de cobrança ou entrega![52]',}, response_b.json())

    # def test_person_address_delete_error_delivery(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '1',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     data_post_b = {
    #         'state': 'SC',
    #         'city': 'Florianópolis',
    #         'number': '123',
    #         'complement': 'casa',
    #         'invoice': '0',
    #         'delivery': '1',
    #     }

    #     response_b = self.client.post('/api/v1/person/address/add/',data_post_b,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     response_c = self.client.post('/api/v1/person/address/%s/delete/' % (response_b.json()['address_id'],),{},
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_c.status_code,400)
    #     self.assertIsNotNone(response_c.json())
    #     self.assertIsInstance(response_c.json(), dict)
    #     self.assertEqual({'message': 'Não é possível remover endereço de entrega ou cobrança![53]',}, response_c.json())

    # def test_person_address_delete(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '0',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     data_post_b = {
    #         'state': 'SC',
    #         'city': 'Florianópolis',
    #         'number': '132',
    #         'complement': 'casa',
    #         'invoice': '0',
    #         'delivery': '0',
    #     }

    #     response_b = self.client.post('/api/v1/person/address/add/',data_post_b,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertIsNotNone(ModelAddress.objects.get(address_id=response_a.json()['address_id']))
    #     self.assertIsNotNone(ModelAddress.objects.get(address_id=response_b.json()['address_id']))

    #     response_c = self.client.post('/api/v1/person/address/%s/delete/' % (response_b.json()['address_id'],),{},
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_c.status_code,200)
    #     self.assertIsNotNone(response_c.json())
    #     self.assertIsInstance(response_c.json(), dict)
    #     self.assertEqual(1,ModelAddress.objects.filter(address_id=response_a.json()['address_id']).count())
    #     self.assertEqual(0,ModelAddress.objects.filter(address_id=response_b.json()['address_id']).count())
    #     self.assertEqual({'result': True,}, response_c.json())

    # def test_person_address_get_http_not_allowed(self):
    #     response = self.client.post('/api/v1/person/address/123/')

    #     self.assertEqual(response.status_code,405)
    #     self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    # def test_person_address_get_not_found(self):
    #     response = self.client.get('/api/v1/person/address/123/',{},
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Registro de endereço não encontrado[54]',}, response.json())

    # def test_person_address_get(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '0',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     response_b = self.client.get('/api/v1/person/address/%s/' % (response_a.json()['address_id'],),
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_b.status_code,200)
    #     self.assertIsNotNone(response_b.json())
    #     self.assertIsInstance(response_b.json(), dict)
    #     self.assertEqual({
    #         'address_id': response_a.json()['address_id'],
    #         'person_id': self.model_login_client.person_id,
    #         'state': data_post_a['state'],
    #         'city': data_post_a['city'],
    #         'number': 99,
    #         'complement': data_post_a['complement'],
    #         'invoice': True,
    #         'delivery': True,
    #         'date_create': response_a.json()['date_create'],
    #     }, response_b.json())

    # def test_person_address_filter_http_not_allowed(self):
    #     response = self.client.post('/api/v1/person/address/filter/')

    #     self.assertEqual(response.status_code,405)
    #     self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')

    # def test_person_address_filter_param_error(self):
    #     data_get = 'page=error&limit=error&invoice=test&delivery=test'

    #     response = self.client.get('/api/v1/person/address/filter/?%s' % (data_get,),
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(response.json())
    #     self.assertIsInstance(response.json(), dict)
    #     self.assertEqual({'message': 'Valor incorreto![55]',}, response.json())

    # def test_person_address_filter(self):
    #     data_post_a = {
    #         'state': 'RS',
    #         'city': 'Porto Alegre',
    #         'number': '99',
    #         'complement': 'casa',
    #         'invoice': '1',
    #         'delivery': '1',
    #     }

    #     response_a = self.client.post('/api/v1/person/address/add/',data_post_a,
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     data_get = 'page=1&limit=10&state=RS&city=Porto Alegre&number=99&complement=casa&invoice=1&delivery=1'

    #     response_b = self.client.get('/api/v1/person/address/filter/?%s' % (data_get,),
    #         REMOTE_ADDR='127.0.0.8',
    #         HTTP_API_KEY=self.model_login_director.token,
    #         HTTP_CLIENT_API_KEY=self.model_login_client.token,
    #         HTTP_CLIENT_IP='127.0.0.9')

    #     self.assertEqual(response_b.status_code,200)
    #     self.assertIsNotNone(response_b.json())
    #     self.assertIsInstance(response_b.json(), dict)
    #     self.assertEqual({
    #         'total': 1,
    #         'limit': 10,
    #         'count': 1,
    #         'num_pages': 1,
    #         'has_next': False,
    #         'has_previous': False,
    #         'data': [{
    #             'address_id': response_a.json()['address_id'],
    #             'person_id': self.model_login_client.person_id,
    #             'state': data_post_a['state'],
    #             'city': data_post_a['city'],
    #             'number': 99,
    #             'complement': data_post_a['complement'],
    #             'invoice': True,
    #             'delivery': True,
    #             'date_create': response_a.json()['date_create'],
    #         }]
    #     }, response_b.json())
