
from django.urls import path

from .views import *

app_name = 'payment'
urlpatterns = [
    # path('', views.BasketView, name='basket'),
    # path('orderplaced/', views.order_placed, name='order_placed'),
    # path('error/', views.Error.as_view(), name='error'),
    # path('webhook/', views.stripe_webhook),

    path('info/', Payment, name='payment_info'),

]