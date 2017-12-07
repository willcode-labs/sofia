import uuid,traceback
from django.db import models
from api.Model.Person import Person as ModelPerson

class AddressManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        person_id = request.POST.get('person_id',None)

        if not person_id:
            raise Exception('ID de pessoa não encontrado![78]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![44]')

        try:
            model_person = ModelPerson.objects.get(person_id=person_id)

        except Exception as error:
            raise Exception('Registro de pessoa não encontrado![68]')

        self.state = request.POST.get('state',None)
        self.city = request.POST.get('city',None)
        self.number = request.POST.get('number',None)
        self.complement = request.POST.get('complement',None)
        self.invoice = request.POST.get('invoice',None)
        self.delivery = request.POST.get('delivery',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.state or not self.city or not self.number:
            raise Exception('Dados insuficientes para criação de endereço![43]')

        if self.invoice not in ['0','1'] or self.delivery not in ['0','1']:
            raise Exception('Valor incorreto![45]')

        if self.invoice == '0':
            self.invoice = False

        else:
            self.invoice = True

        if self.delivery == '0':
            self.delivery = False

        else:
            self.delivery = True

        try:
            model_address_test = Address.objects.filter(
                person_id=model_person.person_id,
                state=self.state,
                number=self.number,
                complement=self.complement,)

            if model_address_test.count() >= 1:
                raise Exception('Endereço duplicado![46]')

            if not self.invoice and not self.delivery:
                model_address_test = Address.objects.filter(
                    person=model_person.person)

                if model_address_test.count() == 0:
                    self.invoice = True
                    self.delivery = True

            else:
                if not self.invoice:
                    model_address_invoice = Address.objects.filter(
                        person=model_person.person,
                        invoice=True)

                    if model_address_invoice.count() == 0:
                        self.invoice = True

                else:
                    model_address_invoice = Address.objects.filter(
                        person=model_person.person,
                        invoice=True).update(invoice=False)

                if not self.delivery:
                    model_address_delivery = Address.objects.filter(
                        person=model_person.person,
                        delivery=True)

                    if model_address_delivery.count() == 0:
                        self.delivery = True

                else:
                    model_address_delivery = Address.objects.filter(
                        person=model_person.person,
                        delivery=True).update(delivery=False)

            model_address = Address(
                person=model_person.person,
                state=self.state,
                city=self.city,
                number=self.number,
                complement=self.complement,
                invoice=self.invoice,
                delivery=self.delivery)

            model_address.save()

        except Exception as error:
            raise error

        return model_address

    def update(self,request,model_login,**kwargs):
        # TODO
        # alternativa para buscar diferentes protocolos de requisições HTTP
        # from django.http import QueryDict
        # put = QueryDict(request.body)
        # description = put.get('description')
        address_id = request.POST.get('address_id',None)

        if not address_id:
            # TODO
            raise Exception('ID de endereço não encontrado![xxx]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![49]')

        try:
            model_address = Address.objects.get(address_id=address_id,)

        except Exception as error:
            raise Exception('Endereço não encontrado![50]')

        self.state = request.POST.get('state',None)
        self.city = request.POST.get('city',None)
        self.number = request.POST.get('number',None)
        self.complement = request.POST.get('complement',None)
        self.invoice = request.POST.get('invoice',None)
        self.delivery = request.POST.get('delivery',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.city and not self.state and not self.number and not self.complement and not self.invoice and not self.delivery:
            raise Exception('Nenhum dado para alterar![47]')

        if self.invoice not in ['0','1'] or self.delivery not in ['0','1']:
            raise Exception('Valor incorreto![48]')

        if self.invoice == '0':
            self.invoice = False

        else:
            self.invoice = True

        if self.delivery == '0':
            self.delivery = False

        else:
            self.delivery = True

        try:
            if self.invoice:
                model_address_invoice = Address.objects.filter(
                    person=model_address.person,
                    invoice=True).update(invoice=False)

            if self.delivery:
                model_address_delivery = Address.objects.filter(
                    person=model_address.person,
                    delivery=True).update(delivery=False)

            if self.state:
                model_address.state = self.state

            if self.city:
                model_address.city = self.city

            if self.number:
                model_address.number = self.number

            if self.complement:
                model_address.complement = self.complement

            if self.invoice:
                model_address.invoice = self.invoice

            if self.delivery:
                model_address.delivery = self.delivery

            model_address.save()

        except Exception as error:
            raise error

        return model_address

    def delete(self,request,model_login,**kwargs):
        address_id = request.POST.get('address_id',None)

        if not address_id:
            # TODO
            raise Exception('ID de endereço não encontrado![xxx]')

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![69]')

        try:
            model_address = Address.objects.get(address_id=address_id)

        except Exception as error:
            raise Exception('Endereço não encontrado![51]')

        for key in kwargs:
            setattr(self,key,kwargs[key])

        try:
            if model_address.invoice:
                raise Exception('Não é possível remover endereço de cobrança ou entrega![52]')

            if model_address.delivery:
                raise Exception('Não é possível remover endereço de entrega ou cobrança![53]')

            model_address.delete()

        except Exception as error:
            raise error

        return True

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(ModelPerson,on_delete=models.CASCADE)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=80)
    number = models.IntegerField()
    complement = models.CharField(max_length=40,null=True)
    invoice = models.BooleanField()
    delivery = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = AddressManager()

    class Meta:
        db_table = 'address'
        ordering = ['-address_id']
        app_label = 'api'
