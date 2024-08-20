from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from seller_app.models import Product
from .models import Order, OrderItem
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY





@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}

    request.session['cart'] = cart
    return redirect('buyer_app:cart')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []

    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)]['quantity'],
            'total_price': product.price * cart[str(product.id)]['quantity']
        })

    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('buyer_app:cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total_price = sum(product.price * cart[str(product.id)]['quantity'] for product in products)

    if request.method == 'POST':
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency='usd',
            automatic_payment_methods={'enabled': True},
        )

        order = Order.objects.create(user=request.user, total_price=total_price)
        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart[str(product.id)]['quantity'],
                price=product.price
            )

        order.stripe_payment_id = intent['id']
        order.save()

        request.session['cart'] = {}

        return render(request, 'checkout_success.html', {'order': order})

    return render(request, 'checkout.html', {'total_price': total_price})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})



def checkout_success(request):
    return render(request, 'buyer/checkout_success.html')
