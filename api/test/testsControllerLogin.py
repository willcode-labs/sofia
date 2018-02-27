import uuid,datetime,json
from django.test import Client,TestCase,TransactionTestCase
from django.http import HttpResponseNotAllowed
from api.Model.Person import Person as ModelPerson
from api.Model.App import App as ModelApp
from api.Model.Token import Token as ModelToken

class TestControllerLogin(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        # Person ROOT
        self.model_person_root = ModelPerson(
            parent_id=None,
            name='William Borba',
            cpf='00000000000',
            cnpj='00000000000',
            email='emailroot@test.com',
            phone1='99123456789',
            phone2=None,
            username='wborba',
            password='12345678',
            verified=False)

        self.model_person_root.save()

        self.model_app_root = ModelApp(
            profile_id=ModelApp.PROFILE_ROOT,
            apikey='apikey-root',
            name='ROOT APIKEY',
            describe='APIKEY for ROOT',
            active=True)

        self.model_app_root.save()

        self.model_token_root = ModelToken(
            person_id=self.model_person_root,
            app_id=self.model_app_root,
            token='token-root',
            ip='127.0.0.1',
            date_expire=datetime.datetime.now() + datetime.timedelta(days=30),)

        self.model_token_root.save()

    def test_auth_verify_ip_not_found(self):
        response = self.client.post('/api/v1/login/verify/',json.dumps({}),
            content_type='application/json',
            REMOTE_ADDR=None,
            HTTP_API_KEY=None,)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['message'],'IP não encontrado![1]')
