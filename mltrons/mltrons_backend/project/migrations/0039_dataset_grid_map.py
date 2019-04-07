# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-31 16:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_auto_20190131_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='grid_map',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
