from django.db import models
from accounts.models import Product

class CustomerFeedback(models.Model):
    stars = (
        ('1 Star', '1 Star'),
        ('2 Stars', '2 Stars'),
        ('3 Stars', '3 Stars'),
        ('4 Stars', '4 Stars'),
        ('5 Stars', '5 Stars'),
    )
    name = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=15, null=True)
    product = models.OneToOneField(Product, null=True, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=500, null=True)
    rate = models.CharField(max_length=10, choices=stars, default='5 Stars')

    def __str__(self):
        return str(self.name)