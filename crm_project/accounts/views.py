from customer_feedback.models import CustomerFeedback, IntrestedCustomer, CustomerComplaint
from django.conf.urls import url
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User

from .models import *
from .forms import ContactForm, CustomerForm, LeadForm, OpportunityForm, OrderForm, CreateUserForm, EmployeeForm, ProductForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
    print(request.user)
    orders = Order.objects.all()
    employees = Employee.objects.all()
    total_employees = employees.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    last_five_orders = orders.order_by('-id')[:5]

    context = {'orders': orders, 'employees': employees, 
        'total_orders': total_orders, 'total_employees': total_employees,
        'delivered': delivered, 'pending': pending, 'last_five_orders': last_five_orders
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee(request, id):
    employee = Employee.objects.get(id=id)
    orders = employee.order_set.all()
    order_count = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'employee': employee, 'orders': orders, 
        'order_count': order_count, 'my_filter': my_filter
    }
    return render(request, 'accounts/employee.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer_feedbacks(request):
    context = {}
    customer_feedbacks = CustomerFeedback.objects.all()
    intrested_customer = IntrestedCustomer.objects.all()
    customer_complaint = CustomerComplaint.objects.all()
    context = {
        'customer_feedbacks': customer_feedbacks,
        'intrested_customer': intrested_customer, 
        'customer_complaint': customer_complaint
    }

    return render(request, 'accounts/customer_feedback.html', context)

#-------------------------Customer start--------------------------------------- 
def get_employee_customers(request):
    opportunities = get_employee_opportunities(request)
    customers = []
    for opportunity in opportunities:
        if hasattr(opportunity, 'customer'):
            customers.append(opportunity.customer)
    return customers

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def customer(request):
    opportunities = []
    customers = []
    if request.user.is_staff:
        customers = Customer.objects.all()
    else:
        customers = get_employee_customers(request)
    return render(request, 'accounts/customers.html', {'customers': customers})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def create_customer(request):
    context = {}
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('http://localhost:8000/customers/')
    
    context['form'] = form
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def update_customer(request, id):
    customer = Customer.objects.get(id=id)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/customers/') 
    
    context = {'form': form}
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def delete_customer(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == 'POST':
        customer.delete()
        return redirect('http://localhost:8000/customers/')
        
    context = {'data': customer}
    return render(request, 'accounts/delete.html', context)
#---------------------------Customer end--------------------------------------------------

#---------------------------Product start-------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_product(request):
    context = {}
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('http://localhost:8000/products/')
    
    context['form'] = form
    return render(request, 'accounts/create_product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_product(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/products/') 
    
    context = {'form': form}
    return render(request, 'accounts/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('http://localhost:8000/products/')
        
    context = {'data': product}
    return render(request, 'accounts/delete.html', context)
#------------------------------Product end-------------------------------------------

#------------------------------Orders start-----------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, id):
    OrderFormSet = inlineformset_factory(Employee, Order, fields=('product', 'status'), extra=10)
    employee = Employee.objects.get(id=id)
    formset = OrderFormSet(instance=employee, queryset=Order.objects.none())
    #form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=employee)
        #form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/') 

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/') 
    
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    context = {'data': order}
    return render(request, 'accounts/delete.html', context)
#-----------------Order end-----------------------------------------------

#-----------------Lead start----------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def leads(request):
    if request.user.is_staff:
        leads = Lead.objects.all()
    else: 
        leads = request.user.employee.lead_set.all()
    return render(request, 'accounts/leads.html', {'leads': leads})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_lead(request):
    context = {}
    
    lead_form = LeadForm()
    contact_form = ContactForm()

    if request.method == 'POST':
        lead_form = LeadForm(request.POST)
        contact_form = ContactForm(request.POST)

        if lead_form.is_valid() and contact_form.is_valid():
            lead = lead_form.save()
            contact = contact_form.save()

            setattr(lead, 'contact', contact)
            lead.save()
            lead_form.save()
            

            return redirect('http://localhost:8000/leads/') 

    context = {'lead_form': lead_form, 'contact_form': contact_form,}
    return render(request, 'accounts/lead_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def update_lead(request, id):
    lead = Lead.objects.get(id=id)
    form = LeadForm(instance=lead)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/leads/') 
    
    context = {'form': form}
    return render(request, 'accounts/lead_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def delete_lead(request, id):
    lead = Lead.objects.get(id=id)

    if request.method == 'POST':
        lead.delete()
        return redirect('http://localhost:8000/leads/')
        
    context = {'data': lead}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def convert_lead(request, id):
    lead = Lead.objects.get(id=id)
    opportunity = Opportunity.objects.create(lead=lead, contact=lead.contact)

    messages.success(request, f'Lead  {lead}  succesfully converted to Opportunity.')

    if request.user.is_staff:
        return redirect('/')
    return redirect('http://localhost:8000/opportunities/') 

#-----------------Lead end----------------------------------------------
#-----------------Opportunity start----------------------------------------------
def get_employee_opportunities(request):
    opportunities = []
    leads = request.user.employee.lead_set.all()
    for lead in leads:
        if hasattr(lead, 'opportunity'):
            opportunities.append(lead.opportunity)
    return opportunities

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def opportunities(request):
    opportunities = []
    if request.user.is_staff:
        opportunities = Opportunity.objects.all()
    else: 
        opportunities = get_employee_opportunities(request)
    return render(request, 'accounts/opportunities.html', {'opportunities': opportunities})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def create_opportunity(request):
    context = {}
    
    form = OpportunityForm()

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
       
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'accounts/opportunity_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def update_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)
    form = OpportunityForm(instance=opportunity)

    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/opportunities/') 
    
    context = {'form': form}
    return render(request, 'accounts/opportunity_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def delete_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)

    if request.method == 'POST':
        opportunity.delete()
        return redirect('http://localhost:8000/opportunities/')
        
    context = {'data': opportunity}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def convert_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)
    customer = Customer.objects.create(opportunity=opportunity, contact=opportunity.contact)

    messages.success(request, request, f'Opportunity {opportunity} succesfully converted to Customer.')

    return redirect('http://localhost:8000/customers/') 
#-----------------Opportunity end----------------------------------------------

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username) 

            return redirect('login')
        
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user 
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            
            login(request, user)
            print(request.user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def user_page(request):
    orders = request.user.employee.order_set.all()
    leads = request.user.employee.lead_set.all()
    opportunities = get_employee_opportunities(request)
    customers = get_employee_customers(request)
    print(leads.count())
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,  'total_orders': total_orders,
        'delivered': delivered, 'pending': pending, 
        'customers': customers, 'leads': leads, 'opportunities': opportunities
    }
    print('request')
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def account_settings(request):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)
