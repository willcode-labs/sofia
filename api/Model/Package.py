from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

class PackageManager(models.Manager):
    def create(self,request,**kwargs):
        self.name = request.POST.get('name',None)
        self.description = request.POST.get('description',None)
        self.price = request.POST.get('price',None)
        self.status = request.POST.get('status',None)
        self.weight = request.POST.get('weight',None)
        self.width = request.POST.get('width',None)
        self.length = request.POST.get('length',None)
        self.height = request.POST.get('height',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.price or not self.status or not self.weight \
            or not self.width or not self.length or not self.height:
            raise Exception('Dados insuficientes para criação de embalagem![134]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.price)):
            raise Exception('Formato de taxa incorreto![135]')

        self.price = Decimal(self.price).quantize(Decimal('0.00'))

        if self.status not in dict(Package.STATUS_LIST).keys():
            raise Exception('Status incorreto![136]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.weight)):
            raise Exception('Formato de peso incorreto![137]')

        self.weight = float(self.weight)

        if self.weight < Package.WEIGHT_VALUE_TUPLE[0] or self.weight > Package.WEIGHT_VALUE_TUPLE[1]:
            raise Exception('Valor para peso incorreto![138]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.width)):
            raise Exception('Formato de largura incorreto![139]')

        self.width = float(self.width)

        if self.width < Package.WIDTH_VALUE_TUPLE[0] or self.width > Package.WIDTH_VALUE_TUPLE[1]:
            raise Exception('Valor para largura incorreto![140]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.length)):
            raise Exception('Formato de comprimento incorreto![141]')

        self.length = float(self.length)

        if self.length < Package.LENGTH_VALUE_TUPLE[0] or self.length > Package.LENGTH_VALUE_TUPLE[1]:
            raise Exception('Valor para comprimento incorreto![142]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.height)):
            raise Exception('Formato de altura incorreto![143]')

        self.height = float(self.height)

        if self.height < Package.HEIGHT_VALUE_TUPLE[0] or self.height > Package.HEIGHT_VALUE_TUPLE[1]:
            raise Exception('Valor para altura incorreto![144]')

        if self.width + self.length + self.height > Package.MAX:
            raise Exception('Soma das medidas não pode ultrapassar 200cm![145]')

        try:
            package_name = Package.objects.filter(
                name=self.name)

            if package_name.count() > 0:
                raise Exception('Existe uma embalagem com este mesmo nome![146]')

            model_package = Package(
                name=self.name,
                description=self.description,
                price=self.price,
                status=self.status,
                weight=self.weight,
                width=self.width,
                length=self.length,
                height=self.height)

            model_package.save()

        except Exception as error:
            raise error

        return model_package

    def update(self,request,**kwargs):
        self.package_id = request.PUT.get('delivery_id',None)
        self.name = request.PUT.get('name',None)
        self.description = request.PUT.get('description',None)
        self.price = request.PUT.get('price',None)
        self.status = request.PUT.get('status',None)
        self.weight = request.PUT.get('weight',None)
        self.width = request.PUT.get('width',None)
        self.length = request.PUT.get('length',None)
        self.height = request.PUT.get('height',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.package_id or not re.match(r'^[0-9]+$',str(self.package_id)):
            raise Exception('ID de embalagem não encontrado![147]')

        self.package_id = int(self.package_id)

        try:
            model_package = Package.objects.get(package_id=self.package_id)

        except Exception as error:
            raise Exception('Registro de embalagem não encontrado![148]')

        if not self.name or not self.description or not self.price or not self.status \
            or not self.weight or not self.width or not self.length or not self.height:
            raise Exception('Dados insuficientes para atualizar entrega![149]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.price)):
            raise Exception('Formato de preço incorreto![150]')

        self.price = Decimal(self.price).quantize(Decimal('0.00'))

        if self.status not in dict(Package.STATUS_LIST).keys():
            raise Exception('Status incorreto![151]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.weight)):
            raise Exception('Formato de peso incorreto![152]')

        self.weight = float(self.weight)

        if self.weight < Package.WEIGHT_VALUE_TUPLE[0] or self.weight > Package.WEIGHT_VALUE_TUPLE[1]:
            raise Exception('Valor para peso incorreto![153]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.width)):
            raise Exception('Formato de largura incorreto![154]')

        self.width = float(self.width)

        if self.width < Package.WIDTH_VALUE_TUPLE[0] or self.width > Package.WIDTH_VALUE_TUPLE[1]:
            raise Exception('Valor para largura incorreto![155]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.length)):
            raise Exception('Formato de comprimento incorreto![156]')

        self.length = float(self.length)

        if self.length < Package.LENGTH_VALUE_TUPLE[0] or self.length > Package.LENGTH_VALUE_TUPLE[1]:
            raise Exception('Valor para comprimento incorreto![157]')

        if not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.height)):
            raise Exception('Formato de altura incorreto![158]')

        self.height = float(self.height)

        if self.height < Package.HEIGHT_VALUE_TUPLE[0] or self.height > Package.HEIGHT_VALUE_TUPLE[1]:
            raise Exception('Valor para altura incorreto![159]')

        if self.width + self.length + self.height > Package.MAX:
            raise Exception('Soma das medidas não pode ultrapassar 200cm![160]')

        try:
            package_name = Package.objects.filter(
                name=self.name).exclude(package_id=model_package.package_id)

            if package_name.count() > 0:
                raise Exception('Existe uma embalagem com este mesmo nome![161]')

            if self.name:
                model_package.name = self.name

            if self.description:
                model_package.description = self.description

            if self.price:
                model_package.price = self.price

            if self.status:
                model_package.status = self.status

            if self.weight:
                model_package.weight = self.weight

            if self.width:
                model_package.width = self.width

            if self.length:
                model_package.length = self.length

            if self.height:
                model_package.height = self.height

            model_package.save()

        except Exception as error:
            raise error

        return model_package

    def delete(self,request,**kwargs):
        self.delivery_id = request.DELETE.get('delivery_id',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        try:
            model_package = Package.objects.get(package_id=self.package_id)

        except Exception as error:
            raise Exception('Registro de embalagem não encontrado![162]')

        try:
            model_package.delete()

        except Exception as error:
            raise error

        return model_package

class Package(models.Model):
    STATUS_ACTIVE = 1
    STATUS_DEACTIVE = 2

    STATUS_LIST = (
        (STATUS_ACTIVE, 'Ativo'),
        (STATUS_DEACTIVE, 'Inativo'),)

    WEIGHT_VALUE_TUPLE = (0.01,30.00)
    WIDTH_VALUE_TUPLE = (11.00,105.00)
    LENGTH_VALUE_TUPLE = (16.00,105.00)
    HEIGHT_VALUE_TUPLE = (2.00,105.00)
    MAX = 200.00

    package_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,max_length=80)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    status = models.IntegerField(db_index=True,choices=STATUS_LIST)
    weight = models.FloatField(validators=[MinValueValidator(WEIGHT_VALUE_TUPLE[0],message='Min 0,1kg'),MaxValueValidator(WEIGHT_VALUE_TUPLE[1],message='Max 30,00kg')])
    width = models.FloatField(validators=[MinValueValidator(WIDTH_VALUE_TUPLE[0],message='Min 11,00cm'),MaxValueValidator(WIDTH_VALUE_TUPLE[1],message='Max 105,00cm')])
    length = models.FloatField(validators=[MinValueValidator(LENGTH_VALUE_TUPLE[0],message='Min 16,00cm'),MaxValueValidator(LENGTH_VALUE_TUPLE[1],message='Max 105,00cm')])
    height = models.FloatField(validators=[MinValueValidator(HEIGHT_VALUE_TUPLE[0],message='Min 2,00cm'),MaxValueValidator(HEIGHT_VALUE_TUPLE[1],message='Max 105,00cm')])
    date_create = models.DateTimeField(auto_now_add=True)

    objects = PackageManager()

    class Meta:
        db_table = 'package'
        ordering = ['-package_id']
        app_label = 'api'
