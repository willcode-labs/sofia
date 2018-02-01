# from django.conf.urls import url
from django.urls import path
from api.Controller.v1 import Login as v1ControllerLogin
from api.Controller.v1 import Person as v1ControllerPerson
from api.Controller.v1 import PersonAddress as v1ControllerPersonAddress
from api.Controller.v1 import Product as v1ControllerProduct
from api.Controller.v1 import Delivery as v1ControllerDelivery
from api.Controller.v1 import Order as v1ControllerOrder
# from web.Controller import Home as ControllerHome

# app api route
# login
urlpatterns = [
    path('api/v1/login/verify/', v1ControllerLogin.Verify.as_view(), name='api_v1_login_verify'),
    path('api/v1/login/auth/', v1ControllerLogin.Auth.as_view(), name='api_v1_login_auth'),
]
# person
urlpatterns += [
    path('api/v1/person/', v1ControllerPerson.EndPoint.as_view(), name='api_v1_person_endpoint'),
]
# person address
urlpatterns += [
    path('api/v1/person-address/', v1ControllerPersonAddress.EndPoint.as_view(), name='api_v1_person_address_endpoint'),
]
# product
urlpatterns += [
    path('api/v1/product/', v1ControllerProduct.EndPoint.as_view(), name='api_v1_product_endpoint'),
    path('api/v1/product/published/', v1ControllerProduct.Publish.as_view(), name='api_v1_product_publish'),
]
# delivery
urlpatterns += [
    path('api/v1/delivery/', v1ControllerDelivery.EndPoint.as_view(), name='api_v1_delivery_endpoint'),
    path('api/v1/delivery/price/', v1ControllerDelivery.Price.as_view(), name='api_v1_delivery_price'),
]
# delivery package
urlpatterns += [
    path('api/v1/delivery-package/', v1ControllerDeliveryPackage.EndPoint.as_view(), name='api_v1_delivery_package_endpoint'),
]
# order
urlpatterns += [
    path('api/v1/order/', v1ControllerOrder.EndPoint.as_view(), name='api_v1_order_endpoint'),
]
