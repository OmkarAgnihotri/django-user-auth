# Generated by Django 3.0.3 on 2020-06-11 14:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_auto_20200611_1854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordresets',
            old_name='verification_code',
            new_name='verification_token',
        ),
        migrations.AlterField(
            model_name='passwordresets',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 19, 57, 39, 816502)),
        ),
    ]
