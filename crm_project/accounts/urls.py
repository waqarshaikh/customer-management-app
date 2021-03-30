from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer', views.customer, name='customer'),
    path('products', views.product, name='products'),
]