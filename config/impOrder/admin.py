from django.contrib import admin
from .models import *
from django.urls import reverse 
#TAG 사용을 가능하게 해줌  
from django.utils.safestring import mark_safe


#커스텀 필드는 OBJ를 받는다. 
def order_detail(obj):
    url = reverse('imp_order:admin_order_detail', args=[obj.id])
    html = mark_safe(f'<a href="{url}">Detail</a>')
    return html 
order_detail.short_description = 'Detail'


# def order_pdf(obj):
#     url = reverse('imp_order:admin_order_pdf', args=[obj.id])
#     html = mark_safe( f"<a href'{url}'>PDF </a>")
#     return 'html' 
# order_pdf.short_description = 'PDF'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class ImpOrderAdmin(admin.ModelAdmin):
    list_display = ['user','id',order_detail,'paid','first_name','last_name','email','address','zip_code','phone_number','created','updated']
    list_filter = ['paid','created','updated']
    # 다른 모델과 연결되어있는 경우 한페이지 표시하고 싶을 때
    inlines = [OrderItemInline]



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product','price','quantity']

class OrderTransactionAdmin(admin.ModelAdmin):
    list_display = ['order','amount','merchant_order_id','transaction_id']


admin.site.register(Order, ImpOrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderTransaction,OrderTransactionAdmin)
admin.site.register(OrderCancel)


