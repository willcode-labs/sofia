import uuid,traceback
from django.db import models
from api.Model.Login import Login as ModelLogin

class MerchantManager(models.Manager):
    def create(self,request,model_login,model_person,**kwargs):
        # person/add via apikey root
        # merchant/add via apikey root
        pass

class Merchant(models.Model):
    merchant_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(ModelLogin,on_delete=models.CASCADE)
    date_expired = models.DateTimeField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = MerchantManager()

    class Meta:
        db_table = 'merchant'
        app_label = 'api'
