from django.forms import ModelForm
from .models import CustomerFeedback

class CustomerFeedbackForm(ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'
