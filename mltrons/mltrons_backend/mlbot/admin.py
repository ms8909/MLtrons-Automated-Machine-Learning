# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class OptionInline(admin.StackedInline):
    model = QuestionOption
    fields = ('option_name', )
    extra = 1

# Register your models here.
class QuestionAdminModel(admin.ModelAdmin):
    list_display = ['question']
    inlines = (OptionInline,)


admin.site.register(RegisterQuestion, QuestionAdminModel)
