# Generated by Django 3.1.7 on 2021-05-03 17:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer_feedback', '0009_customercomplaint'),
        ('accounts', '0020_auto_20210503_2134'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='Customer',
        ),
    ]