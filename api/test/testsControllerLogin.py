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

    def test_login_verify_http_not_allowed(self):
        response = self.client.get('/api/v1/login/verify/')

        self.assertEqual(response.status_code,405)
        self.assertTrue(isinstance(response,HttpResponseNotAllowed),'Não é um objeto do tipo "HttpResponseNotAllowed"')
