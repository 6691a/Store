from django.contrib import admin

from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_key', 'total_price','status']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price','quantity']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

