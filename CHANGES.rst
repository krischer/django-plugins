Changes
=======

0.3.0 (2016-07-06)
------------------

- Added support for Django 1.8 and 1.9.
- Now works for Django 1.6-1.9 and Python 2.7, 3.3, 3.4, and 3.5
- Using the `syncdb` Django command is no longer recommended. Please use
  `migrate` instead.
- Supports django migrations as well as a backwards compatible path for
  south migrations.

0.2.5 (2014-10-25)
------------------

- Officially supported Django versions are now 1.6.8 and 1.7.1.


0.2.4 (2014-07-04)
------------------

- Support for Python 3. Currently Python 2.7, 3.2, 3.3, and 3.4 are officially supported.


0.2.3 (2013-12-22)
------------------

- Django 1.6 support, thanks Felipe Ćlvarez for this.

- Added example-project to show how to use ``django-plugins``.

- Added possibility for ``include_plugins`` to specify more than one list of
  url patterns with possibility to customise inclusion url pattern.

- ``include_plugins`` now automatically provides ``plugin`` argument to view
  functions.

- Now it is possible to get plugin instance from plugon point like this:
  ``MyPluginPoint.get_plugin('plugin-name')``.


0.2.2 (2012-02-08)
------------------

- Improved ``PluginPoint.get_model()`` method, now this method also checks if
  plugin is enabled.


0.2.1 (2011-08-25)
------------------

- Fixed django-plugins setup.py, that was not installable.

- Fixed plugin fields introspection for south.


0.2 (2011-05-30)
----------------

- Plugin points and plugins moved from ``__init__.py`` to ``plugin_points.py``
  and ``plugins.py``

- Improved documentation.


0.1 (2011-01-11)
----------------

- First public release.
