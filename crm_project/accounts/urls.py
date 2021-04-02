from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),
    path('customer/<id>', views.customer, name='customer'),
    path('create_order/<id>', views.createOrder, name='create_order'),
    path('update_order/<id>', views.updateOrder, name='update_order'),
    path('delete_order/<id>', views.deleteOrder, name='delete_order'),
]