from django.conf.urls import url
from api.Controller.v1 import Login as v1ControllerLogin
from api.Controller.v1 import Person as v1ControllerPerson
from api.Controller.v1 import Product as v1ControllerProduct
# from web.Controller import Home as ControllerHome

# app api route
# login
urlpatterns = [
    url(r'^api/v1/login/verify/?$', v1ControllerLogin.verify, name='api_v1_login_verify'),
    url(r'^api/v1/login/auth/?$', v1ControllerLogin.auth, name='api_v1_login_auth'),
]
# person
urlpatterns += [
    url(r'^api/v1/person/filter/?$', v1ControllerPerson.filter, name='api_v1_person_filter'),
    url(r'^api/v1/person/([0-9]+)/?$', v1ControllerPerson.getById, name='api_v1_person_getbyid'),
    url(r'^api/v1/person/add/?$', v1ControllerPerson.add, name='api_v1_person_add'),
    url(r'^api/v1/person/address/filter', v1ControllerPerson.addressFilter, name='api_v1_person_address_filter'),
    url(r'^api/v1/person/address/([0-9]+)/?$', v1ControllerPerson.addressById, name='api_v1_person_address_by_id'),
    url(r'^api/v1/person/address/add/([0-9]+)/?$', v1ControllerPerson.addressAdd, name='api_v1_person_address_add'),
    url(r'^api/v1/person/address/([0-9]+)/update/?$', v1ControllerPerson.addressUpdate, name='api_v1_person_address_update'),
    url(r'^api/v1/person/address/([0-9]+)/delete/?$', v1ControllerPerson.addressDelete, name='api_v1_person_address_delete'),
]
# product
urlpatterns += [
#     url(r'^api/v1/product/filter', v1ControllerProduct.filter, name='api_v1_product_filter'),
#     url(r'^api/v1/product/[0-9]{11}', v1ControllerProduct.getById, name='api_v1_product_getbyid'),
    url(r'^api/v1/product/add/?$', v1ControllerProduct.add, name='api_v1_product_add'),
    # url(r'^api/v1/product/([0-9]+)/update/?$', v1ControllerProduct.update, name='api_v1_product_update'),
#     url(r'^api/v1/product/[0-9]{11}/delete', v1ControllerProduct.delete, name='api_v1_product_delete'),
#     url(r'^api/v1/product/[0-9]{11}/published', v1ControllerProduct.published, name='api_v1_product_published'),
]
# order
# urlpatterns += [
#     url(r'^api/v1/order/filter', v1ControllerOrder.filter, name='api_v1_order_filter'),
#     url(r'^api/v1/order/person/[0-9]{11}/filter', v1ControllerOrder.personFilter, name='api_v1_order_person_filter'),
#     url(r'^api/v1/order/[0-9]{11}', v1ControllerOrder.getById, name='api_v1_order_getById'),
#     url(r'^api/v1/order/add', v1ControllerOrder.add, name='api_v1_order_add'),
#     url(r'^api/v1/order/[0-9]{11}/update', v1ControllerOrder.update, name='api_v1_order_update'),
#     url(r'^api/v1/order/[0-9]{11}/delete', v1ControllerOrder.delete, name='api_v1_order_delete'),
# ]
