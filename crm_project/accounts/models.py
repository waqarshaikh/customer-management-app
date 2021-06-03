from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ModelState
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=225, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default='default-profile-pic.jpg')

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

    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL, verbose_name='Assigned to')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, null=True,  choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name

class Contact(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name




class Company(models.Model):
    company_name = models.CharField(max_length=255, null=True)
    company_phone = models.CharField(max_length=15, null=True)
    company_email = models.EmailField(max_length=255, null=True)
    address = models.TextField(max_length=255, null=True)
    website = models.URLField(max_length=255)
    profile_pic = models.ImageField(null=True, blank=True, default='default-profile-pic.jpg', verbose_name="Logo/Photo")
    
    class Meta:
        verbose_name_plural = 'companies'
    
    def class_name(self):
        return self._meta.model_name

    def __str__(self):
        return self.company_name

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
    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, null=True,  choices=SOURCES)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, verbose_name='Assigned To')
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    comment = models.TextField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'leads'
    
    def class_name(self):
        return self._meta.model_name

    def __str__(self):
        return self.company.company_name

class Opportunity(models.Model):
    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE)
    lead = models.OneToOneField(Lead, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'opportunities'
    
    def class_name(self):
        return self._meta.model_name

    def __str__(self):
        return str(self.contact.name)

class Customer(models.Model):
    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE)
    opportunity = models.OneToOneField(Opportunity, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'customers'
    
    def class_name(self):
        return self._meta.model_name

    def __str__(self):
        return str(self.contact.name)

class Email(models.Model):
    subject = models.CharField(max_length=255, null=True)
    img = models.ImageField(null=True, blank=True, default='default-profile-pic.jpg')
    message = models.TextField(max_length=255, null=True) 

    def __str__(self):
        return str(self.subject)


class Call(models.Model):
    CALL_TYPES = (
        ("Call", "Call"),
        ("Conference", "Conference"),
        ("Skype", "Skype"),
        ("WhatsApp", "WhatsApp"),
    )

    FLAGS = (
        ("No Answer", "No Answer"),
        ("Important", "Important"),
        ("Busy", "Busy"),
        ("Urgent", "Urgent"),
        ("Left message", "Left message"),
        ("Reschedule", "Reschedule"),
    )
    lead = models.ForeignKey(Lead, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    call_type = models.CharField(max_length=255, null=True,  choices=CALL_TYPES)
    flag = models.CharField(max_length=255, null=True,  choices=FLAGS)
    description = models.TextField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'calls'
    
    def class_name(self):
        return self._meta.model_name

    def __str__(self):
        return f"{self.call_type} on {self.date}"