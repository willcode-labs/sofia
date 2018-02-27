import uuid,traceback
from django.db import models

class AppManager(models.Manager):
    def hashRecursive(self):
        hash_code = str(uuid.uuid4())

        try:
            model_app_apikey = App.objects.filter(
                apikey=apikey)

        except Exception as error:
            raise error

        if model_app_apikey.count() > 0:
            return self.hashRecursive(self)

        return hash_code

    def create(self,request,model_login,**kwargs):
        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Usuário não autorizado![163]')

        # try:
        #     model_login_username = Login.objects.filter(
        #         username=model_person.email)

        #     if model_login_username.count() > 0:
        #         raise Exception('Já existe um usuário com este mesmo email![35]')

        #     token = self.tokenRecursive(ip)

        #     model_login_to_save = Login(
        #         person=model_person,
        #         profile_id=Login.PROFILE_CLIENT,
        #         username=model_person.email,
        #         password=None,
        #         verified=False,
        #         token=token,
        #         ip=None,
        #         date_expired=None)

        #     model_login_to_save.save()

        # except Exception as error:
        #     raise error

        # return model_login_to_save
        return False

class App(models.Model):
    PROFILE_ROOT = 1
    PROFILE_DIRECTOR = 2
    PROFILE_CLIENT = 3

    PROFILE_TUPLE = (
        (PROFILE_ROOT, 'root'),
        (PROFILE_DIRECTOR, 'director'),
        (PROFILE_CLIENT, 'client'),)

    app_id = models.AutoField(primary_key=True)
    profile_id = models.IntegerField(db_index=True,choices=PROFILE_TUPLE)
    apikey = models.CharField(unique=True,max_length=40)
    name = models.CharField(unique=True,max_length=80)
    describe = models.TextField()
    active = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = AppManager()

    class Meta:
        db_table = 'app'
        app_label = 'api'
