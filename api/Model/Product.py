import re
from django.db import models

class ProductManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        self.name = request.POST.get('name',None)
        self.description = request.POST.get('description',None)
        self.code = request.POST.get('code',None)
        self.compound = request.POST.get('compound',None)
        self.unit_weight = request.POST.get('unit_weight',None)
        self.weight = request.POST.get('weight',None)
        self.width = request.POST.get('width',None)
        self.length = request.POST.get('length',None)
        self.height = request.POST.get('height',None)
        self.origin = request.POST.get('origin',None)
        self.gtin = request.POST.get('gtin',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.description or not self.code or not self.unit_weight or not self.origin:
            raise Exception('Dados insuficientes para criação de produto![58]')

        self.compound = None if self.compound == '' else self.compound
        self.weight = None if self.weight == '' else self.weight
        self.width = None if self.width == '' else self.width
        self.length = None if self.length == '' else self.length
        self.height = None if self.height == '' else self.height
        self.gtin = None if self.gtin == '' else self.gtin

        if self.compound and not self.compound in ('0','1'):
            raise Exception('Valor do parâmetro composto incorreto![63]')

        self.compound = True if self.compound == '1' else self.compound
        self.compound = False if self.compound == '0' else self.compound

        if self.weight and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',self.weight):
            raise Exception('Valor do parâmetro peso incorreto![64]')

        self.weight = float(self.weight) if self.weight else self.weight

        if self.width and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',self.width):
            raise Exception('Valor do parâmetro largura incorreto![65]')

        self.width = float(self.width) if self.width else self.width

        if self.length and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',self.length):
            raise Exception('Valor do parâmetro comprimento incorreto![66]')

        self.length = float(self.length) if self.length else self.length

        if self.height and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',self.height):
            raise Exception('Valor do parâmetro altura incorreto![67]')

        self.height = float(self.height) if self.height else self.height

        if not self.unit_weight or not re.match(r'^[0-9]+$',self.unit_weight) or int(self.unit_weight) not in dict(Product.UNIT_WEIGHT_LIST).keys():
            raise Exception('Unidade de medida recusada![59]')

        self.unit_weight = int(self.unit_weight)

        if not self.origin or not re.match(r'^[0-9]+$',self.origin) or int(self.origin) not in dict(Product.ORIGIN_LIST).keys():
            raise Exception('Origen recusada![60]')

        self.origin = int(self.origin)

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![61]')

        try:
            product_code_equal = Product.objects.filter(code=self.code)

            if product_code_equal.count() >= 1:
                raise Exception('Existe um produto cadastrado com este mesmo codigo![62]')

            model_product = Product(
                name=self.name,
                description=self.description,
                code=self.code,
                compound=self.compound,
                unit_weight=self.unit_weight,
                weight=self.weight,
                width=self.width,
                length=self.length,
                height=self.height,
                origin=self.origin,
                gtin=self.gtin,
                published=False,)

            model_product.save()

        except Exception as error:
            raise error

        return model_product

    def update(self,request,model_login,**kwargs):
        self.product_id = None
        self.name = None
        self.description = None
        self.code = None
        self.compound = None
        self.unit_weight = None
        self.weight = None
        self.width = None
        self.length = None
        self.height = None
        self.origin = None
        self.gtin = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.compound = None if self.compound == '' else self.compound
        self.weight = None if self.weight == '' else self.weight
        self.width = None if self.width == '' else self.width
        self.length = None if self.length == '' else self.length
        self.height = None if self.height == '' else self.height
        self.gtin = None if self.gtin == '' else self.gtin

        if self.unit_weight and self.unit_weight not in dict(Product.UNIT_WEIGHT_LIST).keys():
            raise Exception('Unidade de medita recusada!')

        if self.origin and self.origin not in dict(Product.ORIGIN_LIST).keys():
            raise Exception('Origen recusada!')

        try:
            product_code_equal = Product.objects.filter(code=self.code,published=True)

            if product_code_equal.count() >= 1:
                raise Exception('Produto com mesmo codigo publicado!')

            try:
                model_product = Product.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            if model_product.published == True:
                raise Exception('Não é possível editar um produto publicado!')

            if self.name:
                model_product.name = self.name

            if self.description:
                model_product.description = self.description

            if self.code:
                model_product.code = self.code

            if self.compound:
                model_product.compound = self.compound

            if self.unit_weight:
                model_product.unit_weight = self.unit_weight

            if self.weight:
                model_product.weight = self.weight

            if self.width:
                model_product.width = self.width

            if self.length:
                model_product.length = self.length

            if self.height:
                model_product.height = self.height

            if self.origin:
                model_product.origin = self.origin

            if self.gtin:
                model_product.gtin = self.gtin

            model_product.save()

        except Exception as error:
            raise error

        return model_product

    def delete(self,request,model_login,**kwargs):
        self.product_id = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id:
            raise Exception('ID de produto não encontrado!')

        try:
            try:
                model_product = Product.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            if model_product.published == True:
                raise Exception('Não é possível remover um produto publicado!')

            model_product.delete()

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                description='Erro na remoção de produto',
                message=error,
                trace=traceback.format_exc())

            raise Exception('Não foi possível remover produto!')

        return model_product

    def published(self,request,model_login,**kwargs):
        self.product_id = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id:
            raise Exception('ID de produto não encontrado!')

        try:
            try:
                model_product = Product.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            if model_product.published == True:
                raise Exception('Produto já está publicado!')

            model_product.published = True
            model_product.save()

        except Exception as error:
            BusinessExceptionLog(request,model_login,
                description='Erro na publicação de produto',
                message=error,
                trace=traceback.format_exc())

            raise Exception('Não foi possível publicar produto!')

        return model_product

class Product(models.Model):
    UNIT_WEIGHT_LIST = (
        (1, 'kg (Kilograma)'),
        (2, 'L (Litros)'),
        (3, 'Kb (Kilobytes)'))

    ORIGIN_LIST = (
        (1, 'Própria'),
        (2, 'Terceirizado'),
        (3, 'Importado'),)

    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    code = models.CharField(max_length=150)
    compound = models.NullBooleanField()
    unit_weight = models.IntegerField(choices=UNIT_WEIGHT_LIST)
    weight = models.FloatField(null=True)
    width = models.FloatField(null=True)
    length = models.FloatField(null=True)
    height = models.FloatField(null=True)
    origin = models.IntegerField(choices=ORIGIN_LIST)
    gtin = models.CharField(max_length=150,null=True)
    published = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        db_table = 'product'
        ordering = ['-product_id']
        app_label = 'api'

