# Generated by Django 3.1.7 on 2021-05-27 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20210527_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=225, null=True),
        ),
    ]
