from .serializers import LeadSerializer
from typing import DefaultDict
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
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError


from pyexcel_xls import get_data as get_xls_data
from pyexcel_xlsx import get_data as get_xlsx_data
from rest_framework.views import APIView

from rest_framework import viewsets


from .models import *
from .forms import CallForm, CompanyForm, ContactForm, CustomerForm, EmailForm, LeadForm, OpportunityForm, OrderForm, CreateUserForm, EmployeeForm, ProductForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
    print(request.user)
    leads = Lead.objects.all()
    opportunities = Opportunity.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    employees = User.objects.filter(groups__name='employee')
    total_employees = employees.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    last_five_orders = orders.order_by('-id')[:5]

    context = {'orders': orders, 'employees': employees, 
        'total_orders': total_orders, 'total_employees': total_employees,
        'delivered': delivered, 'pending': pending, 'last_five_orders': last_five_orders,
        'total_leads': leads.count(), 'total_opportunities': opportunities.count(), 'total_customers': customers.count(),
    }
    return render(request, 'accounts/dashboard.html', context)

# class ParseExcel(APIView):
#     def post(self, request, format=None):
#         import_url = 'http://localhost:8000/import/'
#         try:
#             excel_file = request.FILES['files']
#         except MultiValueDictKeyError:
#             messages.error(request, 'File not found!')
#             return redirect(import_url)
        
#         file_extension = str(excel_file).split('.')[-1]
        
#         if file_extension == 'xls':
#             data = get_xls_data(excel_file, column_limit=9)
#         elif file_extension == 'xlsx':
#             data = get_xlsx_data(excel_file, column_limit=9)
#         else:
#             messages.error(request, 'Invalid File, Upload Excel file only!')
#             return redirect(import_url)

#         sellers = data['Sheet1']
#         seller_count = 0

#         if len(sellers) > 1:
#             for seller in sellers:
#                 if len(seller) > 0:
#                     if seller[0] != 'CompanyName':
#                         if len(seller) < 9:
#                             i = len(seller)
#                             while i < 8:
#                                 seller.append('')
#                                 i += 1
#                         if seller:
#                             seller_count += 1
#                             Seller.objects.create(
#                                 company_name=seller[0], 
#                                 gstin=seller[1],
#                                 address=seller[2],
#                                 city=seller[3],
#                                 state=seller[4],
#                                 pin_code=seller[5],
#                                 mobile=seller[6],
#                                 email=seller[7],
#                                 pan_card=seller[8]
#                             )
#         messages.success(request, f'Succesfully added {seller_count} Sellers')
#         return redirect(import_url)

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
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    order_count = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'employee': customer, 'orders': orders, 
        'order_count': order_count, 'my_filter': my_filter
    }
    return render(request, 'accounts/customer.html', context)

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
@allowed_users(allowed_roles=['employee', 'admin'])
def index(request):
    return render(request, 'accounts/leads.html')

class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            leads = Lead.objects.all()
        else: 
            leads = self.request.user.employee.lead_set.all()
        return leads
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'employee'])
# def leads(request):
#     if request.user.is_staff:
#         leads = Lead.objects.all()
#     else: 
#         leads = request.user.employee.lead_set.all()
    
