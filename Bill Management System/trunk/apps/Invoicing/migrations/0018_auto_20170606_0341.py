# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 03:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0017_auto_20170603_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractagreement',
            name='agreement_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='mode_of_payment',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='net_amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='vat',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='contractagreementpurpose',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='contractagreementpurpose',
            name='amount_per_installment',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='contractagreementpurpose',
            name='num_installment',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]