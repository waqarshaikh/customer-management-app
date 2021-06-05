# Generated by Django 3.1.7 on 2021-06-04 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0053_auto_20210604_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='id',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='company',
        ),
        migrations.AddField(
            model_name='company',
            name='lead',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.lead'),
            preserve_default=False,
        ),
    ]
