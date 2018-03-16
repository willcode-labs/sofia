import datetime,json
from django.test import Client,TestCase,TransactionTestCase
from api.apps import ApiConfig
from api.Model.App import App as ModelApp
from api.Model.Token import Token as ModelToken
from api.Model.Person import Person as ModelPerson
from api.Model.Address import Address as ModelAddress

class TestControllerPerson(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = Client()

        # Person ROOT
        self.model_person_root = ModelPerson(
            profile_id=ModelApp.PROFILE_ROOT,
            name='William Borba ROOT',
            cpf='00000000001',
            cnpj='00000000001',
            email='emailroot@test.com',
            phone1='99123456789',
            phone2=None,
            username='wborba_root',
            password='12345678',
            verified=True)

        self.model_person_root.save()

        self.model_app_root = ModelApp(
            profile_id=ModelApp.PROFILE_ROOT,
            apikey='apikey-root',
            name='ROOT APIKEY',
            describe='APIKEY for ROOT',
            active=True)

        self.model_app_root.save()

        self.model_token_root = ModelToken(
            person=self.model_person_root,
            app=self.model_app_root,
            token='token-root',
            ip='127.0.0.1',
            date_expire=datetime.datetime.now() + datetime.timedelta(days=30))

        self.model_token_root.save()

        # Person DIRECTOR
        self.model_person_director = ModelPerson(
            profile_id=ModelApp.PROFILE_DIRECTOR,
            name='William Borba DIRECTOR',
            cpf='00000000002',
            cnpj='00000000002',
            email='emaildirector@test.com',
            phone1='99123456788',
            phone2=None,
            username='wborba_director',
            password='12345678',
            verified=True)

        self.model_person_director.save()

        self.model_app_director = ModelApp(
            profile_id=ModelApp.PROFILE_DIRECTOR,
            apikey='apikey-director',
            name='DIRECTOR APIKEY',
            describe='APIKEY for DIRECTOR',
            active=True)

        self.model_app_director.save()

        self.model_token_director = ModelToken(
            person=self.model_person_director,
            app=self.model_app_director,
            token='token-director',
            ip='127.0.0.2',
            date_expire=datetime.datetime.now() + datetime.timedelta(days=30))

        self.model_token_director.save()

        # Person CLIENT
        self.model_person_client = ModelPerson(
            profile_id=ModelPerson.PROFILE_CLIENT,
            name='William Borba CLIENT',
            cpf='00000000003',
            cnpj='00000000003',
            email='emailclient@test.com',
            phone1='99123456788',
            phone2=None,
            username='wborba_client',
            password='12345678',
            verified=True)

        self.model_person_client.save()

        self.model_app_client = ModelApp(
            profile_id=ModelApp.PROFILE_CLIENT,
            apikey='apikey-client',
            name='CLIENT APIKEY',
            describe='APIKEY for CLIENT',
            active=True)

        self.model_app_client.save()

        self.model_token_client = ModelToken(
            person=self.model_person_client,
            app=self.model_app_client,
            token='token-client',
            ip='127.0.0.3',
            date_expire=datetime.datetime.now() + datetime.timedelta(minutes=ApiConfig.token_time_client))

        self.model_token_client.save()