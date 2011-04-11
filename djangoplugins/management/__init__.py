from django.db.models.signals import post_syncdb

from djangoplugins import models as plugins_app
from .commands.syncplugins import SyncPlugins


def sync_plugins(sender, verbosity, **kwargs):
    SyncPlugins(False, verbosity).all()
post_syncdb.connect(sync_plugins, sender=plugins_app)
