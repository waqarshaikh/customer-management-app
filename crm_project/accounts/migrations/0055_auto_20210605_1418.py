# Generated by Django 3.1.7 on 2021-06-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_auto_20210605_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lead',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
