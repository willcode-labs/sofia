import json
from django.db import models

class ExceptionManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        request_data = {
            'GET': request.GET.dict(),
            'POST': request.POST.dict(),
            'META': request.META,
            'COOKIES': request.COOKIES,
            'FILES': request.FILES.dict(),
        }

        request_data = json.dumps(str(request_data))

        ip = request.META.get('REMOTE_ADDR',None)
        url_referer = request.META.get('HTTP_REFERER',None)

        self.trace = None
        self.message = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        model_login_id = None

        if model_login:
            model_login_id = model_login.login_id

        try:
            model_exception_log = ExceptionLog(
                login_id=model_login_id,
                ip=ip,
                message=self.message,
                trace=self.trace,
                url_referer=url_referer,
                request_data=request_data)

            model_exception_log.save()

        except Exception as error:
            raise error

        return model_exception_log

class ExceptionLog(models.Model):
    exceptionlog_id = models.AutoField(primary_key=True)
    login_id = models.IntegerField(null=True)
    ip = models.GenericIPAddressField(protocol='both',null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    message = models.TextField()
    trace = models.TextField(null=True,blank=True)
    url_referer = models.URLField(max_length=254,null=True,blank=True)
    request_data = models.TextField(null=True,blank=True)

    objects = ExceptionManager()

    class Meta:
        db_table = 'exceptionlog'
        app_label = 'api'
