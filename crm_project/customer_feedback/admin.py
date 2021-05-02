from .models import CustomerComplaint, CustomerFeedback, IntrestedCustomer
from django.contrib import admin

admin.site.register(CustomerFeedback)
admin.site.register(IntrestedCustomer)
admin.site.register(CustomerComplaint)
