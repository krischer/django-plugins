from __future__ import absolute_import

from django import forms
from django.db import models

from .models import Plugin
from .utils import get_plugin_name


class PluginField(models.ForeignKey):
    def __init__(self, point=None, *args, **kwargs):

        # If not migrating, add a new fields.
        if point is not None:
            kwargs['limit_choices_to'] = {
                'point__pythonpath': get_plugin_name(point)
            }

        super(PluginField, self).__init__(
            to=kwargs.pop("to", Plugin), *args, **kwargs)


class ManyPluginField(models.ManyToManyField):
    def __init__(self, point=None, *args, **kwargs):

        # If not migrating, add a new fields.
        if point is not None:
            kwargs['limit_choices_to'] = {
                'point__pythonpath': get_plugin_name(point)
            }

        super(ManyPluginField, self).__init__(
            to=kwargs.pop("to", Plugin), *args, **kwargs)


def get_plugins_qs(point):
    return point.get_plugins_qs().exclude(name__isnull=True)


class PluginChoiceField(forms.ModelChoiceField):
    def __init__(self, point, *args, **kwargs):
        kwargs['to_field_name'] = 'name'
        super(PluginChoiceField, self).\
            __init__(queryset=get_plugins_qs(point), **kwargs)

    def to_python(self, value):
        value = super(PluginChoiceField, self).to_python(value)
        if value:
            return value.get_plugin()
        else:
            return value


class PluginMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, point, *args, **kwargs):
        kwargs['to_field_name'] = 'name'
        super(PluginMultipleChoiceField, self).\
            __init__(queryset=get_plugins_qs(point), **kwargs)


class PluginModelChoiceField(forms.ModelChoiceField):
    def __init__(self, point, *args, **kwargs):
        super(PluginModelChoiceField, self).\
            __init__(queryset=get_plugins_qs(point), **kwargs)


class PluginModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, point, *args, **kwargs):
        super(PluginModelMultipleChoiceField, self).\
            __init__(queryset=get_plugins_qs(point), **kwargs)
