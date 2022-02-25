from django.db.models import Q
from .serializers import LeadSerializer
from typing import DefaultDict
from customer_feedback.models import CustomerFeedback, IntrestedCustomer, CustomerComplaint
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
from .forms import CallForm, CompanyForm, ContactForm, CustomerForm, EmailForm, LeadForm, MeetingForm, OpportunityForm, OrderForm, CreateUserForm, EmployeeForm, ProductForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
    print(request.user)
    leads = Lead.objects.all().filter(status="Lead", delete=False)
    products = Product.objects.all()
    opportunities =Lead.objects.all().filter(status="Opportunity", delete=False)
    customers = Lead.objects.all().filter(status="Customer", delete=False)
    orders = Order.objects.all()
    employees = User.objects.filter(groups__name='employee')
    total_employees = employees.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    last_five_orders = orders.order_by('-id')[:5]

    employee_data = []
    
    for emp in employees:
        _leads = emp.employee.lead_set.filter(status="Lead", delete=False)
        _opportunities = emp.employee.lead_set.filter(status="Opportunity", delete=False)
        _customers = emp.employee.lead_set.filter(status="Customer", delete=False)
    
        employee = [
            emp.username,
            _leads.count(),
            _opportunities.count(),
            _customers.count(),
        ]
        employee_data.append(employee)

    context = {'orders': orders, 'employees': employees, 
        'total_orders': total_orders, 'total_employees': total_employees,
        'delivered': delivered, 'pending': pending, 'last_five_orders': last_five_orders,
        'total_leads': leads.count(), 'total_opportunities': opportunities.count(), 'total_customers': customers.count(),
        'employee_data': employee_data, 'products': products,
    }
    render(request, "accounts/base.html", context)

    return render(request, 'accounts/dashboard.html', context)

class ParseExcel(APIView):
    def post(self, request, format=None):
        import_url = 'http://localhost:8000/import/'
        try:
            excel_file = request.FILES['files']
        except MultiValueDictKeyError:
            messages.error(request, 'File not found!')
            return redirect(import_url)
        
        file_extension = str(excel_file).split('.')[-1]
        
        if file_extension == 'xls':
            data = get_xls_data(excel_file, column_limit=5)
        elif file_extension == 'xlsx':
            data = get_xlsx_data(excel_file, column_limit=5)
        else:
            messages.error(request, 'Invalid File, Upload Excel file only!')
            return redirect(import_url)

        leads = data['Sheet1']
        lead_count = 0

        if len(leads) > 1:
            for lead in leads:
                if len(lead) > 0:
                    if lead[0] != 'CompanyName':
                        if len(lead) < 9:
                            i = len(lead)
                            while i < 8:
                                lead.append('')
                                i += 1
                        if lead:
                            lead_count += 1
                            Lead.objects.create(
                                company_name=lead[0], 
                                gstin=lead[1],
                                address=lead[2],
                                city=lead[3],
                                state=lead[4],
                                pin_code=lead[5],
                                mobile=lead[6],
                                email=lead[7],
                                pan_card=lead[8]
                            )
        messages.success(request, f'Succesfully added {lead_count} Leads')
        return redirect(import_url)

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
def get_customers(request, opportunities):
    customers = []
    for opportunity in opportunities:
        if hasattr(opportunity, 'customer'):
            customers.append(opportunity.customer)
    return customers

