# Generated by Django 3.1.7 on 2021-05-21 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20210521_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employee'),
        ),
    ]