# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0005_auto_20170606_0420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='is_person',
        ),
        migrations.AddField(
            model_name='client',
            name='short_name',
            field=models.CharField(default=11, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=100),
        ),
    ]
