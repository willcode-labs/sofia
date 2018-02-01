from decimal import Decimal
from django.db import models

class DeliveryManager(models.Manager):
    def create(self,request,**kwargs):
        self.name = request.POST.get('name',None)
        self.description = request.POST.get('description',None)
        self.rate = request.POST.get('rate',None)
        self.status = request.POST.get('status',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.rate or not self.status:
            raise Exception('Dados insuficientes para criação de entrega![112]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.rate)):
            raise Exception('Formato de taxa incorreto![118]')

        self.rate = Decimal(self.rate).quantize(Decimal('0.00'))

        if self.status not in dict(Delivery.STATUS_LIST).keys():
            raise Exception('Status incorreto![119]')

        try:
            delivery_name = Delivery.objects.filter(
                name=self.name)

            if delivery_name.count() > 0:
                raise Exception('Existe uma entrega com este mesmo nome![120]')

            model_delivery = Delivery(
                name=self.name,
                description=self.description,
                rate=self.rate,
                status=self.status,)

            model_delivery.save()

        except Exception as error:
            raise error

        return model_delivery

    def update(self,request,**kwargs):
        self.delivery_id = request.PUT.get('delivery_id',None)
        self.name = request.PUT.get('name',None)
        self.description = request.PUT.get('description',None)
        self.rate = request.PUT.get('rate',None)
        self.status = request.PUT.get('status',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.delivery_id or not re.match(r'^[0-9]+$',str(self.delivery_id)):
            raise Exception('ID de entrega não encontrado![121]')

        self.delivery_id = int(self.delivery_id)

        try:
            model_delivery = Delivery.objects.get(delivery_id=self.delivery_id)

        except Exception as error:
            raise Exception('Registro de entrega não encontrado![122]')

        if not self.name or not self.description or not self.rate or not self.status:
            raise Exception('Dados insuficientes para atualizar entrega![123]')

        if self.rate and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.rate)):
            raise Exception('Formato de taxa incorreto![124]')

        if self.rate
            self.rate = Decimal(self.rate).quantize(Decimal('0.00'))

        if self.status and self.status not in dict(Delivery.STATUS_LIST).keys():
            raise Exception('Status incorreto![125]')

        try:
            delivery_name = Delivery.objects.filter(
                name=self.name).exclude(delivery_id=self.delivery_id)

            if delivery_name.count() > 0:
                raise Exception('Existe uma entrega com este mesmo nome![126]')

            if self.name:
                model_delivery.name = self.name

            if self.description:
                model_delivery.description = self.description

            if self.rate:
                model_delivery.rate = self.rate

            if self.status:
                model_delivery.status = self.status

            model_delivery.save()

        except Exception as error:
            raise error

        return model_delivery

    def delete(self,request,**kwargs):
        self.delivery_id = request.DELETE.get('delivery_id',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.delivery_id or not re.match(r'^[0-9]+$',str(self.delivery_id)):
            raise Exception('ID de entrega não encontrado![127]')

        self.delivery_id = int(self.deliver_id)

        try:
            model_delivery = Delivery.objects.get(delivery_id=self.delivery_id)

        except Exception as error:
            raise Exception('Registro de entrega não encontrado![128]')

        if model_delivery.status in [Delivery.STATUS_ACTIVE,]:
            raise Exception('Entrega ativo não pode ser removido![129]')

        try:
            model_delivery.delete()

        except Exception as error:
            raise error

        return model_delivery

class Delivery(models.Model):
    STATUS_ACTIVE = 1
    STATUS_DEACTIVE = 2

    STATUS_LIST = (
        (STATUS_ACTIVE, 'Ativo'),
        (STATUS_DEACTIVE, 'Inativo'),)

    delivery_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,max_length=80)
    description = models.TextField(null=True)
    rate = models.DecimalField(max_digits=8,decimal_places=2)
    status = models.IntegerField(choices=STATUS_LIST)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = DeliveryManager()

    class Meta:
        db_table = 'delivery'
        ordering = ['-delivery_id']
        app_label = 'api'
