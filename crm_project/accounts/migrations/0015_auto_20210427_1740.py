# Generated by Django 3.1.7 on 2021-04-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210427_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
