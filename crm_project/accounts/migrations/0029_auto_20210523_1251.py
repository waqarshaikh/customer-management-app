# Generated by Django 3.1.7 on 2021-05-23 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20210523_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='comment',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
