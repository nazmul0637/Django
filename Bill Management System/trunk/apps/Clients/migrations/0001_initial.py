# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 09:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='code')),
                ('address', models.CharField(max_length=40, verbose_name='address')),
                ('contact_number', models.CharField(max_length=20, verbose_name='contact number')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('description', models.TextField(verbose_name='description')),
                ('is_person', models.BooleanField(default=False, verbose_name='is_person')),
                ('status', models.BooleanField(verbose_name='status')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField()),
                ('updated_by', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='ConcernPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='order')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('designation', models.CharField(max_length=50, verbose_name='designation')),
                ('division', models.CharField(max_length=40, verbose_name='division')),
                ('status', models.BooleanField(verbose_name='status')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concern_persons', to='Clients.Client')),
            ],
            options={
                'db_table': 'client_concern_persons',
            },
        ),
        migrations.AlterUniqueTogether(
            name='concernperson',
            unique_together=set([('order', 'client')]),
        ),
    ]
