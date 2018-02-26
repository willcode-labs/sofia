import uuid,traceback
from django.db import models
from api.Model.Person import Person as ModelPerson
from api.Model.App import App as ModelApp

class TokenManager(models.Manager):
    def tokenRecursive(self,ip):
        token = str(uuid.uuid4())

        try:
            model_login_total = Login.objects.filter(
                token=token,
                ip=ip)

        except Exception as error:
            raise error

        if model_login_total.count() > 0:
            return self.tokenRecursive(self,ip)

        return token

    def create(self,request,model_login,model_person,**kwargs):
        ip = request.META.get('REMOTE_ADDR',None)

        if not ip:
            raise Exception('Ip não encontrado![73]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![34]')

        try:
            model_login_username = Login.objects.filter(
                username=model_person.email)

            if model_login_username.count() > 0:
                raise Exception('Já existe um usuário com este mesmo email![35]')

            token = self.tokenRecursive(ip)

            model_login_to_save = Login(
                person=model_person,
                profile_id=Login.PROFILE_CLIENT,
                username=model_person.email,
                password=None,
                verified=False,
                token=token,
                ip=None,
                date_expired=None)

            model_login_to_save.save()

        except Exception as error:
            raise error

        return model_login_to_save

    def update(self,request,model_login,**kwargs):
        if model_login.profile_id not in(Login.PROFILE_ROOT,Login.PROFILE_DIRECTOR,Login.PROFILE_CLIENT):
            raise Exception('Perfil inválido para esta operação![75]')

        try:
            if 'token' in kwargs.keys():
                model_login.token = kwargs['token']

            if 'ip' in kwargs.keys():
                model_login.ip = kwargs['ip']

            if 'date_expired' in kwargs.keys():
                model_login.date_expired = kwargs['date_expired']

            if 'verified' in kwargs.keys():
                model_login.verified = kwargs['verified']

            model_login.save()

        except Exception as error:
            raise error

        return model_login

class Token(models.Model):
    token_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(ModelPerson,on_delete=models.CASCADE)
    app_id = models.ForeignKey(ModelApp,on_delete=models.CASCADE,null=True)
    token = models.CharField(db_index=True,max_length=40,null=True)
    ip = models.GenericIPAddressField(db_index=True,protocol='both',null=True)
    date_expire = models.DateTimeField(db_index=True,null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = TokenManager()

    class Meta:
        db_table = 'token'
        app_label = 'api'
