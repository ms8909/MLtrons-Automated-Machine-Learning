# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MlbotConfig(AppConfig):
    name = 'mlbot'

    def ready(self):
        pass
        import mlbot.signals
