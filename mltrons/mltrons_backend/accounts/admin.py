# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdminModel(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'company_name', 'is_admin', 'is_active']
    list_filter = ('is_admin',)


admin.site.register(User, UserAdminModel)
