# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-02 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0043_task_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_tasks', to='project.Project'),
        ),
    ]
