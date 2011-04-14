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
        return self.get(pythonpath=get_plugin_name(point))


class PluginPoint(models.Model):
    pythonpath = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)

    objects = PluginPointManager()

    def __unicode__(self):
        return self.title


class PluginManager(models.Manager):
    def get_plugin(self, plugin):
        return self.get(pythonpath=get_plugin_name(plugin))

    def get_plugins_of(self, point):
        return self.filter(point__pythonpath=get_plugin_name(point),
                           status=ENABLED)

    def get_by_natural_key(self, name):
        return self.get(pythonpath=name)


class Plugin(models.Model):
    """
    Database representation of a plugin.

    Fields ``name`` and ``title`` are synchronized from plugin classes.

    point
        Plugin point.

    pythonpath
        Full python path to plugin class, including class too.

    name
        Plugin slug name, must be unique within one plugin point.

    title
        Eny verbose title of this plugin.

    index
        Using values from this field plugins are orderd.

    status
        Plugin status.
    """
    point = models.ForeignKey(PluginPoint)
    pythonpath = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, default='', blank=True)
    index = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)

    objects = PluginManager()

    class Meta:
        unique_together = (("point", "name"),)
        order_with_respect_to = 'point'
        ordering = ('index', 'id')

    def __unicode__(self):
        if self.title:
            return self.title
        if self.name:
            return self.name
        return self.pythonpath

    def natural_key(self):
        return (self.pythonpath,)

    def is_active(self):
        return self.status == ENABLED

    def get_plugin(self):
        plugin_class = get_plugin_from_string(self.pythonpath)
        return plugin_class()
