# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 10:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0007_contractagreementpurpose_amount_per_installment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractagreementpurpose',
            name='installment',
        ),
        migrations.AddField(
            model_name='contractagreementpurpose',
            name='num_installment',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='num installment'),
            preserve_default=False,
        ),
    ]
