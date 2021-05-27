from .forms import CustomerComplaintForm, CustomerFeedbackForm, InterstedCustomerForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

def customer_feedback(request):
    form = CustomerFeedbackForm(request.POST)

    if form.is_valid():
        form.save()
    return HttpResponse('<h2>Thanks for giving your valuable feedback!</h2>')
  

def intrested_customer(request):
    form = InterstedCustomerForm(request.POST)

    if form.is_valid():
        form.save()

    return HttpResponse('<h2>Thanks for showing your intrest in our product!</h2>')


def customer_complaint(request):
    form = CustomerComplaintForm(request.POST)

    if form.is_valid():
        form.save()
             
    return HttpResponse('<h2>Thanks for submiting your complaint!</h2>')

def customer_feedback_form(request):
    customer_complaint_form = CustomerComplaintForm()
    customer_feedback_form = CustomerFeedbackForm()
    intrested_customer_form = InterstedCustomerForm()

    context = {
        'customer_complaint_form': customer_complaint_form,
        'customer_feedback_form': customer_feedback_form,
        'intrested_customer_form': intrested_customer_form
    }

    return render(request, 'customer_feedback/customer_feedback_form.html', context)
