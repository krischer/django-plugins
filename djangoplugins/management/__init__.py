from __future__ import absolute_import

from django.db.models.signals import post_migrate

from djangoplugins import models as plugins_app
from .commands.syncplugins import SyncPlugins


def sync_plugins(sender, verbosity, **kwargs):
    SyncPlugins(False, verbosity).all()

# Always run after `migrate`.
post_migrate.connect(sync_plugins, sender=plugins_app)
