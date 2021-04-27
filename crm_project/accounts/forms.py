from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Customer, Order, Product, Tag

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

# class ProductForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
             
#     def __init__(self, *args, **kwargs):
        
#         super(ProductForm, self).__init__(*args, **kwargs)

#         self.fields["tags"].widget = CheckboxSelectMultiple()
#         self.fields["tags"].queryset = Tag.objects.all()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']