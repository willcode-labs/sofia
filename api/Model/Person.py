import re
from django.db import models
from django.core.validators import MinLengthValidator,EmailValidator,validate_email
from api.Model.App import App as ModelApp
from api.Exception.Api import Api as ExceptionApi

class PersonManager(models.Manager):
    def create(self,request,model_token,**kwargs):
        if model_token.person.profile_id not in (ModelApp.PROFILE_ROOT,ModelApp.PROFILE_DIRECTOR,):
            raise ExceptionApi('Tipo de perfil não permitido![188]')

        self.profile_id = request.POST.get('profile_id',None)
        self.name = request.POST.get('name',None)
        self.cpf = request.POST.get('cpf',None)
        self.cnpj = request.POST.get('cnpj',None)
        self.email = request.POST.get('email',None)
        self.phone1 = request.POST.get('phone1',None)
        self.phone2 = request.POST.get('phone2',None)
        self.username = self.email
        self.password = request.POST.get('password',None)
        self.verified = request.POST.get('verified',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.email or not self.password:
            raise ExceptionApi('Dados insuficientes para criação de pessoa![189]')

        if not re.match(r'^[0-9]+$',str(self.profile_id)):
            raise ExceptionApi('ID de perfil incorreto![113]')

        if self.profile_id not in dict(ModelApp.PROFILE_TUPLE).keys():
            raise ExceptionApi('Tipo de perfil incorreto![70]')

        if model_token.profile_id == ModelApp.PROFILE_ROOT and self.profile_id not in (ModelApp.PROFILE_DIRECTOR,ModelApp.PROFILE_CLIENT):
            raise ExceptionApi('Perfil não pode criar este tipo de pessoa![211]')

        if model_token.profile_id == ModelApp.PROFILE_DIRECTOR and self.profile_id != ModelApp.PROFILE_CLIENT:
            raise ExceptionApi('Perfil não pode criar este tipo de pessoa![72]')

        try:
            validate_email(self.email)

        except Exception as error:
            raise ExceptionApi('Formato do email incorreto![210]')

        if not self.cpf and not self.cnpj:
            raise ExceptionApi('Um dos campos deve estar preenchido, CPF ou CNPJ![190]')

        if self.cpf and not re.match(r'^[0-9]{11}$',str(self.cpf)):
            raise ExceptionApi('CPF incorreto![191]')

        if self.cnpj and not re.match(r'^[0-9]{14}$',str(self.cnpj)):
            raise ExceptionApi('CNPJ incorreto![192]')

        if self.phone1 and not re.match(r'^[0-9]{10,15}$',str(self.phone1)):
            raise ExceptionApi('Telefone 1 incorreto![193]')

        if self.phone2 and not re.match(r'^[0-9]{10,15}$',str(self.phone2)):
            raise ExceptionApi('Telefone 2 incorreto![194]')

        if self.username.__len__() < 6 or self.username.__len__() > 150:
            raise ExceptionApi('Username deve estar entre 6 e 150 caracteres![195]')

        if self.password.__len__() != 8:
            raise ExceptionApi('Password deve ter 8 caracteres![196]')

        if not self.verified in ('0','1'):
            raise Exception('Valor do parâmetro verified incorreto![186]')

        self.verified = False if self.verified == '0' else True

        if self.cpf:
            model_person_cpf = Person.objects.filter(
                cpf=self.cpf)

            if model_person_cpf.count() > 0:
                raise ExceptionApi('Existe uma pessoa cadastrada com este mesmo CPF![197]')

        if self.cnpj:
            model_person_cnpj = Person.objects.filter(
                cnpj=self.cnpj)

            if model_person_cnpj.count() > 0:
                raise ExceptionApi('Existe uma pessoa cadastrada com este mesmo CNPJ![198]')

        model_person_email = Person.objects.filter(
            email=self.email)

        if model_person_email.count() > 0:
            raise ExceptionApi('Existe uma pessoa cadastrada com este mesmo E-mail![199]')

        model_person_username = Person.objects.filter(
            username=self.username)

        if model_person_username.count() > 0:
            raise ExceptionApi('Existe uma pessoa cadastrada com este mesmo username![200]')

        model_person = Person(
            profile_id=self.profile_id,
            name=self.name,
            cpf=self.cpf,
            cnpj=self.cnpj,
            email=self.email,
            phone1=self.phone1,
            phone2=self.phone2,
            username=self.username,
            password=self.password,
            verified=self.verified)

        model_person.save()

        # TODO
        # servico de email
        # notifica o usuario pelo email de cadastro
        # no email deve estar o link de verificacao

        return model_person

    def verify(self,request,model_token,model_person):
        """
        Método: Bussines.Auth.Auth.verify
        Atualiza o(s) dado(s): verified.
        """
        if model_token.app.profile_id not in(ModelApp.PROFILE_CLIENT,):
            raise ExceptionApi('Perfil inválido para esta operação![169]')

        # TODO
        # backup register

        model_person.save()

        return model_person

class Person(models.Model):
    PROFILE_ROOT = ModelApp.PROFILE_ROOT
    PROFILE_DIRECTOR = ModelApp.PROFILE_DIRECTOR
    PROFILE_CLIENT = ModelApp.PROFILE_CLIENT

    PROFILE_TUPLE = ModelApp.PROFILE_TUPLE

    person_id = models.AutoField(primary_key=True)
    profile_id = models.IntegerField(db_index=True,choices=ModelApp.PROFILE_TUPLE)
    name = models.CharField(unique=True,max_length=150)
    cpf = models.CharField(unique=True,max_length=11,null=True,validators=[MinLengthValidator(11,message='Min 11 caracteres')])
    cnpj = models.CharField(unique=True,max_length=14,null=True,validators=[MinLengthValidator(14,message='Min 14 caracteres')])
    email = models.EmailField(unique=True,max_length=150,validators=[EmailValidator(message='Formato de email incorreto!')])
    phone1 = models.CharField(max_length=15,null=True,validators=[MinLengthValidator(10,message='Min 10 caracteres')])
    phone2 = models.CharField(max_length=15,null=True,validators=[MinLengthValidator(10,message='Min 10 caracteres')])
    username = models.CharField(unique=True,max_length=150,validators=[MinLengthValidator(6,message='Min 6 caracteres')])
    password = models.CharField(db_index=True,max_length=8,validators=[MinLengthValidator(8,message='Min 8 caracteres')])
    verified = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        ordering = ['-person_id']
        app_label = 'api'
