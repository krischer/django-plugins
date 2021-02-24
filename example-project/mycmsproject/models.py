from __future__ import absolute_import

from django.db import models

from djangoplugins.fields import PluginField

from mycmsproject.plugins import ContentType


class Content(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    plugin = PluginField(ContentType, editable=False, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return self.plugin.get_plugin().get_read_url(self)
