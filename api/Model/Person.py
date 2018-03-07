from django.db import models
from django.core.validators import MinLengthValidator
from api.Model.App import App as ModelApp
from api.Exception.Api import Api as ExceptionApi

class PersonManager(models.Manager):
    def createSimple:
        if model_token.profile_id not in (ModelApp.PROFILE_ROOT,ModelApp.PROFILE_DIRECTOR,ModelApp.PROFILE_CLIENT,):
            raise ExceptionApi('Tipo de perfil não permitido![188]')

        self.profile_id = ModelApp.PROFILE_CLIENT
        self.name = request.POST.get('name',None)
        self.cpf = request.POST.get('cpf',None)
        self.cnpj = request.POST.get('cnpj',None)
        self.email = request.POST.get('email',None)
        self.phone1 = request.POST.get('phone1',None)
        self.phone2 = request.POST.get('phone2',None)
        self.username = self.email
        self.password = request.POST.get('password',None)
        self.verified = False

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if self.name or not self.email or not self.password:
            raise ExceptionApi('Dados insuficientes para criação de pessoa![189]')

        # if not self.cpf and not self.cnpj:
        #     raise ExceptionApi('Um dos campos deve estar preenchido, CPF ou CNPJ![74]')

        # if self.cpf and not re.match(r'^[0-9]{11}$',str(self.cpf)):
        #     raise ExceptionApi('CPF incorreto![114]')

        # if self.cnpj and not re.match(r'^[0-9]{14}$',str(self.cnpj)):
        #     raise ExceptionApi('CNPJ incorreto![115]')

        # if self.phone1 and not re.match(r'^[0-9]{10,15}$',str(self.phone1)):
        #     raise ExceptionApi('Telefone 1 incorreto![116]')

        # self.phone2 = None if self.phone2 == '' else self.phone2

        # if self.phone2 and not re.match(r'^[0-9]{10,15}$',str(self.phone2)):
        #     raise ExceptionApi('Telefone 2 incorreto![117]')

        # if self.username.__len__() < 6 or self.username.__len__() > 150:
        #     raise ExceptionApi('Username deve estar entre 6 e 150 caracteres![184]')

        # if self.password.__len__() != 8:
        #     raise ExceptionApi('Password deve ter 8 caracteres![185]')

    def create(self,request,model_token,**kwargs):
        if model_token.profile_id not in (ModelApp.PROFILE_ROOT,ModelApp.PROFILE_DIRECTOR,):
            raise ExceptionApi('Tipo de perfil não permitido![31]')

        self.profile_id = request.POST.get('profile_id',None)
        self.name = request.POST.get('name',None)
        self.cpf = request.POST.get('cpf',None)
        self.cnpj = request.POST.get('cnpj',None)
        self.email = request.POST.get('email',None)
        self.phone1 = request.POST.get('phone1',None)
        self.phone2 = request.POST.get('phone2',None)
        self.username = request.POST.get('username',None)
        self.password = request.POST.get('password',None)
        self.verified = request.POST.get('verified',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.profile_id or not self.name or not self.email or not self.phone1 \
        or not self.username or not self.password or not self.verified:
            raise ExceptionApi('Dados insuficientes para criação de pessoa![30]')

        if not re.match(r'^[0-9]+$',str(self.profile_id)):
            raise ExceptionApi('ID de perfil incorreto![113]')

        self.profile_id = int(self.profile_id)

        if self.profile_id not in dict(ModelApp.PROFILE_TUPLE).keys():
            raise ExceptionApi('Tipo de perfil incorreto![70]')

        if model_token.profile_id == ModelApp.PROFILE_DIRECTOR and self.profile_id not in(model_login.PROFILE_DIRECTOR,model_login.PROFILE_CLIENT,):
            raise ExceptionApi('Perfil não pode criar este tipo de pessoa![72]')

        if not self.cpf and not self.cnpj:
            raise ExceptionApi('Um dos campos deve estar preenchido, CPF ou CNPJ![74]')

        if self.cpf and not re.match(r'^[0-9]{11}$',str(self.cpf)):
            raise ExceptionApi('CPF incorreto![114]')

        if self.cnpj and not re.match(r'^[0-9]{14}$',str(self.cnpj)):
            raise ExceptionApi('CNPJ incorreto![115]')

        if self.phone1 and not re.match(r'^[0-9]{10,15}$',str(self.phone1)):
            raise ExceptionApi('Telefone 1 incorreto![116]')

        self.phone2 = None if self.phone2 == '' else self.phone2

        if self.phone2 and not re.match(r'^[0-9]{10,15}$',str(self.phone2)):
            raise ExceptionApi('Telefone 2 incorreto![117]')

        if self.username.__len__() < 6 or self.username.__len__() > 150:
            raise ExceptionApi('Username deve estar entre 6 e 150 caracteres![184]')

        if self.password.__len__() != 8:
            raise ExceptionApi('Password deve ter 8 caracteres![185]')

        if not self.verified in ('0','1'):
            raise Exception('Valor do parâmetro verified incorreto![186]')

        self.verified = False if self.verified == '0' else True

        if self.cpf:
            model_person_cpf = Person.objects.filter(
                cpf=self.cpf)

            if model_person_cpf.count() > 0:
                raise ExceptionApi('Já existe uma pessoa cadastrada com este mesmo CPF![32]')

        if self.cnpj:
            model_person_cnpj = Person.objects.filter(
                cnpj=self.cnpj)

            if model_person_cnpj.count() > 0:
                raise ExceptionApi('Já existe uma pessoa cadastrada com este mesmo CNPJ![77]')

        model_person_email = Person.objects.filter(
            email=self.email)

        if model_person_email.count() > 0:
            raise ExceptionApi('Já existe uma pessoa cadastrada com este mesmo E-mail![33]')

        model_person_username = Person.objects.filter(
            username=self.username)

        if model_person_username.count() > 0:
            raise ExceptionApi('Já existe uma pessoa cadastrada com este mesmo username![187]')

        model_person = Person(
            profile_id=Person.PROFILE_CLIENT,
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
    PROFILE_CLIENT = ModelApp.PROFILE_CLIENT

    person_id = models.AutoField(primary_key=True)
    profile_id = models.IntegerField(db_index=True,choices=ModelApp.PROFILE_TUPLE)
    name = models.CharField(unique=True,max_length=150)
    cpf = models.CharField(unique=True,max_length=11,null=True)
    cnpj = models.CharField(unique=True,max_length=14,null=True)
    email = models.EmailField(unique=True,max_length=150)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15,null=True)
    username = models.CharField(unique=True,max_length=150,validators=[MinLengthValidator(6,message='Min 6 caracteres')])
    password = models.CharField(db_index=True,max_length=8,validators=[MinLengthValidator(8,message='Min 8 caracteres')])
    verified = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        ordering = ['-person_id']
        app_label = 'api'
