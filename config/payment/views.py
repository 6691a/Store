import stripe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import config.__setting__ as setting

@login_required
def Payment(request):
    cart = Cart(request)
    #type: decimal.Decimal
    total_price = str(cart.get_total_price())
    total_price = total_price.replace('.', '')
    total_price = int(total_price)
    print(total_price)

    stripe.api_key = setting.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        # amount=total_price,
        amount= 50,
        currency='USD',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment.html', {'client_secret': intent.client_secret})