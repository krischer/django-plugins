from __future__ import absolute_import

# Import cascade to work with a number of Django versions.
try:
    from django.db.models.signals import post_migrate
except ImportError:
    try:
        from django.db.models.signals import post_syncdb as post_migrate
    except ImportError:
        from south.signals import post_migrate


from djangoplugins import models as plugins_app
from .commands.syncplugins import SyncPlugins


def sync_plugins(sender, verbosity, **kwargs):
    # Different django version have different senders.
    if (hasattr(sender, "name") and sender.name == "djangoplugins") or \
            (sender == plugins_app):
        SyncPlugins(False, verbosity).all()


# Plugins must be synced to the database.
post_migrate.connect(sync_plugins)
