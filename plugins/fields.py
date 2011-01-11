from django.db import models

from plugins.models import Plugin
from plugins.utils import get_plugin_name


class PluginField(models.ForeignKey):
    def __init__(self, point, **kwargs):
        kwargs['limit_choices_to'] = {
            'point__name': get_plugin_name(point),
        }
        super(PluginField, self).__init__(Plugin, **kwargs)


class ManyPluginField(models.ManyToManyField):
    def __init__(self, point, **kwargs):
        kwargs['limit_choices_to'] = {
            'point__name': get_plugin_name(point),
        }
        super(ManyPluginField, self).__init__(Plugin, **kwargs)
