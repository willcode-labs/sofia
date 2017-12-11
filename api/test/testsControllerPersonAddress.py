import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed,HttpResponseNotFound
from api.apps import ApiConfig
from api.Model.Person import Person as ModelPerson
from api.Model.Login import Login as ModelLogin
from api.Model.Address import Address as ModelAddress

class TestControllerPerson(TransactionTestCase):
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

    def test_person_address_get_error(self):
        data_get = {
            'address_id': '1234567890',
            'person_id': '',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Registro de endereço não encontrado![78]',}, response.json())

    def test_person_address_get_ok(self):
        model_address = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address.save()

        data_get = {
            'address_id': model_address.address_id,
            'person_id': '',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'person_id': model_address.person_id, 
            'complement': model_address.complement, 
            'number': model_address.number, 
            'delivery': model_address.delivery, 
            'invoice': model_address.invoice, 
            'address_id': model_address.address_id, 
            'state': model_address.state, 
            'city': model_address.city}, response.json())

    def test_person_address_filter_param_invoice_and_deliver_error(self):
        data_get = {
            'address_id': '',
            'person_id': '',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': 'a',
            'delivery': 'b',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor incorreto![55]',}, response.json())

    def test_person_address_filter_empty_result(self):
        data_get = {
            'address_id': '',
            'person_id': '1',
            'state': '1',
            'city': '1',
            'number': '1',
            'complement': '1',
            'invoice': '1',
            'delivery': '1',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 0, 
            'has_next': False, 
            'count': 0, 
            'has_previous': False, 
            'limit': 20, 
            'data': [], 
            'num_pages': 1}, response.json())

    def test_person_address_filter_with_result(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address_2.save()

        data_get = {
            'address_id': '',
            'person_id': self.model_person_client.person_id,
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 2, 
            'has_next': False, 
            'count': 2, 
            'has_previous': False, 
            'limit': 20, 
            'data': [
                {
                    'address_id': model_address_2.address_id, 
                    'person_id': model_address_2.person_id, 
                    'number': model_address_2.number, 
                    'state': model_address_2.state, 
                    'complement': model_address_2.complement, 
                    'city': model_address_2.city, 
                    'delivery': model_address_2.delivery, 
                    'invoice': model_address_2.invoice}, 
                {
                    'address_id': model_address_1.address_id, 
                    'person_id': model_address_1.person_id, 
                    'number': model_address_1.number, 
                    'state': model_address_1.state, 
                    'complement': model_address_1.complement, 
                    'city': model_address_1.city, 
                    'delivery': model_address_1.delivery, 
                    'invoice': model_address_1.invoice}], 
            'num_pages': 1}, response.json())

    def test_person_address_filter_with_pagination_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address_2.save()

        data_get = {
            'page': '3',
            'limit': '1',
            'address_id': '',
            'person_id': self.model_person_client.person_id,
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Nenhum registro encontrado![80]'}, response.json())

    def test_person_address_filter_with_pagination_ok(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address_2.save()

        data_get = {
            'page': '1',
            'limit': '1',
            'address_id': '',
            'person_id': self.model_person_client.person_id,
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.get('/api/v1/person/address/',data_get,
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'total': 2, 
            'has_next': True, 
            'count': 2, 
            'has_previous': False, 
            'limit': 1, 
            'data': [
                {
                    'address_id': model_address_2.address_id, 
                    'person_id': model_address_2.person_id, 
                    'number': model_address_2.number, 
                    'state': model_address_2.state, 
                    'complement': model_address_2.complement, 
                    'city': model_address_2.city, 
                    'delivery': model_address_2.delivery, 
                    'invoice': model_address_2.invoice},], 
            'num_pages': 2}, response.json())

    def test_person_address_add_person_id_error(self):
        data_post = {
            'person_id': '',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'ID de pessoa não encontrado![78]'}, response.json())

    def test_person_address_add_person_not_found(self):
        data_post = {
            'person_id': '1234567890',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Registro de pessoa não encontrado![68]'}, response.json())

    def test_person_address_add_param_missing(self):
        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Dados insuficientes para criação de endereço![43]'}, response.json())
    
    def test_person_address_add_estate_error(self):
        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': 'KK',
            'city': 'Porto Alegre',
            'number': '123',
            'complement': '',
            'invoice': 'qwert',
            'delivery': 'gfdsa',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Sigla de estado incorreto![85]'}, response.json())

    def test_person_address_add_invoice_and_delivery_error(self):
        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': 'RS',
            'city': 'Porto Alegre',
            'number': '123',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor incorreto![45]'}, response.json())

    def test_person_address_add_invoice_and_delivery_error_2(self):
        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': 'RS',
            'city': 'Porto Alegre',
            'number': '123',
            'complement': '',
            'invoice': 'qwert',
            'delivery': 'gfdsa',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor incorreto![45]'}, response.json())

    def test_person_address_add_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address_2.save()

        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': 'RS',
            'city': 'Porto Alegre',
            'number': '123',
            'complement': 'Casa',
            'invoice': '0',
            'delivery': '0',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token,)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Endereço duplicado![46]'}, response.json())

    def test_person_address_add_ok(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=True,
            delivery=True,)
        model_address_2.save()

        data_post = {
            'person_id': self.model_person_client.person_id,
            'state': 'SC',
            'city': 'Florianópolis',
            'number': '123456',
            'complement': 'Pousada',
            'invoice': '1',
            'delivery': '1',
        }

        response = self.client.post('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'complement': data_post['complement'], 
            'state': data_post['state'], 
            'invoice': True, 
            'person_id': response.json()['person_id'], 
            'delivery': True, 
            'city': data_post['city'], 
            'address_id': response.json()['address_id'], 
            'number': data_post['number']}, response.json())

        self.assertEqual(
            ModelAddress.objects.filter(address_id=model_address_1.address_id,invoice=False,delivery=False).count(),1)
        self.assertEqual(
            ModelAddress.objects.filter(address_id=model_address_2.address_id,invoice=False,delivery=False).count(),1)

    def test_person_address_update_address_id_missing(self):
        data_post = {
            'address_id': '',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'ID de endereço não encontrado![82]'}, response.json())

    def test_person_address_update_address_not_find(self):
        data_post = {
            'address_id': '1234567890',
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Endereço não encontrado![50]'}, response.json())

    def test_person_address_update_param_missing(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        data_post = {
            'address_id': model_address_1.address_id,
            'state': '',
            'city': '',
            'number': '',
            'complement': '',
            'invoice': '',
            'delivery': '',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Nenhum dado para alterar![47]'}, response.json())

    def test_person_address_update_param_estate_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        data_post = {
            'address_id': model_address_1.address_id,
            'state': 'KK',
            'city': 'Porto Alegre',
            'number': '134567890',
            'complement': 'Apartamento',
            'invoice': 'error',
            'delivery': '1',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Sigla de estado incorreto![84]'}, response.json())

    def test_person_address_update_param_invoice_or_delivery_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        data_post = {
            'address_id': model_address_1.address_id,
            'state': 'RS',
            'city': 'Porto Alegre',
            'number': '134567890',
            'complement': 'Apartamento',
            'invoice': 'error',
            'delivery': '1',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Valor incorreto![48]'}, response.json())

    def test_person_address_update_ok(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        data_post = {
            'address_id': model_address_1.address_id,
            'state': 'RS',
            'city': 'Porto Alegre',
            'number': '134567890',
            'complement': 'Apartamento',
            'invoice': '1',
            'delivery': '1',
        }

        response = self.client.put('/api/v1/person/address/',json.dumps(data_post),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({
            'complement': data_post['complement'], 
            'address_id': data_post['address_id'], 
            'city': data_post['city'], 
            'state': data_post['state'], 
            'delivery': True, 
            'number': data_post['number'], 
            'person_id': model_address_1.person_id, 
            'invoice': True}, response.json())

        self.assertEqual(
            ModelAddress.objects.filter(address_id=model_address_1.address_id,invoice=True,delivery=True).count(),1)

    def test_person_address_delete_address_id_missing(self):
        data_delete = {
            'address_id': '',
        }

        response = self.client.delete('/api/v1/person/address/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'ID de endereço não encontrado![86]'}, response.json())

    def test_person_address_delete_address_not_found(self):
        data_delete = {
            'address_id': '1234567890',
        }

        response = self.client.delete('/api/v1/person/address/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Endereço não encontrado![51]'}, response.json())

    def test_person_address_delete_invoice_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=True,
            delivery=False,)
        model_address_1.save()

        data_delete = {
            'address_id': model_address_1.address_id,
        }

        response = self.client.delete('/api/v1/person/address/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Não é possível remover endereço de cobrança ou entrega![52]'}, response.json())

    def test_person_address_delete_delivery_error(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=False,
            delivery=True,)
        model_address_2.save()

        data_delete = {
            'address_id': model_address_2.address_id,
        }

        response = self.client.delete('/api/v1/person/address/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'message': 'Não é possível remover endereço de entrega ou cobrança![53]'}, response.json())

    def test_person_address_delete_ok(self):
        model_address_1 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='SP',
            city='São Paulo',
            number=321,
            complement='Apartamento',
            invoice=False,
            delivery=False,)
        model_address_1.save()

        model_address_2 = ModelAddress(
            person_id=self.model_person_client.person_id,
            state='RS',
            city='Porto Alegre',
            number=123,
            complement='Casa',
            invoice=False,
            delivery=False,)
        model_address_2.save()

        data_delete = {
            'address_id': model_address_2.address_id,
        }

        response = self.client.delete('/api/v1/person/address/',json.dumps(data_delete),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.8',
            HTTP_API_KEY=self.model_login_director.token)

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertEqual({'result': True}, response.json())

        self.assertEqual(
            ModelAddress.objects.filter().count(),1)