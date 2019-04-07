# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from mlbot_webservices.shared_utils import UploadToPathAndRename
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
User = get_user_model()

class UserDashboard(models.Model):
    dashboard_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    dashboard_name = models.CharField(max_length=256, null=True, blank=True)
    dashboard_url = models.FileField(upload_to=UploadToPathAndRename('Images/User/Dashboard'),null=True, blank=True)  # media/
    graph_key = models.TextField(blank=True, null=True)

    class Meta:
        default_permissions = ()


class UserDocs(models.Model):
    Pending = 'Pending'
    Processed = 'Processed'
    STATUS_CHOICES = (
        (Pending, 'Pending'),
        (Processed, 'Processed'),
    )

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='docs')
    dashboard = models.ForeignKey(UserDashboard, on_delete=models.CASCADE, related_name='docs_dashboard')
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='docs_country')
    file_url = models.FileField(upload_to=UploadToPathAndRename('Images/User/Docs'))  # media/
    doc_status = models.CharField(max_length=37, choices=STATUS_CHOICES, default=Pending)
    y_variables = models.TextField(blank=True, null=True)

    date = models.DateTimeField(default=timezone.now)

    class Meta:
        default_permissions = ()


class DashboardGraphs(models.Model):
    dashboard = models.ForeignKey(UserDashboard, on_delete=models.CASCADE, related_name='graphs')
    graph_url = models.FileField(upload_to=UploadToPathAndRename('Images/User/Graphs'))  # media/
    graph_input_data = models.TextField(blank=True, null=True)
    class Meta:
        default_permissions = ()


class RegisterQuestion(models.Model):
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class QuestionOption(models.Model):
    question = models.ForeignKey(RegisterQuestion, on_delete=models.CASCADE, related_name='options')
    option_name = models.CharField(max_length=500)

    def __str__(self):
        return self.option_name


class UserAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)