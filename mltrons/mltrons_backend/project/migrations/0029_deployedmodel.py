# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-30 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_auto_20190129_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.TrainingModel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
    ]
