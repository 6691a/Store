
from django.urls import path

from .views import *

app_name = 'payment'
urlpatterns = [
    path('info/', payment, name='payment_info'),

]