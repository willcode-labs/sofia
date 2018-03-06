import uuid
from django.db import models
from api.Model.Person import Person as ModelPerson
from api.Model.App import App as ModelApp

class TokenManager(models.Manager):
    def tokenRecursive(self):
        token = str(uuid.uuid4())

        try:
            model_token_total = Token.objects.filter(
                token=token)

        except Exception as error:
            raise error

        if model_token_total.count() > 0:
            return self.tokenRecursive(self)

        return token

    def verify(self,request,model_token):
        """
        Método: Bussines.Auth.Auth.verify
        Atualiza o(s) dado(s): token,ip e date_expire.
        """
        if model_token.app.profile_id not in(ModelApp.PROFILE_CLIENT,):
            raise Exception('Perfil inválido para esta operação![168]')

        # TODO
        # backup register

        try:
            model_token.save()

        except Exception as error:
            raise error

        return model_token

    def auth(self,request,model_token):
        """
        Método: Bussines.Auth.Auth.auth
        Atualiza o(s) dado(s): date_expire.
        """
        if model_token.app.profile_id not in(ModelApp.PROFILE_CLIENT,):
            raise Exception('Perfil inválido para esta operação![180]')

        # TODO
        # backup register

        try:
            model_token.save()

        except Exception as error:
            raise error

        return model_token

class Token(models.Model):
    token_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(ModelPerson,on_delete=models.CASCADE)
    app = models.ForeignKey(ModelApp,on_delete=models.CASCADE)
    token = models.CharField(unique=True,max_length=40)
    ip = models.GenericIPAddressField(db_index=True,protocol='both')
    date_expire = models.DateTimeField(db_index=True,null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = TokenManager()

    class Meta:
        db_table = 'token'
        app_label = 'api'
