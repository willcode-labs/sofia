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
