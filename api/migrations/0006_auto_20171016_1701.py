# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171013_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-address_id']},
        ),
        migrations.AlterField(
            model_name='exceptionlog',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
