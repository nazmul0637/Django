# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoicing', '0005_auto_20170516_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractagreementconcernperson',
            name='concern_person_type',
            field=models.CharField(max_length=8),
        ),
    ]