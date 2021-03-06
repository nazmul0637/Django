# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 03:46
from __future__ import unicode_literals

import Employees.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employees', '0003_auto_20170525_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='status',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='designation',
            name='title',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contact_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='current_salary',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_joining',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='father_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mother_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='employee',
            name='national_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='permanent_address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='present_address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=Employees.models.upload_location),
        ),
        migrations.AlterField(
            model_name='employee',
            name='starting_salary',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.BooleanField(),
        ),
    ]
