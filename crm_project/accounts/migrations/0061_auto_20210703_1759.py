# Generated by Django 3.1.7 on 2021-07-03 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0060_remove_contact_opportunity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='success',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='success',
        ),
    ]
