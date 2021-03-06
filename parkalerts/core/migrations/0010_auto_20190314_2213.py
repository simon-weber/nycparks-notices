# Generated by Django 2.1.5 on 2019-03-15 02:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190218_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='address',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='facility_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, help_text='Don\'t see your location? <a href="mailto:simon@simonmweber.com?subject=Please add my NYC Parks location">Email me</a> and I\'ll add it.', size=None, verbose_name='locations'),
        ),
    ]
