# Generated by Django 3.0.3 on 2020-06-12 12:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_auto_20200612_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresets',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 12, 17, 46, 21, 36812)),
        ),
        migrations.AlterField(
            model_name='passwordresets',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
