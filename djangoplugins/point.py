from .models import PluginPoint as PluginPointModel
from .utils import get_plugin_name

_PLUGIN_POINT = "<class 'djangoplugins.point.PluginPoint'>"


def is_plugin_point(cls):
    return repr(cls.__base__) == _PLUGIN_POINT


class PluginMount(type):
    """
    See: http://martyalchin.com/2008/jan/10/simple-plugin-framework/

    """

    points = []

    def __new__(meta, class_name, bases, class_dict):
        cls = type.__new__(meta, class_name, bases, class_dict)
        if is_plugin_point(cls):
            PluginMount.points.append(cls)
        return cls

    def __init__(cls, name, bases, attrs):
        if is_plugin_point(cls):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        elif hasattr(cls, 'plugins'):
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        """
        Returns all plugin instances of plugin point, passing all args and
        kwargs to plugin constructor.
        """
        return [p(*args, **kwargs) for p in cls.plugins]

    def get_plugins_qs(cls):
        """
        Returns query set of all plugins belonging to plugin point.

        Example::

            for plugin_instance in MyPluginPoint.get_plugins_qs():
                print(plugin_instance.get_plugin().name)

        """
        instance = PluginPointModel.objects.get(name=get_plugin_name(cls))
        return instance.plugin_set.all()


class PluginPoint(object):
    __metaclass__ = PluginMount
