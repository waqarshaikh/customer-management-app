from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_feedback, name='customer-feedback'),
    path('intrested_customer/', views.intrested_customer, name='intrested_customer'),
    path('customer_complaint/', views.customer_complaint, name='customer_complaint'),
]