#     return render(request, 'accounts/leads.html', {'leads': leads})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_lead(request):
    context = {}
    
    lead_form = LeadForm()
    contact_form = ContactForm()
    company_form = CompanyForm()

    if request.method == 'POST':
        lead_form = LeadForm(request.POST)
        contact_form = ContactForm(request.POST)
        company_form = CompanyForm(request.POST)

        print('Pre save')
        print(lead_form.errors)
        print(contact_form.errors)
        print(company_form.errors)
        if lead_form.is_valid() and contact_form.is_valid() and company_form.is_valid():
            lead = lead_form.save()
            print('lead save')
            company = company_form.save()
            print('company save')
            contact = contact_form.save(commit=False)
            setattr(lead, 'company', company)
            contact.lead = lead
            contact_form.save() 
            lead.save()
            lead_form.save()
            
            return redirect('http://localhost:8000/leads/') 

    context = {'lead_form': lead_form, 'contact_form': contact_form, 'company_form': company_form}
    return render(request, 'accounts/lead_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def update_lead(request, id):
    lead = Lead.objects.get(id=id)
    
    lead_form = LeadForm(instance=lead)
    print(lead.company)
    company_form = CompanyForm(instance=lead.company)
    contact_form = ContactForm(instance=lead.contact_set.all().first())

    if request.method == 'POST':
        lead_form = LeadForm(request.POST, instance=lead)
        contact_form = ContactForm(request.POST, instance=lead.contact_set.all().first())
        company_form = CompanyForm(request.POST, instance=lead.company)
        print("pre save")
        if lead_form.is_valid() and contact_form.is_valid() and company_form.is_valid():
            lead = lead_form.save()
            contact_form.save()
            company_form.save()
            print("post save")
            messages.success(request, f'Succesfully updated Lead {lead.company}')
            return redirect('http://localhost:8000/leads/') 
    
    context = {'lead_form': lead_form, 'contact_form': contact_form, 'company_form': company_form}
    return render(request, 'accounts/lead_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def delete_lead(request, id):
    lead = Lead.objects.get(id=id)

    if request.method == 'POST':
        lead.delete()
        return redirect('http://localhost:8000/leads/')
        
    context = {'data': lead, 'delete': f'delete_lead', 'reverse': lead._meta.verbose_name_plural}
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
        
    context = {'data': opportunity, 'delete': f'delete_opportunity', 'reverse': opportunity._meta.verbose_name_plural}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def convert_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)
    customer = Customer.objects.create(opportunity=opportunity, contact=opportunity.contact)

    messages.success(request, f'Opportunity {opportunity} succesfully converted to Customer.')

    return redirect('http://localhost:8000/customers/') 
#-----------------Opportunity end----------------------------------------------
#-----------------Call end----------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def calls(request, id):
    lead = Lead.objects.get(id=id)
    calls = lead.call_set.all()

    context = {'calls': calls, 'lead':lead}
    return render(request, 'accounts/calls.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def create_call(request, id):
    lead = Lead.objects.get(id=id)
    
    if request.method == 'POST':
        call_form = CallForm(request.POST)

        if call_form.is_valid():
            call = call_form.save(commit=False)
            call.lead = lead
            call_form.save()
            messages.success(request, "Succesfully added call")
            return redirect(f'/lead_detail/{id}/calls') 
    else:
        call_form = CallForm()
    context = {'call_form': call_form}
    return render(request, 'accounts/call_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def update_call(request, id, call_id):
    call = Call.objects.get(id=call_id)
    form = CallForm(instance=call)

    if request.method == 'POST':
        form = CallForm(request.POST, instance=call)
        if form.is_valid():
            form.save()
            return redirect(f'http://localhost:8000/lead_detail/{id}/calls/') 
    
    context = {'call_form': form}
    return render(request, 'accounts/call_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def delete_call(request, id, call_id):
    call = Call.objects.get(id=call_id)

    if request.method == 'POST':
        call.delete()
        return redirect(f'http://localhost:8000/lead_detail/{id}/calls/')
        
    context = {'data': call,'delete': f'/lead_detail/{id}/calls/delete/{call_id}/', 'reverse': f'/lead_detail/{id}/calls/'}
    return render(request, 'accounts/delete.html', context)
#-----------------Call end----------------------------------------------

#-----------------Contact end----------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def contacts(request, id):
    lead = Lead.objects.get(id=id)
    contacts = lead.contact_set.all()

    context = {'contacts': contacts, 'lead':lead}
    return render(request, 'accounts/contacts.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def create_contact(request, id):
    lead = Lead.objects.get(id=id)
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.lead = lead
            contact_form.save()
            messages.success(request, "Succesfully added contact")
            return redirect(f'/lead_detail/{id}/contacts') 
    else:
        contact_form = ContactForm()
    context = {'contact_form': contact_form}
    return render(request, 'accounts/contact_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def update_contact(request, id, contact_id):
    contact = Contact.objects.get(id=contact_id)
    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(f'http://localhost:8000/lead_detail/{id}/contacts/') 
    
    context = {'contact_form': form}
    return render(request, 'accounts/contact_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def delete_contact(request, id, contact_id):
    contact = Contact.objects.get(id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect(f'http://localhost:8000/lead_detail/{id}/contacts/')
        
    context = {'data': contact,'delete': f'/lead_detail/{id}/contacts/delete/{contact_id}/', 'reverse': f'/lead_detail/{id}/contacts/'}
    return render(request, 'accounts/delete.html', context)
#-----------------Contact end----------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def lead_detail_view(request, id):
    lead = Lead.objects.get(id=id)
    
    context = {
        'lead': lead
    }
    return render(request, 'accounts/customer.html', context)

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
def send_email(request, id):
    form = EmailForm()
    customer = Customer.objects.get(id=id)

    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            message = request.POST.get('message')
            subject = request.POST.get('subject')
            from_email = settings.EMAIL_HOST_USER
            to_email = "mailmerairishabh99@gmail.com"
            
            img_data =  open('D:\Web\Django\customer-management-app\crm_project\static\images\LOGO.png', 'rb').read()

            html_part = MIMEMultipart(_subtype='related')
           
            body = MIMEText('<h3>Image: </h3><br><img src="cid:myimage" />', _subtype='html')
            html_part.attach(body)

            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>') 
            img.add_header("Content-Disposition", "inline", filename="myimage") 
            html_part.attach(img)

            msg = EmailMessage(subject, message, from_email, [to_email])
            msg.attach(html_part) 
            print(f"Message: {message}\n Subject: {subject}\n From: {from_email}\n To: {to_email}\nImage: {img}")
            msg.send()
            
            messages.success(request, f'Email sucesfully send to {customer}')
        print(form.errors)
        return HttpResponse('Email sent')
    
    context = {'form': form}

    return render(request, 'accounts/email_form.html', context)
    

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
        'customers': customers, 'leads': leads, 'opportunities': opportunities,
        'total_leads': leads.count(), 'total_opportunities': opportunities.__len__(), 'total_customers': customers.__len__(),
    }
    print('request')
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def users(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'accounts/users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_employee(request, id):
    user = User.objects.get(id=id)
    group = Group.objects.get(name='employee')
    user.groups.add(group)
    messages.success(request, 'Succesfully User added to Employee')
    return redirect('/')


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
