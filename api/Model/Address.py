import uuid,traceback
from django.db import models
from api.Model.Person import Person as ModelPerson

class AddressManager(models.Manager):
    def create(self,request,model_login,model_person,**kwargs):
        self.state = None
        self.city = None
        self.number = None
        self.complement = None
        self.invoice = None
        self.delivery = None

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

        if model_login.profile_id not in (model_login.PROFILE_MERCHANT,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![44]')

        try:
            model_address_test = Address.objects.filter(
                    person=model_person,
                    state=self.state,
                    number=self.number,
                    complement=self.complement,)

            if model_address_test.count() >= 1:
                raise Exception('Endereço duplicado![46]')

            if not self.invoice and not self.delivery:
                model_address_test = Address.objects.filter(
                    person=model_person)

                if model_address_test.count() == 0:
                    self.invoice = True
                    self.delivery = True

            else:
                if self.invoice:
                    model_address_invoice = Address.objects.filter(
                        person=model_person,
                        invoice=True)

                    if model_address_invoice.count() >= 1:
                        model_address_invoice[0].invoice = False
                        model_address_invoice[0].save()

                if self.delivery:
                    model_address_delivery = Address.objects.filter(
                        person=model_person,
                        delivery=True)

                    if model_address_delivery.count() >= 1:
                        model_address_delivery[0].delivery = False
                        model_address_delivery[0].save()

            model_address = Address(
                person=model_person,
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

    def update(self,request,model_login,model_person,**kwargs):
        self.address_id = None
        self.state = None
        self.city = None
        self.number = None
        self.complement = None
        self.invoice = None
        self.delivery = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.address_id:
            raise Exception('Necessário informar um ID de endereço!')

        if not self.city and not self.state and not self.number and not self.complement and not self.invoice and not self.delivery:
            raise Exception('Atenção, nenhum dado para alterar!')

        try:
            try:
                model_address = ModelAddress.objects.get(
                    address_id=self.address_id,
                    person=model_person)

            except Exception as error:
                raise Exception('Endereço não encontrado!')

            if not self.invoice and not self.delivery:
                self.invoice = False
                self.delivery = False

            elif self.invoice == True:
                model_address_invoice = Address.objects.get(
                    person=model_person,
                    invoice=True)

                model_address_invoice.invoice = False
                model_address_invoice.save()

            elif self.delivery == True:
                model_address_delivery = Address.objects.get(
                    person=model_person,
                    delivery=True)

                model_address_delivery.delivery = False
                model_address_delivery.save()

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

    def delete(self,request,model_login,model_person,**kwargs):
        self.address_id = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.address_id:
            raise Exception('Dados insuficientes para remoção de endereço!')

        try:
            try:
                model_address = ModelAddress.objects.get(
                    address_id=self.address_id,
                    person=model_person)

            except Exception as error:
                raise Exception('Endereço não encontrado!')

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
        app_label = 'api'
