from django import forms
from accounts.models import Product, Employee
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm
from .models import CustomerComplaint, CustomerFeedback, IntrestedCustomer

class CustomerFeedbackForm(ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        
        super(CustomerFeedbackForm, self).__init__(*args, **kwargs)

        self.fields["product"].widget = CheckboxSelectMultiple()
        self.fields["product"].queryset = Product.objects.all()
        self.fields["feedback"].widget = forms.Textarea(attrs={"rows":4,"cols":20})

class InterstedCustomerForm(ModelForm):
    class Meta:
        model = IntrestedCustomer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        
        super(InterstedCustomerForm, self).__init__(*args, **kwargs)

        self.fields["product"].widget = CheckboxSelectMultiple()
        self.fields["product"].queryset = Product.objects.all()

class CustomerComplaintForm(ModelForm):
    class Meta:
        model = CustomerComplaint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        
        super(CustomerComplaintForm, self).__init__(*args, **kwargs)

        self.fields["product"].widget = CheckboxSelectMultiple()
        self.fields["product"].queryset = Product.objects.all()

        self.fields["employee"].widget = CheckboxSelectMultiple()
        self.fields["employee"].queryset = Employee.objects.all()
        self.fields["message"].widget = forms.Textarea(attrs={"rows":4,"cols":20})