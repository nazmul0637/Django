# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0021_invoice_invoice_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_sequence',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]