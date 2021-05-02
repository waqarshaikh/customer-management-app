# Generated by Django 3.1.7 on 2021-05-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210430_0953'),
        ('customer_feedback', '0008_auto_20210502_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerComplaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('email', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('message', models.TextField(max_length=500, null=True)),
                ('employee', models.ManyToManyField(to='accounts.Employee')),
                ('product', models.ManyToManyField(to='accounts.Product')),
            ],
        ),
    ]
