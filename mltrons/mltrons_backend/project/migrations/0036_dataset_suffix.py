# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-31 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_auto_20190130_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='suffix',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
