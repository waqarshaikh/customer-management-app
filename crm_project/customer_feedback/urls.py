from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_feedback, name='customer-feedback'),

]