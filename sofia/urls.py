from django.urls import path
from django.conf.urls import handler400,handler403,handler404,handler500
from api.Controller.v1 import Auth as v1ControllerAuth
from api.Controller.v1 import Person as v1ControllerPerson
from api.Controller.v1 import PersonAddress as v1ControllerPersonAddress
from api.Controller.v1 import Product as v1ControllerProduct
from api.Controller.v1 import Delivery as v1ControllerDelivery
from api.Controller.v1 import Order as v1ControllerOrder
# app api route
# login
urlpatterns = [
    path('api/v1/client/auth/verify/',v1ControllerAuth.VerifyClient.as_view(),name='api_v1_client_auth_verify'),
    path('api/v1/auth/login/',v1ControllerAuth.Auth.as_view(),name='api_v1_auth_login'),
]
# person
urlpatterns += [
    path('api/v1/client/person/',v1ControllerPerson.EndPointClient.as_view(),name='api_v1_client_person_endpoint'),
    path('api/v1/director/person/',v1ControllerPerson.EndPointDirector.as_view(),name='api_v1_director_person_endpoint'),
]
# # person address
# urlpatterns += [
#     path('api/v1/person-address/', v1ControllerPersonAddress.EndPoint.as_view(), name='api_v1_person_address_endpoint'),
# ]
# # product
# urlpatterns += [
#     path('api/v1/product/', v1ControllerProduct.EndPoint.as_view(), name='api_v1_product_endpoint'),
#     path('api/v1/product/published/', v1ControllerProduct.Publish.as_view(), name='api_v1_product_publish'),
# ]
# # delivery package
# urlpatterns += [
#     path('api/v1/delivery-package/', v1ControllerDeliveryPackage.EndPoint.as_view(), name='api_v1_delivery_package_endpoint'),
# ]
# # delivery
# urlpatterns += [
#     path('api/v1/delivery/', v1ControllerDelivery.EndPoint.as_view(), name='api_v1_delivery_endpoint'),
#     path('api/v1/delivery/price/', v1ControllerDelivery.Price.as_view(), name='api_v1_delivery_price'),
# ]
# # order
# urlpatterns += [
#     path('api/v1/order/', v1ControllerOrder.EndPoint.as_view(), name='api_v1_order_endpoint'),
# ]
# error handler
handler400 = 'api.Controller.v1.HandlerError.bad_request'
handler403 = 'api.Controller.v1.HandlerError.permission_denied'
handler404 = 'api.Controller.v1.HandlerError.page_not_found'
handler500 = 'api.Controller.v1.HandlerError.server_error'
