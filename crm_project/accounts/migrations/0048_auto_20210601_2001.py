# Generated by Django 3.1.7 on 2021-06-01 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_email_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='call',
            options={'verbose_name_plural': 'calls'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': 'customers'},
        ),
        migrations.AlterModelOptions(
            name='lead',
            options={'verbose_name_plural': 'leads'},
        ),
        migrations.AlterModelOptions(
            name='opportunity',
            options={'verbose_name_plural': 'opportunities'},
        ),
    ]