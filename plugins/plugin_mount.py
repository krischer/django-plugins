class PluginMount(type):
    """
    See: http://martyalchin.com/2008/jan/10/simple-plugin-framework/

    """

    points = []

    def __new__(meta, class_name, bases, class_dict):
        cls = type.__new__(meta, class_name, bases, class_dict)
        if class_dict.get('__metaclass__', None) == PluginMount:
            PluginMount.points.append(cls)
        return cls

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
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
