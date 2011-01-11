from django.conf.urls.defaults import include, patterns
from django.utils.importlib import import_module


def get_plugin_name(cls):
    return "%s.%s" % (cls.__module__, cls.__name__)


def get_plugin_from_string(plugin_name):
    """
    Returns plugin or plugin point class from given ``plugin_name`` string.

    Example of ``plugin_name``::

        'my_app.MyPlugin'

    """
    modulename, classname = plugin_name.rsplit('.', 1)
    module = import_module(modulename)
    return getattr(module, classname)


def include_plugins(point):
    urls = []
    for plugin in point.get_plugins():
        if hasattr(plugin, 'urls') and hasattr(plugin, 'name'):
            urls.append((r'%s/' % (plugin.name), include(plugin.urls)))
    return include(patterns('', *urls))
