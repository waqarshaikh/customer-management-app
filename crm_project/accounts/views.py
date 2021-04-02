from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 
        'total_orders': total_orders, 'total_customers': total_customers,
        'delivered': delivered, 'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)

def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    order_count = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)

def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def create_order(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    #form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        #form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/') 

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

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

def delete_order(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    context = {'order': order}
    return render(request, 'accounts/delete.html', context)

def register_page(request):
    context ={}
    return redirect(request, 'accounts/register.html', context)

def login_page(request):
    context ={}
    return redirect(request, 'accounts/login.html', context)