# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 04:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0006_auto_20170525_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Project', 'Project'), ('Product', 'Product')], max_length=7),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productpurpose',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purpose_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purpose_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
