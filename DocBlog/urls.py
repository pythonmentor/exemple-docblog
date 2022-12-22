from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .viewsaccueil import index, abonnement, article, product_detail
from store.views import add_to_cart, cart, delete_cart, create_checkout_session, checkout_success, stripe_webhook
from accounts.views import signup, logout_user, login_user
from blog.views import CGV
from DocBlog import settings

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    # path('appelsdoffres/', include('blog.urls', namespace='blog')),
    path('abonnement/', abonnement, name="abonnement"),
    path('abonnement/article-<str:numero_article>/', article, name="blog-article"),
    path('CGV/', CGV, name="CGV"),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('cart/', cart, name="cart"),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/success', checkout_success, name="checkout-success"),
    path('cart/create-checkout-session', create_checkout_session, name="create-checkout-session"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)