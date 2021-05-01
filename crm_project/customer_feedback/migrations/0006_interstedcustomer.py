# Generated by Django 3.1.7 on 2021-05-01 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210430_0953'),
        ('customer_feedback', '0005_auto_20210430_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterstedCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('email', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('product', models.ManyToManyField(to='accounts.Product')),
            ],
        ),
    ]