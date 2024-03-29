# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-12 17:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_auto_20190112_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accuracy',
            old_name='training_metric',
            new_name='training_model',
        ),
        migrations.RenameField(
            model_name='actualvsprediction',
            old_name='training_metric',
            new_name='training_model',
        ),
        migrations.RenameField(
            model_name='blueprint',
            old_name='training_metric',
            new_name='training_model',
        ),
        migrations.RenameField(
            model_name='featureimportance',
            old_name='training_metric',
            new_name='training_model',
        ),
        migrations.RenameField(
            model_name='lossvsinteraction',
            old_name='training_metric',
            new_name='training_model',
        ),
        migrations.RenameField(
            model_name='roc',
            old_name='training_metric',
            new_name='training_model',
        ),
    ]
