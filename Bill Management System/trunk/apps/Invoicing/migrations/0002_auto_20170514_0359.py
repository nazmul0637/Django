# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-14 03:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContractAgreementPurposes',
            new_name='ContractAgreementPurpose',
        ),
        migrations.AlterModelTable(
            name='contractagreementpurpose',
            table='contract_agreement_purposes',
        ),
    ]
