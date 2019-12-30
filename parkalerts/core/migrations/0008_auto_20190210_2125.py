# Generated by Django 2.1.5 on 2019-02-10 21:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_status_facility_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
