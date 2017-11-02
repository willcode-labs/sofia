from django.db import models

class PersonManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        self.profile_id = request.POST.get('profile_id',None)
        self.name = request.POST.get('name',None)
        self.cpf = request.POST.get('cpf',None)
        self.cnpj = request.POST.get('cnpj',None)
        self.email = request.POST.get('email',None)
        self.phone1 = request.POST.get('phone1',None)
        self.phone2 = request.POST.get('phone2',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.profile_id or not self.name or not self.email or not self.phone1:
            raise Exception('Dados insuficientes para criação de pessoa![30]')

        if not self.cpf and not self.cnpj:
            raise Exception('Um dos campos deve estar preenchido, CPF ou CNPJ![74]')

        self.phone2 = None if self.phone2 == '' else self.phone2

        if self.profile_id not in dict(ModelLogin.PROFILE_TUPLE).keys():
            raise Exception('Tipo de perfil incorreto![70]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![31]')

        if model_login.profile_id == model_login.PROFILE_ROOT and self.profile_id not in(model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,model_login.PROFILE_CLIENT,):
            raise Exception('Perfil não pode criar este tipo de pessoa![71]')

        if model_login.profile_id == model_login.PROFILE_DIRECTOR and self.profile_id not in(model_login.PROFILE_DIRECTOR,model_login.PROFILE_CLIENT,):
            raise Exception('Perfil não pode criar este tipo de pessoa![72]')

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
    cpf = models.CharField(max_length=12,null=True)
    cnpj = models.CharField(max_length=14,null=True)
    email = models.EmailField(max_length=254)
    phone1 = models.CharField(max_length=60)
    phone2 = models.CharField(max_length=60,null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        ordering = ['-person_id']
        app_label = 'api'
