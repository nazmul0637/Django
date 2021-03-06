# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Settings', '0003_auto_20170530_0535'),
        ('Invoicing', '0013_auto_20170525_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractagreement',
            name='bank_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Settings.Bankaccount'),
        ),
        migrations.AlterField(
            model_name='billschedule',
            name='contract_agreement_purpose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_schedules', to='Invoicing.ContractAgreementPurpose'),
        ),
    ]
