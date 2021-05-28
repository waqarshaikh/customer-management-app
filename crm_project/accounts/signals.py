from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Employee

def employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance, name=instance.username, email=instance.email)
    print('Profile created!')

post_save.connect(employee_profile, sender=User)