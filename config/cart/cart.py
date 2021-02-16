from store.models import Product
from decimal import Decimal

class Cart():
    CART_SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(self.CART_SESSION_KEY)

        if 'cart' not in request.session:
            cart = self.session[self.CART_SESSION_KEY] = {}
        self.cart = cart

    # my_car 미존재 시 KeyError 발생
    # my_car = request.session['my_car']


    def save(self):
        self.session[self.CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1 ,is_update = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':int(quantity), 'price':str(product.price)}
        
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            print(self.cart[product_id])
            del(self.cart[product_id])
            self.save()