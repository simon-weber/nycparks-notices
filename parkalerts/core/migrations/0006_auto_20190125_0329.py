# Generated by Django 2.1.5 on 2019-01-25 03:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190125_0106'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Greeting',
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='address',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='key',
            field=models.UUIDField(default=uuid.uuid1, editable=False, unique=True),
        ),
    ]
