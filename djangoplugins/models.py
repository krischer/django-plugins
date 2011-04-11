from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import get_plugin_name, get_plugin_from_string

ENABLED = 0
DISABLED = 1
REMOVED = 2

STATUS_CHOICES = (
    (ENABLED,  _('Enabled')),
    (DISABLED, _('Disabled')),
    (REMOVED,  _('Removed')),
)


class PluginPointManager(models.Manager):
    def get_point(self, point):
        return self.get(name=get_plugin_name(point))


class PluginPoint(models.Model):
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)

    objects = PluginPointManager()

    def __unicode__(self):
        return self.name


class PluginManager(models.Manager):
    def get_plugin(self, plugin):
        return self.get(name=get_plugin_name(plugin))

    def get_plugins_of(self, point):
        return self.filter(point__name=get_plugin_name(point))

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Plugin(models.Model):
    point = models.ForeignKey(PluginPoint)
    name = models.CharField(max_length=255, unique=True)
    index = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)

    objects = PluginManager()

    class Meta:
        order_with_respect_to = 'point'
        ordering = ('index', 'id')

    def __unicode__(self):
        plugin = self.get_plugin()
        if hasattr(plugin, 'title'):
            return unicode(plugin.title)
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_plugin(self):
        plugin_class = get_plugin_from_string(self.name)
        return plugin_class()
