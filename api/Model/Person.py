from django.db import models

class PersonManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        self.name = request.POST.get('name',None)
        self.cpf = request.POST.get('cpf',None)
        self.email = request.POST.get('email',None)
        self.phone1 = request.POST.get('phone1',None)
        self.phone2 = request.POST.get('phone2',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.cpf or not self.email or not self.phone1:
            raise Exception('Dados insuficientes para criação de pessoa![30]')

        if model_login.profile_id not in (model_login.PROFILE_MERCHANT,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![31]')

        try:
            model_person_cpf = Person.objects.filter(
                cpf=self.cpf)

            if model_person_cpf.count() > 0:
                raise Exception('Já existe uma pessoa cadastrada com este mesmo CPF![32]')

            model_person_email = Person.objects.filter(
                email=self.email)

            if model_person_email.count() > 0:
                raise Exception('Já existe uma pessoa cadastrada com este mesmo E-mail![33]')

            model_person = Person(
                parent=model_login.person,
                name=self.name,
                cpf=self.cpf,
                email=self.email,
                phone1=self.phone1,
                phone2=self.phone2,)

            model_person.save()

        except Exception as error:
            raise error

        return model_person

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self',null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    phone1 = models.CharField(max_length=60)
    phone2 = models.CharField(max_length=60,null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        ordering = ['-person_id']
        app_label = 'api'
