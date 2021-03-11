
from django.urls import path
from .views import *


app_name = 'imp_order'
urlpatterns = [
    path('create/', order_create, name='order_create'),

    path('complete/', order_complete,name='order_complete'),
    
    path('create_ajax/', OrderCreateAjaxView.as_view(),name='order_create_ajax'),
    path('checkout/', OrderCheckoutAjaxView.as_view(),name='order_checkout'),
    path('validation/', OrderImpAjaxView.as_view(),name='order_validation'),
    path('detail/<int:order_id>/', OrderDetail ,name='order_detail'),

    path('cancel/', OrderCancelView.as_view(),name='order_cancel'),


    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    # path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),
]