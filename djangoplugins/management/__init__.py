from __future__ import absolute_import

try:
    from django.db.models.signals import post_migrate
except ImportError:
    from south.signals import post_migrate

from django.db.models.signals import post_syncdb


from djangoplugins import models as plugins_app
from .commands.syncplugins import SyncPlugins


def sync_plugins(sender, verbosity, **kwargs):
    SyncPlugins(False, verbosity).all()

# Always run after `migrate`.
post_migrate.connect(sync_plugins, sender=plugins_app)

# This is somehow needed for the tests to work.
# XXX: Figure out how to get rid of this.
post_syncdb.connect(sync_plugins, sender=plugins_app)
