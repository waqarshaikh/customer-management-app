# Generated by Django 3.1.7 on 2021-06-02 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_auto_20210602_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='email',
            new_name='company_email',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='phone',
            new_name='company_phone',
        ),
    ]
