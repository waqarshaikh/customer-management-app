# Generated by Django 3.1.7 on 2021-07-12 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0068_auto_20210712_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default-company-pic.png', null=True, upload_to='', verbose_name='Logo/Photo'),
        ),
    ]