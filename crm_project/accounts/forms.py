from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Call, Company, Contact, Customer, Email, Employee, Lead, Opportunity, Order, Product, Tag

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee    
        fields = '__all__'
        exclude = ['user']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class LeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        exclude = ['contact', 'company', 'call']

    # def __init__(self, *args, **kwargs):
    #     self.fields["comment"].widget = forms.Textarea(attrs={"rows":4,"cols":20})

class OpportunityForm(ModelForm):
    class Meta:
        model = Opportunity
        fields = '__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        
        exclude = ['profile_pic', ]

    # def __init__(self, *args, **kwargs):
    #     self.fields["address"].widget = forms.Textarea(attrs={"rows":4,"cols":20})

class CallForm(ModelForm):
    class Meta:
        model = Call
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
             
    def __init__(self, *args, **kwargs):
        
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'message']