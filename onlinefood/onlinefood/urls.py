"""
URL configuration for onlinefood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from foodapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_page , name="login_page"),
    path('register/', register , name="register"),
    path('logout/', logout_page, name="logout_page"),
    path('add-cart/<item_uid>', add_cart, name='add_cart'),
    path('cart/',cart, name="cart"),
    path('remove_cart_items/<cart_item_uid>', remove_cart_items, name="remove_cart_items"),
    path('orders/', orders, name='orders'),
    path('add-item/', add_item, name='add_item'),
    path('all-items/', all_items, name='all_items'),
     path('delete-recipe/<item_uid>/', delete_item, name="delete_item"),
    path('update-recipe/<item_uid>/', update_item, name="update_item"),
    path('success/', success, name="success"),
    path('all-orders/', all_orders, name="all_orders"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
