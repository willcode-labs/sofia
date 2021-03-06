# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 21:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=80)),
                ('number', models.IntegerField()),
                ('complement', models.CharField(max_length=40)),
                ('invoice', models.BooleanField()),
                ('delivery', models.BooleanField()),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='ExceptionLog',
            fields=[
                ('exceptionlog_id', models.AutoField(primary_key=True, serialize=False)),
                ('login_id', models.IntegerField(null=True)),
                ('client_login_id', models.IntegerField(null=True)),
                ('ip', models.GenericIPAddressField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=254, null=True)),
                ('message', models.TextField()),
                ('trace', models.TextField(blank=True, null=True)),
                ('url_referer', models.URLField(blank=True, max_length=254, null=True)),
                ('request_data', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exceptionlog',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('login_id', models.IntegerField()),
                ('client_login_id', models.IntegerField(null=True)),
                ('table', models.CharField(max_length=100)),
                ('table_column_pk', models.CharField(max_length=20)),
                ('table_id', models.IntegerField()),
                ('ip', models.GenericIPAddressField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('url_referer', models.URLField(blank=True, max_length=254, null=True)),
                ('request_data', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'log',
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('login_id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_id', models.IntegerField(choices=[(1, 'root'), (2, 'merchant'), (3, 'client')])),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=8)),
                ('verified', models.BooleanField()),
                ('token', models.CharField(max_length=40)),
                ('ip', models.GenericIPAddressField()),
                ('date_expired', models.DateTimeField()),
            ],
            options={
                'db_table': 'login',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchant_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_expired', models.DateTimeField()),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Login')),
            ],
            options={
                'db_table': 'merchant',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
                ('phone1', models.CharField(max_length=60)),
                ('phone2', models.CharField(blank=True, max_length=60, null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Person')),
            ],
            options={
                'db_table': 'person',
                'ordering': ['-person_id'],
            },
        ),
        migrations.AddField(
            model_name='login',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person'),
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person'),
        ),
    ]
