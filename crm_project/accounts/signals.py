from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Employee

def employee_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employee')
        instance.groups.add(group)

        Employee.objects.create(user=instance, name=instance.username,)
    print('Profile created!')

post_save.connect(employee_profile, sender=User)