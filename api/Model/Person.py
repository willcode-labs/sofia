from django.db import models
from django.core.validators import MinLengthValidator
from api.Model.App import App as ModelApp

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

        if self.profile_id and not re.match(r'^[0-9]+$',str(self.profile_id)):
            raise Exception('ID de perfil incorreto![113]')

        self.profile_id = int(self.profile_id)

        if self.profile_id not in dict(model_login.PROFILE_TUPLE).keys():
            raise Exception('Tipo de perfil incorreto![70]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Tipo de perfil não permitido![31]')

        if model_login.profile_id == model_login.PROFILE_ROOT and self.profile_id not in(model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,model_login.PROFILE_CLIENT,):
            raise Exception('Perfil não pode criar este tipo de pessoa![71]')

        if model_login.profile_id == model_login.PROFILE_DIRECTOR and self.profile_id not in(model_login.PROFILE_DIRECTOR,model_login.PROFILE_CLIENT,):
            raise Exception('Perfil não pode criar este tipo de pessoa![72]')

        if not self.cpf and not self.cnpj:
            raise Exception('Um dos campos deve estar preenchido, CPF ou CNPJ![74]')

        if self.cpf and not re.match(r'^[0-9]{11}$',str(self.cpf)):
            raise Exception('CPF incorreto![114]')

        if self.cnpj and not re.match(r'^[0-9]{14}$',str(self.cnpj)):
            raise Exception('CNPJ incorreto![115]')

        self.phone2 = None if self.phone2 == '' else self.phone2

        if self.phone1 and not re.match(r'^[0-9]{10,15}$',str(self.phone1)):
            raise Exception('Telefone 1 incorreto![116]')

        if self.phone2 and not re.match(r'^[0-9]{10,15}$',str(self.phone2)):
            raise Exception('Telefone 2 incorreto![117]')

        try:
            if self.cpf:
                model_person_cpf = Person.objects.filter(
                    cpf=self.cpf)

                if model_person_cpf.count() > 0:
                    raise Exception('Já existe uma pessoa cadastrada com este mesmo CPF![32]')

            if self.cnpj:
                model_person_cnpj = Person.objects.filter(
                    cnpj=self.cnpj)

                if model_person_cnpj.count() > 0:
                    raise Exception('Já existe uma pessoa cadastrada com este mesmo CNPJ![77]')

            model_person_email = Person.objects.filter(
                email=self.email)

            if model_person_email.count() > 0:
                raise Exception('Já existe uma pessoa cadastrada com este mesmo E-mail![33]')

            model_person = Person(
                parent=model_login.person,
                name=self.name,
                cpf=self.cpf,
                cnpj=self.cnpj,
                email=self.email,
                phone1=self.phone1,
                phone2=self.phone2,)

            model_person.save()

        except Exception as error:
            raise error

        return model_person

    def verify(self,request,model_token,model_person):
        if model_token.app.profile_id not in(ModelApp.PROFILE_CLIENT,):
            raise Exception('Perfil inválido para esta operação![169]')

        # TODO
        # backup register

        try:
            model_person.save()

        except Exception as error:
            raise error

        return model_person

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,max_length=50)
    cpf = models.CharField(unique=True,max_length=11,null=True)
    cnpj = models.CharField(unique=True,max_length=14,null=True)
    email = models.EmailField(unique=True,max_length=150)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15,null=True)
    username = models.CharField(unique=True,max_length=40,validators=[MinLengthValidator(6,message='Min 6 caracteres')])
    password = models.CharField(db_index=True,max_length=8,validators=[MinLengthValidator(8,message='Min 8 caracteres')])
    verified = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        ordering = ['-person_id']
        app_label = 'api'