def get_employee_customers(request):
    opportunities = get_employee_opportunities(request)
    customers = []
    for opportunity in opportunities:
        if hasattr(opportunity, 'customer'):
            customers.append(opportunity.customer)
    return customers

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def customers(request):
    customers = []
    if request.user.is_staff:
        customers = Lead.objects.all().filter(status="Customer", delete=False)
    else:
        customers = request.user.employee.lead_set.filter(status="Customer", delete=False)
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
    customer = Lead.objects.get(id=id)

    if request.method == 'POST':
        if customer.delete:
            customer.delete()
        else:
            customer.delete = True
            customer.save()
        return redirect('http://localhost:8000/customers/')
        
    context = {'data': customer, 'delete': f'delete_customer', 'reverse': "customers"}
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
            leads = Lead.objects.all().filter(status="Lead", delete=False)
        else: 
            leads = self.request.user.employee.lead_set.filter(status="Lead", delete=False)
            
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
            lead.status = "Lead"
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
        if lead.delete:
            lead.delete()
        else:
            lead.delete = True
            lead.save()
        return redirect('http://localhost:8000/leads/')
        
    context = {'data': lead, 'delete': f'delete_lead', 'reverse': lead._meta.verbose_name_plural}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def convert_lead(request, id):
    lead = Lead.objects.get(id=id)
    lead.status = "Opportunity" if lead.status == "Lead" else "Customer"
    lead.save()

    messages.success(request, f'Lead  {lead}  succesfully converted to Opportunity.')

    if request.user.is_staff:
        return redirect('/')
    return redirect('http://localhost:8000/opportunities/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def restore_lead(request, id, data):
    name = data
    data = Lead.objects.get(id=id)
            
    data.delete = False
    data.save()
    return redirect(name)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def leads_recycle_bin(request, data):
    name = data
    if data == "leads":
        data = Lead.objects.filter(status="Lead", delete=True) if request.user.is_staff else request.user.employee.lead_set.filter(status="Lead", delete=True)
    elif data == "opportunities":
        data = Lead.objects.filter(status="Opportunity", delete=True) if request.user.is_staff else request.user.employee.lead_set.filter(status="Opportunity", delete=True)
    elif data == "customers":
        data = Lead.objects.filter(status="Customer", delete=True) if request.user.is_staff else request.user.employee.lead_set.filter(status="Customer", delete=True)
    
    context = {'data': data, 'name': name}
    return render(request, 'accounts/lead_recycle_bin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def success_leads(request, data):
    if data == "leads":
        data = Lead.objects.filter(Q(status="Opportunity") | Q(status="Customer")) if request.user.is_staff else request.user.employee.lead_set.filter(Q(status="Opportunity") | Q(status="Customer"))
    elif data == "opportunities":
        data = Lead.objects.filter(status="Customer") if request.user.is_staff else request.user.employee.lead_set.filter(status="Customer")

    context = {'data': data}
    return render(request, 'accounts/success_leads.html', context)


#-----------------Lead end----------------------------------------------
#-----------------Opportunity start----------------------------------------------

def get_opportunity(request, leads):
    opportunities = []
    for lead in leads:
        if hasattr(lead, 'opportunity'):
            opportunities.append(lead.opportunity)
    return opportunities

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
    if request.user.is_staff:
        opportunities = Lead.objects.filter(status="Opportunity", delete=False)
    else: 
        opportunities = request.user.employee.lead_set.filter(status="Opportunity", delete=False)

    return render(request, 'accounts/opportunities.html', {'opportunities': opportunities})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def create_opportunity(request):
    context = {}
    
    form = LeadForm()

    if request.method == 'POST':
        form = LeadForm(request.POST)

        if form.is_valid():
            opportunity = form.save()
            opportunity.status = "Opportunity"
            return redirect('/') 

    context = {'form': form}
    return render(request, 'accounts/lead_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
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
@allowed_users(allowed_roles=['employee', 'admin'])
def delete_opportunity(request, id):
    opportunity = Lead.objects.get(id=id)

    if request.method == 'POST':
        if opportunity.delete:
            opportunity.delete()
        else:
            opportunity.delete = True
            opportunity.save()
        return redirect('http://localhost:8000/opportunities/')
        
    context = {'data': opportunity, 'delete': f'delete_opportunity', 'reverse': "opportunities"}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def convert_opportunity(request, id):
    opportunity = Lead.objects.get(id=id)
    opportunity.status = "Customer"
    opportunity.save()
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

#-----------------Meeting end----------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def meetings(request, id):
    lead = Lead.objects.get(id=id)
    meetings = lead.meeting_set.all()

    context = {'meetings': meetings, 'lead':lead}
    return render(request, 'accounts/meetings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def create_meeting(request, id):
    lead = Lead.objects.get(id=id)
    
    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST)

        if meeting_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.lead = lead
            meeting_form.save()
            messages.success(request, "Succesfully added meeting")
            return redirect(f'/lead_detail/{id}/meetings') 
    else:
        meeting_form = MeetingForm()
    context = {'meeting_form': meeting_form}
    return render(request, 'accounts/meeting_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def update_meeting(request, id, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    form = MeetingForm(instance=meeting)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect(f'http://localhost:8000/lead_detail/{id}/meetings/') 
    
    context = {'meeting_form': form}
    return render(request, 'accounts/meeting_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def delete_meeting(request, id, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    print("delete.....")
    if request.method == 'POST':
        meeting.delete()
        return redirect(f'http://localhost:8000/lead_detail/{id}/meetings/')
        
    context = {'data': meeting,'delete': f'/lead_detail/{id}/meetings/delete/{meeting_id}/', 'reverse': f'/lead_detail/{id}/meetings/'}
    return render(request, 'accounts/delete.html', context)
#-----------------Meeting end----------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def lead_detail_view(request, id):
    lead = Lead.objects.get(id=id)
    contact = lead.contact_set.all().first()

    context = {
        'lead': lead, 'contact': contact
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
@allowed_users(allowed_roles=['employee', 'admin'])
def send_email(request, id):
    form = EmailForm()
    lead = Lead.objects.get(id=id)
    
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
    
        if form.is_valid():
            email = form.save()

            message = request.POST.get('message')
            subject = request.POST.get('subject')
            image = email.img
            from_email = settings.EMAIL_HOST_USER
            to_email =  lead.company.company_email

            print("Image: ",image)
            print("Email: ",lead.company.company_email)
            
            img_data =  open(f'D:\Web\Django\customer-management-app\crm_project\static\images\{image}', 'rb').read()

            html_part = MIMEMultipart(_subtype='related')
           
            body = MIMEText('<br><img src="cid:myimage" />', _subtype='html')
            html_part.attach(body)

            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>') 
            img.add_header("Content-Disposition", "inline", filename="myimage") 
            html_part.attach(img)

            msg = EmailMessage(subject, message, from_email, [to_email])
            msg.attach(html_part) 
            print(f"Message: {message}\n Subject: {subject}\n From: {from_email}\n To: {to_email}\nImage: {img}")
            msg.send()
            
        print(form.errors)
        return HttpResponse('<h1>Email sent </h1>')
    
    context = {'form': form}

    return render(request, 'accounts/email_form.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def user_page(request):
    orders = request.user.employee.order_set.all()
    leads = request.user.employee.lead_set.filter(status="Lead", delete=False)
    opportunities = request.user.employee.lead_set.filter(status="Opportunity", delete=False)
    customers = request.user.employee.lead_set.filter(status="Customer", delete=False)
    print(leads.count())
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,  'total_orders': total_orders,
        'delivered': delivered, 'pending': pending, 
        'customers': customers, 'leads': leads, 'opportunities': opportunities,
        'total_leads': leads.count(), 'total_opportunities': opportunities.count(), 'total_customers': customers.count(),
    }
    print('request')
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def users(request):
    users = User.objects.filter(is_superuser=False)
    
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
@allowed_users(allowed_roles=['admin'])
def delete_employee(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        user.delete()
        return redirect('/')
        
    context = {'data': user, 'delete': f'delete-employee', 'reverse': "users"}
    return render(request, 'accounts/delete.html', context)

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
