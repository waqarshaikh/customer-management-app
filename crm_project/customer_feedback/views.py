from .forms import CustomerFeedbackForm, InterstedCustomerForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

def customer_feedback(request):
    context = {}
    form = CustomerFeedbackForm()

    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Thanks for giving your valuable feedback!</h2>')
    
    context['form'] = form
    return render(request, 'customer_feedback/customer_feedback.html', context)

def intrested_customer(request):
    context = {}
    form = InterstedCustomerForm()

    if request.method == 'POST':
        form = InterstedCustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Thanks for showing your intrest in our product!</h2>')
    
    context['form'] = form
    return render(request, 'customer_feedback/intrested_customer.html', context)
