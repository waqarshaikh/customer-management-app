# Generated by Django 3.1.7 on 2021-07-04 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0065_auto_20210704_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='contact',
        ),
    ]
