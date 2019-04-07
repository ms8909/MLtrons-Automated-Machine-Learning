# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


# Register your models here.

class DatasetInline(admin.TabularInline):
    model = DataSet
    extra = 1

# Register your models here.
class ProjectAdminModel(admin.ModelAdmin):
    list_display = ['name', 'user', 'status']
    list_filter = ('status',)
    inlines = (DatasetInline,)

class MetaInline(admin.TabularInline):
    model = Meta
    extra = 1

class DatasetAdminModel(admin.ModelAdmin):
    list_display = ['name', 'project', 'file_url', 'status']
    list_filter = ('status',)
    inlines = (MetaInline,)

class PredictionValuesAdminModel(admin.ModelAdmin):
    list_display = ['project', 'file_url', 'created_at']


class GraphAdminModel(admin.ModelAdmin):
    list_display = ['name', 'project', 'type']

admin.site.register(Project, ProjectAdminModel)
admin.site.register(DataSet, DatasetAdminModel)
admin.site.register(Graph, GraphAdminModel)
admin.site.register(MetaType)
admin.site.register(MetaRole)
admin.site.register(MetaImputation)
admin.site.register(ProblemType)
admin.site.register(TimeType)
admin.site.register(ForecastGroupBy)
admin.site.register(GraphType)
admin.site.register(Metric)

