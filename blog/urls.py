from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_cart
from blog.views import article
from django.urls import path

from . import views


urlpatterns = [

     path('', index, name="blog-index"),
     path('article-<str:numero_article>/', article, name="blog-article"),

 ]