# Generated by Django 3.1.7 on 2021-05-21 08:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_feedback', '0010_auto_20210503_2255'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0021_auto_20210503_2255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Employee',
        ),
    ]