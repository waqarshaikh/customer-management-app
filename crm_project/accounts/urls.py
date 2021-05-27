from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),    
    path('customers/', views.customer, name='customers'),    
    path('customer_feedbacks/', views.customer_feedbacks, name='customer_feedbacks'),
    path('update_customer/<id>', views.update_customer, name='update_customer'),
    path('delete_customer/<id>', views.delete_customer, name='delete_customer'),
    path('create_customer/', views.create_customer, name='create_customer'),    
    path('update_product/<id>', views.update_product, name='update_product'),
    path('delete_product/<id>', views.delete_product, name='delete_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('employee/<id>', views.employee, name='employee'),
    path('create_order/<id>', views.create_order, name='create_order'),
    path('update_order/<id>', views.update_order, name='update_order'),
    path('delete_order/<id>', views.delete_order, name='delete_order'),

    path('leads/', views.leads, name='leads'),
    path('create_lead/', views.create_lead, name='create_lead'),
    path('update_lead/<id>', views.update_lead, name='update_lead'),
    path('delete_lead/<id>', views.delete_lead, name='delete_lead'),
    path('convert_lead/<id>', views.convert_lead, name='convert_lead'),

    path('opportunities/', views.opportunities, name='opportunities'),
    path('create_opportunity/', views.create_opportunity, name='create_opportunity'),
    path('update_opportunity/<id>', views.update_opportunity, name='update_opportunity'),
    path('delete_opportunity/<id>', views.delete_opportunity, name='delete_opportunity'),   
    path('convert_opportunity/<id>', views.convert_opportunity, name='convert_opportunity'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.user_page, name='user-page'),
    path('send_email/<id>', views.send_email, name='send-email'),
    path('account/', views.account_settings, name='account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
]