import stripe
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from pprint import pprint

from DocBlog import settings
from accounts.models import Shopper
from store.models import Product, Cart, Order
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_API_KEY


def index(request):
    products = Product.objects.all()
    return render(request, 'blog/index.html', context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})


def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(
        request, 'store/cart.html', context={"orders": cart.orders.all()}
    )


def create_checkout_session(request):
    cart = request.user.cart

    line_items = [
        {"price": order.product.stripe_id, "quantity": order.quantity}
        for order in cart.orders.all()
    ]

    session = stripe.checkout.Session.create(
        locale="fr",
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('checkout-success')),
        cancel_url='http://127.0.0.1:8000',
    )

    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, 'store/success.html')


def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = "whsec_6f842c271ecaf1e27ecfcd47b106c3e60530c47cab87dab75312537f44fbdf35"
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(statuzs=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
    if event['type'] == 'checkout.session.completed':
        data = event['data']['object']
        return complete_order(data)

    # Passed signature verification
    return HttpResponse(status=200)


def complete_order(data):
    try:
        user_email = data['customer_details']['email']
    except KeyError:
        return HttpResponse("Invalid user email", status=404)

    user = get_object_or_404(Shopper, email=user_email)
    user.cart.ordered = True
    user.cart.ordered_date = timezone.now()
    for order in user.cart.orders.all():
    user.cart.save()

    return HttpResponse(status=200)
