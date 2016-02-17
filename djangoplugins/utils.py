from __future__ import absolute_import

from os.path import join, exists, dirname

from django.conf import settings

from django.conf.urls import include, patterns

from importlib import import_module


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


def include_plugins(point, pattern=r'{plugin}/', urls='urls'):
    pluginurls = []
    for plugin in point.get_plugins():
        if hasattr(plugin, urls) and hasattr(plugin, 'name'):
            _urls = getattr(plugin, urls)
            for url in _urls:
                url.default_args['plugin'] = plugin.name
            pluginurls.append((
                pattern.format(plugin=plugin.name),
                include(_urls)
            ))
    return include(patterns('', *pluginurls))


def import_app(app_name):
    try:
        mod = import_module(app_name)
    except ImportError:  # Maybe it's AppConfig
        parts = app_name.split('.')
        tmp_app, app_cfg_name = '.'.join(parts[:-1]), parts[-1]
        try:
            tmp_app = import_module(tmp_app)
        except ImportError:
            raise
        mod = getattr(tmp_app, app_cfg_name).name
        mod = import_module(mod)

    return mod


def load_plugins():
    for app in settings.INSTALLED_APPS:
        try:
            import_module('%s.plugins' % app)
        except ImportError as e:
            # If module exists but still can't be imported it means, that there
            # is error inside plugins module.
            mod = import_app(app)
            if exists(join(dirname(mod.__file__), 'plugins.py')):
                raise e
