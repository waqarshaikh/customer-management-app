# Generated by Django 3.1.7 on 2021-04-27 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210427_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(choices=[], to='accounts.Tag'),
        ),
    ]
