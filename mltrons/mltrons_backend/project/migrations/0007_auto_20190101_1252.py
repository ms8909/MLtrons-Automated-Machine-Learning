# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-01 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20190101_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
