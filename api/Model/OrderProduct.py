import uuid,traceback
from django.db import models
from api.Model.Order import Order as ModelOrder
from api.Model.Product import Product as ModelProduct

class OrderProductManager(models.Manager):
    def create(self,request,model_login,**kwargs):
        self.order_id = None
        self.product_id = None
        self.quantity = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.order_id or not self.product_id or not self.quantity:
            raise Exception('Dados insuficientes para adicionar produto ao pedido!')

        try:
            try:
                model_order = ModelOrder.objects.get(order_id=self.order_id)

            except Exception as error:
                raise Exception('Pedido não encontrado!')

            try:
                model_product = ModelProduct.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            model_order_product = OrderProduct(
                order=model_order,
                product=model_product,
                quantity=self.quantity)

        except Exception as error:
            raise Exception('Não foi possível criar relação entre pedido e produto!')

        return model_order_product

    def update(self,request,model_login,**kwargs):
        self.order_id = None
        self.product_id = None
        self.product_id_origin = None
        self.quantity = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.order_id or not self.product_id or not self.product_id_origin or not self.quantity:
            raise Exception('Dados insuficientes para atualizar relação entre produto e pedido!')

        if self.quantity <= 0:
            raise Exception('Quantidade não pode ser menor que zero!')

        if self.product_id == self.product_id_origin:
            raise Exception('Os produtos são iguais, atualização cancelada!')

        try:
            try:
                model_order = ModelOrder.objects.get(order_id=self.order_id)

            except Exception as error:
                raise Exception('Pedido não encontrado!')

            try:
                model_product = ModelProduct.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            try:
                model_product_origin = ModelProduct.objects.get(product_id=self.product_id_origin)

            except Exception as error:
                raise Exception('Produto de origem não encontrado!')

            model_order_product_conflict = OrderProduct.objects.filter(
                order=model_order,
                product=model_product)

            if model_order_product_conflict.count() >= 1:
                raise Exception('Pedido já contem este produto!')

            try:
                model_order_product = OrderProduct.objects.get(
                    order=model_order,
                    product=model_product_origin)

            except Exception as error:
                raise Exception('Vinculo entre pedido e produto não encontrado!')

            try:
                model_order_product.product = model_product
                model_order_product.quantity = self.quantity
                model_order_product.save()

            except Exception as error:
                raise Exception('Não foi possível efetuar a troca de produto para este pedido!')

        except Exception as error:
            raise Exception('Não foi possível atualizar relação entre pedido e produto!')

        return model_order_product

    def delete(self,request,**kwargs):
        self.order_id = None
        self.product_id = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.order_id or not self.product_id:
            raise Exception('Dados insuficientes para remover produto do pedido!')

        try:
            try:
                model_order = ModelOrder.objects.get(order_id=self.order_id)

            except Exception as error:
                raise Exception('Pedido não encontrado!')

            try:
                model_product = ModelOrder.objects.get(product_id=self.product_id)

            except Exception as error:
                raise Exception('Produto não encontrado!')

            try:
                model_order_product = OrderProduct.objects.get(
                    order=model_order,
                    product=model_product,)

            except Exception as error:
                raise Exception('Relação entre pedido e produto não encontrada!')

            model_order_product.delete()

        except Exception as error:
            raise Exception('Não foi possível remover relação entre pedido e produto!')

        return True

class OrderProduct(models.Model):
    order = models.ForeignKey(ModelOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(ModelProduct,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_product'
        app_label = 'api'
        unique_together = ((order, product),)

    objects = OrderProductManager()
