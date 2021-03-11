from django.db import models
from django.conf import settings
from store.models import Product
from .iamport import payments_prepare, find_transaction, order_cancel
import hashlib
from django.urls import reverse
from django.db.models.signals import post_save

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='imporder_user')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #결제 여부
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        db_table = 'impOrder'

    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product 
    
        # 상세페이지 
    def get_absolute_url(self):
        return reverse('imp_order:order_detail', args=[self.id])

        


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_product',on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'impOrderItem'

    def get_item_price(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.id)





class OrderTransactionManager(models.Manager):

    def create_new(self, order, amount, type, success=None, transaction_status=None):
        if not order:
            raise ValueError("Order is None")
        
        #email + order_Id -> 주문번호 생성
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email = str(order.email).split('@')[0]
        order_id = hashlib.sha1((order_hash  + email).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = str(order_id)

        #iamport 결제 준비
        payments_prepare(merchant_order_id, amount)

        tranasction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount,
            type=type
        )

        if success is not None:
            tranasction.success = success
            tranasction.transaction_status = transaction_status
        
        try:
            tranasction.save()
        except Exception as e:
            print("Tranasction error",e)

        return tranasction.merchant_order_id

    def get_transaction(self,merchant_order_id):
        if merchant_order_id:
            result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None


    class Meta:
        db_table = 'impOrderTransactionManager'


class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='trans')
    merchant_order_id = models.CharField(max_length=25, null=True, blank=True)
    #iamport의 PK값 
    transaction_id = models.CharField(max_length=120, null=True,blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True,blank=True)
    type = models.CharField(max_length=120,blank=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)

    objects = OrderTransactionManager()
    
    def __str__(self):
        return str(self.order)

    class Meta:
        ordering = ['-created']
        db_table = 'impOrderTransaction'


def order_payment_validation(sender, instance, created, *args, **kwargs):
    #OrderTransaction instance 들어옴
    if instance.transaction_id:
        iamport_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)
        if iamport_transaction:
            merchant_order_id = iamport_transaction['merchant_order_id']
            imp_id = iamport_transaction['imp_id']
            amount = iamport_transaction['amount']

            local_transaction = OrderTransaction.objects.filter(
                merchant_order_id = merchant_order_id, 
                transaction_id = imp_id,
                amount = amount,
                ).exists()

            if not iamport_transaction or not local_transaction:
                raise ValueError("PAYMENT ERROR")



post_save.connect(order_payment_validation,sender=OrderTransaction)


# class OrderCancelManager(models.Manager):
#     def create_new(self, user, order, amount, reason, cancel_amount):
#         if not order and not user:
#             raise ValueError("Order / User is None")
#         merchant_order_id = order.merchant_order_id
#         #결제 취소

#         order_cancel(merchant_order_id, reason, amount)
#         cancel = self.model(
#             user = self.user,
#             order = order,
#             reason = reason,
#             cancel_amount = amount
#         )

#         try:
#             cancel.save()
#         except Exception as e:
#             print("Cancel error", e)

# def order_cancel_validation(sender, instance, created, *args, **kwargs):
#     pass



class OrderCancel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cancel_user')
    order = models.ForeignKey(Order, related_name='cancel_items', on_delete=models.CASCADE)
    #환불 성공 여부
    canceled  = models.BooleanField(default=False)
    #환불 사유
    reason = models.CharField(max_length=255)
    #환불 요청 금액
    cancel_amount = models.DecimalField(max_digits=10, decimal_places=2)
    #환불된 금액
    canceled_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        db_table = 'impOrderCencel'