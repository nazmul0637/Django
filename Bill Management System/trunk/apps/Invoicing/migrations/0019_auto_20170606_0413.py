# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 04:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0018_auto_20170606_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractagreement',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_agreement_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contractagreement',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_agreement_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
