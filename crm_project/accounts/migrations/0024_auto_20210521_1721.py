# Generated by Django 3.1.7 on 2021-05-21 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20210521_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employee'),
        ),
    ]
