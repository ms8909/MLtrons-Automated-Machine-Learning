# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-28 15:44
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_dataset_columns'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingdetail',
            name='selected_columns',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
