from accounts.models import Product
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm
from .models import CustomerFeedback, IntrestedCustomer

class CustomerFeedbackForm(ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        
        super(CustomerFeedbackForm, self).__init__(*args, **kwargs)

        self.fields["product"].widget = CheckboxSelectMultiple()
        self.fields["product"].queryset = Product.objects.all()

class InterstedCustomerForm(ModelForm):
    class Meta:
        model = IntrestedCustomer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        
        super(InterstedCustomerForm, self).__init__(*args, **kwargs)

        self.fields["product"].widget = CheckboxSelectMultiple()
        self.fields["product"].queryset = Product.objects.all()