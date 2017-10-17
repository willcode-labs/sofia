from django.conf.urls import url
from api.Controller import Login as ControllerLogin
from api.Controller import Person as ControllerPerson
from api.Controller import Product as ControllerProduct
# from web.Controller import Home as ControllerHome

# app api route
# login
urlpatterns = [
    url(r'^api/v1/login/verify/$', ControllerLogin.verify, name='api_v1_login_verify'),
    url(r'^api/v1/login/auth/$', ControllerLogin.auth, name='api_v1_login_auth'),
]
# person
urlpatterns += [
    url(r'^api/v1/person/filter/$', ControllerPerson.filter, name='api_v1_person_filter'),
    url(r'^api/v1/person/$', ControllerPerson.getById, name='api_v1_person_getbyid'),
    url(r'^api/v1/person/add/$', ControllerPerson.add, name='api_v1_person_add'),
    url(r'^api/v1/person/address/([0-9]+)/$', ControllerPerson.addressById, name='api_v1_person_address_by_id'),
    url(r'^api/v1/person/address/filter', ControllerPerson.addressFilter, name='api_v1_person_address_filter'),
    url(r'^api/v1/person/address/add/$', ControllerPerson.addressAdd, name='api_v1_person_address_add'),
    url(r'^api/v1/person/address/([0-9]+)/update/$', ControllerPerson.addressUpdate, name='api_v1_person_address_update'),
    url(r'^api/v1/person/address/([0-9]+)/delete/$', ControllerPerson.addressDelete, name='api_v1_person_address_delete'),
]
# product
urlpatterns += [
#     url(r'^api/v1/product/filter', ControllerProduct.filter, name='api_v1_product_filter'),
#     url(r'^api/v1/product/[0-9]{11}', ControllerProduct.getById, name='api_v1_product_getbyid'),
    url(r'^api/v1/product/add/$', ControllerProduct.add, name='api_v1_product_add'),
    # url(r'^api/v1/product/([0-9]+)/update/$', ControllerProduct.update, name='api_v1_product_update'),
#     url(r'^api/v1/product/[0-9]{11}/delete', ControllerProduct.delete, name='api_v1_product_delete'),
#     url(r'^api/v1/product/[0-9]{11}/published', ControllerProduct.published, name='api_v1_product_published'),
]
# order
# urlpatterns += [
#     url(r'^api/v1/order/filter', ControllerOrder.filter, name='api_v1_order_filter'),
#     url(r'^api/v1/order/person/[0-9]{11}/filter', ControllerOrder.personFilter, name='api_v1_order_person_filter'),
#     url(r'^api/v1/order/[0-9]{11}', ControllerOrder.getById, name='api_v1_order_getById'),
#     url(r'^api/v1/order/add', ControllerOrder.add, name='api_v1_order_add'),
#     url(r'^api/v1/order/[0-9]{11}/update', ControllerOrder.update, name='api_v1_order_update'),
#     url(r'^api/v1/order/[0-9]{11}/delete', ControllerOrder.delete, name='api_v1_order_delete'),
# ]

# app web route
# urlpatterns += [
#     url(r'^home/', ControllerHome.home, name='web_home_home'),
# ]
