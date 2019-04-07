# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocs',
            name='doc_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed')], default='Pending', max_length=37),
        ),
        migrations.AddField(
            model_name='userdocs',
            name='y_variables',
            field=models.TextField(blank=True, null=True),
        ),
    ]