from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),
    path('customer/<id>', views.customer, name='customer'),
    path('create_order/<id>', views.create_order, name='create_order'),
    path('update_order/<id>', views.update_order, name='update_order'),
    path('delete_order/<id>', views.delete_order, name='delete_order'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.user_page, name='user-page'),
]