# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-25 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='frame_path',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]