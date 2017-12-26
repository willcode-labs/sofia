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
        self.quantity = request.POST.get('quantity',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.name or not self.description or not self.code or not self.unit_weight or not self.origin or not self.quantity:
            raise Exception('Dados insuficientes para criação de produto![58]')

        self.compound = None if self.compound == '' else self.compound
        self.weight = None if self.weight == '' else self.weight
        self.width = None if self.width == '' else self.width
        self.length = None if self.length == '' else self.length
        self.height = None if self.height == '' else self.height
        self.gtin = None if self.gtin == '' else self.gtin

        if self.compound and not self.compound in ('0','1'):
            raise Exception('Valor do parâmetro composto incorreto![63]')

        self.compound = False if self.compound == '0' else self.compound
        self.compound = True if self.compound == '1' else self.compound

        if self.weight and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.weight)):
            raise Exception('Valor do parâmetro peso incorreto![64]')

        self.weight = float(self.weight) if self.weight else self.weight

        if self.width and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.width)):
            raise Exception('Valor do parâmetro largura incorreto![65]')

        self.width = float(self.width) if self.width else self.width

        if self.length and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.length)):
            raise Exception('Valor do parâmetro comprimento incorreto![66]')

        self.length = float(self.length) if self.length else self.length

        if self.height and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.height)):
            raise Exception('Valor do parâmetro altura incorreto![67]')

        self.height = float(self.height) if self.height else self.height

        if not self.unit_weight or not re.match(r'^[0-9]+$',str(self.unit_weight)) or int(self.unit_weight) not in dict(Product.UNIT_WEIGHT_LIST).keys():
            raise Exception('Unidade de medida recusada![59]')

        self.unit_weight = int(self.unit_weight)

        if not self.origin or not re.match(r'^[0-9]+$',str(self.origin)) or int(self.origin) not in dict(Product.ORIGIN_LIST).keys():
            raise Exception('Origen recusada![60]')

        self.origin = int(self.origin)

        if not re.match(r'^[0-9]+$',str(self.quantity)):
            raise Exception('Parametro quantidade incorreto![110]')

        self.quantity = int(self.quantity)

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
                quantity=self.quantity,
                published=False,)

            model_product.save()

        except Exception as error:
            raise error

        return model_product

    def update(self,request,model_login,**kwargs):
        self.product_id = request.PUT.get('product_id',None)
        self.name = request.PUT.get('name',None)
        self.description = request.PUT.get('description',None)
        self.code = request.PUT.get('code',None)
        self.compound = request.PUT.get('compound',None)
        self.unit_weight = request.PUT.get('unit_weight',None)
        self.weight = request.PUT.get('weight',None)
        self.width = request.PUT.get('width',None)
        self.length = request.PUT.get('length',None)
        self.height = request.PUT.get('height',None)
        self.origin = request.PUT.get('origin',None)
        self.gtin = request.PUT.get('gtin',None)
        self.quantity = request.PUT.get('quantity',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id:
            raise Exception('Dados insuficientes para edição de produto![89]')

        try:
            model_product = Product.objects.get(product_id=self.product_id)

        except Exception as error:
            raise Exception('Produto não encontrado![99]')

        if model_product.published == True:
            raise Exception('Não é possível editar um produto publicado![101]')

        if not self.name and not self.description and not self.code and not self.compound \
            and not self.unit_weight and not self.weight and not self.width and not self.length \
            and not self.height and not self.origin and not self.gtin and not self.quantity:
            raise Exception('Dados insuficientes para edição de produto![90]')

        self.compound = None if self.compound == '' else self.compound
        self.weight = None if self.weight == '' else self.weight
        self.width = None if self.width == '' else self.width
        self.length = None if self.length == '' else self.length
        self.height = None if self.height == '' else self.height
        self.gtin = None if self.gtin == '' else self.gtin

        if self.compound and not self.compound in ('0','1'):
            raise Exception('Valor do parâmetro composto incorreto![91]')

        self.compound = False if self.compound == '0' else self.compound
        self.compound = True if self.compound == '1' else self.compound

        if self.weight and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.weight)):
            raise Exception('Valor do parâmetro peso incorreto![92]')

        self.weight = float(self.weight) if self.weight else self.weight

        if self.width and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.width)):
            raise Exception('Valor do parâmetro largura incorreto![93]')

        self.width = float(self.width) if self.width else self.width

        if self.length and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.length)):
            raise Exception('Valor do parâmetro comprimento incorreto![94]')

        self.length = float(self.length) if self.length else self.length

        if self.height and not re.match(r'^[0-9]+([.]{1}[0-9]{1,2})?$',str(self.height)):
            raise Exception('Valor do parâmetro comprimento incorreto![95]')

        self.height = float(self.height) if self.height else self.height

        if not self.unit_weight or not re.match(r'^[0-9]+$',str(self.unit_weight)) or int(self.unit_weight) not in dict(Product.UNIT_WEIGHT_LIST).keys():
            raise Exception('Unidade de medida recusada![96]')

        self.unit_weight = int(self.unit_weight)

        if not self.origin or not re.match(r'^[0-9]+$',str(self.origin)) or int(self.origin) not in dict(Product.ORIGIN_LIST).keys():
            raise Exception('Origen recusada![97]')

        self.origin = int(self.origin)

        if not re.match(r'^[0-9]+$',str(self.quantity)):
            raise Exception('Parametro quantidade incorreto![111]')

        self.quantity = int(self.quantity)

        if model_login.profile_id not in (model_login.PROFILE_ROOT,model_login.PROFILE_DIRECTOR,):
            raise Exception('Relacionamento entre tipo de pessoas incorreto![98]')

        try:
            if self.code:
                product_code_equal_total = Product.objects.filter(code=self.code).exclude(product_id=model_product.product_id).count()

                if product_code_equal_total >= 1:
                    raise Exception('Existe um outro produto cadastrado com este mesmo código![100]')

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

            if self.quantity:
                model_product.quantity = self.quantity

            model_product.save()

        except Exception as error:
            raise error

        return model_product

    def delete(self,request,model_login,**kwargs):
        self.product_id = request.DELETE.get('product_id',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id:
            raise Exception('ID de produto não encontrado![102]')

        try:
            model_product = Product.objects.get(product_id=self.product_id)

        except Exception as error:
            raise Exception('Produto não encontrado![103]')

        try:
            if model_product.published == True:
                raise Exception('Não é possível remover um produto publicado![104]')

            model_product.delete()

        except Exception as error:
            raise error

        return True

    def publish(self,request,model_login,**kwargs):
        self.product_id = request.PUT.get('product_id',None)
        self.published = request.PUT.get('published',None)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id or not self.published:
            raise Exception('Parâmetros insuficientes para este operação![105]')

        if self.published not in ('0','1'):
            raise Exception('Valor de parâmetro incorreto![106]')

        self.published = False if self.published == '0' else self.published
        self.published = True if self.published == '1' else self.published

        try:
            model_product = Product.objects.get(product_id=self.product_id)

        except Exception as error:
            raise Exception('Produto não encontrado![107]')

        if model_product.published == self.published:
            if self.published == True:
                raise Exception('Produto ja está publicado![108]')

            else:
                raise Exception('Produto não se encontra com status publicado![109]')

        try:
            model_product.published = self.published
            model_product.save()

        except Exception as error:
            raise error

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
    quantity = models.IntegerField()
    published = models.BooleanField()
    date_create = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        db_table = 'product'
        ordering = ['-product_id']
        app_label = 'api'

