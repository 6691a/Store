from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem

def add(request):

    cart = Cart(request)
    if request.method == 'POST':
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        total_price = cart.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            return JsonResponse({'error':'Order already exists'}, status= 400)
        else:
            order = Order.objects.create(
                user_id = user_id, 
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'), 
                phone_number = request.POST.get('phone_number'),
                address= request.POST.get('address'),
                state_province_region=request.POST.get('state_province_region'),
                zip_code=request.POST.get('zip_code'),
                city=request.POST.get('city'),
                total_price=total_price, 
                order_key=order_key)
            order_id = order.pk

            for item in cart:
                #product = get_object_or_404(Product, title=item['product'])
                # if product.quantity < item['quantity']:
                #     return JsonResponse({'error': 'quantity error'}, status = 400)
                # product.quantity -= item['quantity']
                OrderItem.objects.create(order_id = order_id,  product=item['product'], price=item['price'], quantity=item['quantity'])


        return JsonResponse({'success': 'Return something'})


    



