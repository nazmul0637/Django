# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0005_auto_20170525_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
    ]
