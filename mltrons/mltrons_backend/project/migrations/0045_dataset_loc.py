# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-09 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_auto_20190202_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='loc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
