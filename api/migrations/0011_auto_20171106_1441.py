# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20171102_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='username',
            field=models.CharField(max_length=40),
        ),
    ]