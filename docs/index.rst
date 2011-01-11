Welcome to django-plugins's documentation!
==========================================

Introduction
------------

``django-plugins`` will help you to make your Django app more reusable. You
will be able to define plugin points, plugins and various ways, how plugins can
be integrated to your base app and extended from other apps.

**Features**

- Synchronization with database.
- ``PluginField`` for your models.
- Possibility to include plugins to urls.
- Possibility to access plugins from templates.

Registering plugins and plugin points
-------------------------------------

Recommended way is to place all plugins and plugin points to ``__init__.py``
file of your django app.

Example how to register a plugin point::

    from plugins import PluginMount

    class MyPluginPoint:
        """
        Documentation, that describes how plugins can implement this plugin
        point.

        Example:

        Plugins implementing this reference should provide the following attributes:

        ========  ========================================================
        title     The text to be displayed, describing the action
        ========  ========================================================

        """
        __metaclass__ = PluginMount


Example, how to register plugin, that implements ``MyPluginPoint``, defined
above::

    class MyPlugin1(MyPluginPoint):
        title = 'Plugin 1'

    class MyPlugin2(MyPluginPoint):
        title = 'Plugin 2'

Synchronizing to database
-------------------------

All defined plugins and plugin points can be synchronized to database using
Django management command ``syncplugins``.

When added to database, plugins can be ordered, disabled, accessed from Django
admin, etc.

``syncplugins`` command detects if plugins or points where removed from code
and marks them as ``REMOVED``, but leaves then in place. If you want to clean
up your database and really delete all removed plugins us ``--delete`` flag.

Utilizing available plugins
---------------------------

There are many ways how you can use plugins and plugin points. Out of the box
plugins are stored as python objects and recored in database.

``get_plugins`` method of each plugin point class and plugin point model
instance, returns list of plugins instances.

Example, how to use plugins::

    from my_app import MyPluginPoint

    @register.inclusion_tag('templatetags/actions.html', takes_context=True)
    def my_plugins(context):
        plugins = MyPluginPoint.get_plugins()
        return {'plugins': plugins}

``templatetags/actions.html``::

    <ul>
        {% for plugin in plugins %}
        <li>plugin.title</li>
        {% endfor %}
    </ul>

If you need to order or filter plugins, you can always access them via Django
models::

    from plugins.models import PluginPoint
    from my_app import MyPluginPoint

    @render_to('my_app/my_template.html')
    def my_view(request):
        point = PluginPoint.objects.get_point(MyPluginPoint)
        plugins = point.plugin_set.order_by('name')
        return {'plugins': plugins}

Using plugins as fields
-----------------------

::

    from django.db import models
    from plugins.fields import PluginField
    from my_app import MyPluginPoint

    class MyModel(models.Model):
        plugin = PluginField(MyPluginPoint)

Using plugins in urls
---------------------

``django-plugins`` has build-in possibility to include urls from plugins. Here
is example how this can be done::

    from django.conf.urls.defaults import *
    from plugins.utils import include_plugins
    from my_app import MyPluginPoint

    urlpatterns = patterns('wora.views',
        (r'^plugin/', include_plugins(MyPluginPoint)),
    )

``include_plugins`` function will search ``urls`` and ``name`` properties in
all plugins, and if both is available, then will provided urls will be
included. Example plugin::

    class MyPluginWithUrls(MyPluginPoint):
        name = 'my-plugin'
        urls = patterns('my_app.views',
                (r'create/$', 'my_view', {}, 'my_app-create'),
            )

With this plugin, plugin point inclusion will provide these urls::

    plugin/my-plugin/create


Using plugins in templates
--------------------------

You can access your plugins in templates using ``get_plugins`` template tag.::

    {% load plugins %}
    {% get_plugins my_app.MyPluginPoint as plugins %}
    <ul>
        {% for plugin in plugins %}
        <li>{{ plugin.title }}</li>
        {% endfor %}
    </ul>

Why another plugin system?
--------------------------

Currently these similar projects exists:

- django-app-plugins_ - template oriented, pretty complete, but totally
  undocumented. Project is not active and bugs are fixed only in forked
  repository django-caching-app-plugins_.
- django-plugins_ - template oriented, small project. Plugins are uploaded
  through Django admin.

.. _django-app-plugins: http://code.google.com/p/django-app-plugins/
.. _django-plugins: https://github.com/alex/django-plugins
.. _django-caching-app-plugins: https://bitbucket.org/bkroeze/django-caching-app-plugins/

Also there is a lot of articles and code snippets, that describes how plugin
system can be implemented. Here is article, that most influenced this project:

- http://martyalchin.com/2008/jan/10/simple-plugin-framework/

Also see list of other articles and python plugin system implementations:

- http://wehart.blogspot.com/2009/01/python-plugin-frameworks.html

None of these projects fully provides what I need:

- Good documentation.
- Plugins and plugin points should be provided by Django apps, not only by
  single uploaded files.
- Plugins should not be restricted by file names, then can be registered
  anywhere, like Django signals.
- Plugins should be synchronized with database, and plugin point can be used as
  fields.


