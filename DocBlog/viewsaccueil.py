from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse
from store.models import Product, Cart, Order

User = get_user_model()

def abonnement(request):
    products = Product.objects.all

    return render(request, 'blog/index.html', context={"products": products})

def index(request):
    return render(request, "DocBlog/index.html", context={"date": datetime.today()})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'blog/detail.html', context={"product": product})

def article(request, numero_article):
    if numero_article in["01", "02", "03"]:
        return render(request, f"blog/article_{numero_article}.html")
    return render(request, "blog/article_not_found.html")

def signup(request):
    if request.method == "POST":
        # Traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)

        login(request, user)
        return redirect('index')

    return render(request, 'accounts/signup.html')

def login_user(request):
    if request.method == "POST":
        #connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')

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

    return redirect(reverse("product", kwargs={"slug": slug}))  #


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})


def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')



