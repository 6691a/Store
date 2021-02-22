from django.shortcuts import render, get_object_or_404
from .models import *

def product_in_category(request, slug=None):

    #쿼리를 여러번 실행해도 출력,필요 시 한번만 호출
    #전달 시 필요한 쿼리만 호출
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(display=True)

    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=current_category)
    return render(
        request, 
        'store/list.html', 
        {
            'current_category': current_category,
            'categories':categories,
            'products':products
        }
    )


def product_detail(request, id, slug=None):
    product = get_object_or_404(Product,id =id, slug=slug)
    
    print(product.quantity)
    return render(request, 'store/detail.html', 
        {
            'product': product,
            'range':range(1, product.quantity + 1)
        }
    )
