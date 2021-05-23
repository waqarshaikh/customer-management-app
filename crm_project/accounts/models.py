from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default='default-profile-pic.jpg')

    def __str__(self):
        return str(self.name)

class Customer(models.Model):
    name = models.CharField(max_length=50, null=True)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )

    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, null=True,  choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name

class Lead(models.Model):
    SOURCES = (
        ('Facebook', 'Facebook'),
        ('Google', 'Google'),
        ('Friend to Friend', 'Friend to Friend'),
        ('Twitter', 'Twitter'),
        ('By Company', 'By Company'),
        ('LinkedIn', 'LinkedIn'),
    )

    STATUS = (
        ('New', 'New'),
        ('Working', 'Working'),
        ('Contacted', 'Contacted'),
        ('Proposal Sent', 'Proposal Sent'),
        ('Qualified', 'Qualified'),
        ('Customer (converted lead)', 'Customer (converted lead)'),
        ('Closed', 'Closed'),
        ('Others', 'Others'),
    )
    name = models.CharField(max_length=30, null=True, blank=True)
    source = models.CharField(max_length=20, null=True,  choices=SOURCES)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    comment = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name