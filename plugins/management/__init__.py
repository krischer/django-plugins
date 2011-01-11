from django.db.models.signals import post_syncdb

from plugins import models as plugins_app
from plugins.management.commands.syncplugins import SyncPlugins


def sync_plugins(sender, verbosity, **kwargs):
    SyncPlugins(False, verbosity).all()
post_syncdb.connect(sync_plugins, sender=plugins_app)
