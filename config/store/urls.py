from django.urls import path
from .views import *

#namespace
app_name = 'store'
urlpatterns = [
    path('<str:slug>/', product_in_category, name ='product_in_category'),
    path('<int:id>/<str:slug>/', product_detail, name ='product_detail'),
    path('', product_in_category, name ='product_all'),
    
]