from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.generic.base import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

#
from .iamport import *
# pdf를 위한 임포트
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint


@login_required
@csrf_exempt
#JS가 동작하지 않을때
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])


            cart.clear()
            return render(request, 'order_created.html', {'order':order})
    
    return render(request, 'order_form.html', {'cart':cart})

@login_required
# ajax로 결제 후에 보여줄 결제 완료 화면
def order_complete(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request,'order_created.html',{'order':order})


class OrderCreateAjaxView(View):
    @csrf_exempt
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        cart = Cart(request)

     
        order = Order.objects.create(
            user = request.user,
            first_name= request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            zip_code=request.POST.get('zip_code'),
            phone_number=request.POST.get('phone_number')
        )

        if order:
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

            cart.clear()

            data = {
                "order_id": order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


# 결제 정보 생성
class OrderCheckoutAjaxView(View):
    @csrf_exempt
    def post(self, request):
        
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount,
                type = ''
            )
        except Exception as e:
            print(e)
            merchant_order_id = None

        
        if merchant_order_id is not None:
            data = {
                "success": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            data = {
                "success": False,
                "error": 'merchant_order_id is None'
            }
            return JsonResponse(data, status=401)



# 실제 결제가 이뤄진 것이 있는지 확인
class OrderImpAjaxView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None


        if trans is not None:
            trans.transaction_id = imp_id
            trans.save()

            order.paid = True
            order.save()

        
            data = {
                "success": True
            }
            return JsonResponse(data)
        else:
            data = {
                "success": False,
                "error": 'OrderTransaction is None'
            }
            return JsonResponse(data, status=401)


class OrderCancelView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        
        order = request.POST.get('order_id')
        tran = get_object_or_404(OrderTransaction,order = order)
        merchant_order_id = tran.merchant_order_id
        amount = tran.amount
        reason = request.POST.get('reason')


        tran.transaction_status
        impcancel = order_cancel(merchant_order_id, reason, amount)
 
        try:
            cancel = OrderCancel.objects.create(
                user = request.user,
                order_id= order,
                reason = reason,
                cancel_amount = amount
            )
        except:
            cancel = None

        if impcancel['code'] == 0:
            tran.transaction_status = "환불 완료"
            tran.save()
            cancel.canceled = True
            canceled_amount = impcancel['response']['amount']
            cancel.save()
            data = {
                "success": True,
                "msg": "정상 환불 되었습니다."
            }
            return JsonResponse(data, status=200)
        else:
            data = {
                "success": False,
                "msg": impcancel['message']
            }
            return JsonResponse(data, status=401)
@login_required
def OrderDetail(request, order_id):
    return render(request, 'order_detail.html', {'order':find_order(request, order_id)})


#관리자만 접속가능
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/detail.html', {'order':order})



# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('admin/pdf.html', {'order':order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.user}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
#     return response

def find_order(request, order_id):
    user = request.user.id
    order = Order.objects.get(user = user, pk=order_id)
    return order

def user_orders(request):
    user = request.user.id
    orders = Order.objects.filter(user=user)
    return orders




