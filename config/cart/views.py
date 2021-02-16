from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .cart import Cart
from store.models import Product



@csrf_exempt
@require_POST
def cart_add(request, is_update=False):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product_quantity = int(request.POST.get('product_quantity'))


    product = get_object_or_404(Product , id=product_id)

    cart.add(product = product, quantity=product_quantity)

    cart_quantity = cart.__len__()

    response = JsonResponse({'cart_quantity': cart_quantity})
    return response

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart':cart})


@csrf_exempt
@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product_quantity = int(request.POST.get('product_quantity'))


    product = get_object_or_404(Product , id=product_id)
    cart.add(product = product, quantity=product_quantity, is_update=True)

    cart_quantity = cart.__len__()
    total_price = cart.get_total_price()

    response = JsonResponse({'cart_quantity': cart_quantity, 'get_total_price': total_price})
    return response

@csrf_exempt
@require_POST
def cart_delete(request):
    product_id = int(request.POST.get('product_id'))
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.delete(product)


    cart_quantity = cart.__len__()
    total_price = cart.get_total_price()


    response = JsonResponse({'cart_quantity': cart_quantity, 'get_total_price': total_price})
    return response





