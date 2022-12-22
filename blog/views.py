from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from store.models import Product, Cart, Order

User = get_user_model()
# Create your views here.

def index(request):
    products = Product.objects.all()

    return render(request, "blog/index.html", context={"products":products})



def article(request, numero_article):
    print(numero_article)
    if numero_article in["01", "02", "03"]:
        return render(request, f"blog/article_{numero_article}.html")
    return render(request, "blog/article_not_found.html")

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'blog/detail.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'blog/cart.html', context={"orders": cart.orders.all()})

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')

def CGV(request):
    return render(request, 'blog/CGV.html')
