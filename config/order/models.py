from django.db import models
from decimal import Decimal
# from django.conf import settings
from user.models import User
from store.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('PAYMENT_PROGRESS', '결제 진행'),
        ('PAYMENT_COMPLETION', '결제 완료'),
        ('PAYMENT_ERROR', '결제 오류'),
        ('PAYMENT_ FAILED', '결제 실패'),
        ('PREPARE','배송 준비'),
        ('SHIPPING','배송 중'), 
        ('SHIPPED','배송 완료'),   
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state_province_region = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    class Meta:
        ordering = ['-created',]
    
    def __str__(self):
        return str(self.created)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)