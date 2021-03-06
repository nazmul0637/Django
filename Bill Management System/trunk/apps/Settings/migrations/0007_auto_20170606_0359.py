# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 03:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Settings', '0006_holiday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_no',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='bank_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='branch_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='name_of_account',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='routing_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='swift_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='branch_id',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='holiday_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='holiday_type',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='invoicetemplate',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_template_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicetemplate',
            name='status',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='invoicetemplate',
            name='template_body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='invoicetemplate',
            name='title',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='invoicetemplate',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_template_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
