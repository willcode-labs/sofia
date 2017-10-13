import uuid,traceback,datetime
from django.db import models
from api.apps import ApiConfig
from api.Business.ExceptionLog import ExceptionLog as BusinessExceptionLog
from api.Model.Product import Product as ModelProduct
from api.Model.Person import Person as ModelUser
from api.Model.Address import Address as ModelAddress
from api.Model.OrderProduct import OrderProduct as ModelOrderProduct

class OrderManager(models.Manager):
    def create(self,request,**kwargs):
        self.product_id_list = None
        self.product_quantity_list = None
        self.user = None
        self.ticket = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.user or not self.product_id_list or not self.product_quantity_list:
            raise Exception('Dados insuficientes para criação de pedido!')

        if not isinstance(self.user, ModelUser):
            raise Exception('Um usuário é necessário para criação de pedido!')

        if self.product_id_list.count() != self.product_quantity_list.count():
            raise Exception('Dados inconsistentes para criação de pedido!')

        for product_quantity in self.product_quantity_list:
            if product_quantity <= 0:
                raise Exception('Quantidade não pode ser zero!')

        try:
            model_product_with_quantity_list = []

            for index,product_id in enumerate(self.product_id_list):
                try:
                    model_product = ModelProduct.objects.get(product_id=product_id)

                    model_product_with_quantity_list.append({
                        'quantity': self.product_quantity_list[index],
                        'model_product': model_product
                    })

                except Exception as error:
                    raise Exception('Produto não encontrado(%s)!' % (product_id,))

            try:
                date_expired = datetime.datetime.now() + datetime.timedelta(hours=ApiConfig.order_expired_in_hour)

                model_order = Order(
                    user=user,
                    address=None,
                    status=Order.STATUS_OPEN,
                    ticket=self.ticket,
                    date_expired=date_expired,)

                model_order.save()

            except Exception as error:
                raise Exception('Não foi possivel criar pedido!')

            model_order_product_list = []

            for model_product_with_quantity in model_product_with_quantity_list:
                model_order_product = ModelOrderProduct.objects.create(
                    order=model_order,
                    product=model_product_with_quantity['model_product'],
                    quantity=model_product_with_quantity['quantity'])

                model_order_product_list.append(model_order_product)

        except Exception as error:
            BusinessExceptionLog(request,
                description='Erro na criação de pedido',
                message=error,
                trace=traceback.format_exc())

            raise Exception('Não foi possível criar pedido!')

        model_order.product = model_order_product_list

        return model_order

    def update(self,request,**kwargs):
        self.order_id = None
        self.product_id_list = None
        self.product_quantity_list = None
        self.ticket = None

        for key in kwargs:
            setattr(self,key,kwargs[key])

        if not self.product_id_list or not self.product_quantity_list:
            raise Exception('Dados insuficientes para criação de pedido!')

        if self.product_id_list.count() != self.product_quantity_list.count():
            raise Exception('Dados inconsistentes para criação de pedido!')

        for product_quantity in self.product_quantity_list:
            if product_quantity <= 0:
                raise Exception('Quantidade não pode ser zero!')

        try:
            model_product_with_quantity_list = []

            for index,product_id in enumerate(self.product_id_list):
                try:
                    model_product = ModelProduct.objects.get(product_id=product_id)

                    model_product_with_quantity_list.append({
                        'quantity': self.product_quantity_list[index],
                        'model_product': model_product
                    })

                except Exception as error:
                    raise Exception('Produto não encontrado(%s)!' % (product_id,))

            try:
                date_expired = datetime.datetime.now() + datetime.timedelta(hours=ApiConfig.order_expired_in_hour)

                model_order = Order(
                    user=user,
                    address=None,
                    status=Order.STATUS_OPEN,
                    ticket=self.ticket,
                    date_expired=date_expired,)

                model_order.save()

            except Exception as error:
                raise Exception('Não foi possivel criar pedido!')

            model_order_product_list = []

            for model_product_with_quantity in model_product_with_quantity_list:
                model_order_product = ModelOrderProduct.objects.create(
                    order=model_order,
                    product=model_product_with_quantity['model_product'],
                    quantity=model_product_with_quantity['quantity'])

                model_order_product_list.append(model_order_product)

        except Exception as error:
            BusinessExceptionLog(request,
                description='Erro na criação de pedido',
                message=error,
                trace=traceback.format_exc())

            raise Exception('Não foi possível criar pedido!')

        model_order.product = model_order_product_list

        return model_order

class Order(models.Model):
    STATUS_OPEN = 1
    STATUS_CANCELED  = 2
    STATUS_AWAITING_PAYMENT = 3
    STATUS_PAYMENT_ACCEPT = 4
    STATUS_PAYMENT_OK = 5
    STATUS_DISPATCHED = 6
    STATUS_DELIVERED = 7
    STATUS_REVERSED = 8
    STATUS_RETURNED = 9

    STATUS_LIST = (
        (STATUS_OPEN, 'Aberto'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_AWAITING_PAYMENT, 'Aguardando pagamento'),
        (STATUS_PAYMENT_ACCEPT, 'Pagamento recusado'),
        (STATUS_PAYMENT_OK, 'Pago'),
        (STATUS_DISPATCHED, 'Despachado'),
        (STATUS_DELIVERED, 'Entregue'),
        (STATUS_REVERSED, 'Estornado')
        (STATUS_RETURNED, 'Devolvido'))

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(ModelUser)
    address_id = models.ForeignKey(ModelAddress)
    status = models.IntegerField(choices=STATUS_LIST)
    ticket = models.CharField(max_length=30)
    date_expired = models.DateTimeField()
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
        app_label = 'api'

    objects = OrderManager()
