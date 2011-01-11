from django.test import TestCase

from plugins import PluginMount
from plugins.models import Plugin, PluginPoint
from plugins.models import ENABLED, REMOVED
from plugins.management.commands.syncplugins import SyncPlugins


class MyPluginPoint:
    __metaclass__ = PluginMount


class MyPlugin(MyPluginPoint):
    pass


class SimpleTest(TestCase):
    def test_plugin_sync(self):
        points = PluginPoint.objects.filter(
                        name='plugins.tests.MyPluginPoint')
        plugins = Plugin.objects.filter(
                        name='plugins.tests.MyPlugin')

        # At first there should not be any plugins in database
        self.assertEqual(points.count(), 0)
        self.assertEqual(plugins.count(), 0)

        # Now sync plugins and check if they appear in database
        sync = SyncPlugins(False, 0)
        sync.all()
        self.assertEqual(points.filter(status=ENABLED).count(), 1)
        self.assertEqual(plugins.filter(status=ENABLED).count(), 1)

        # Remove all plugin points and sync again, without deleting.
        # All plugin points (but not plugins) should be marked as REMOVED
        points_copy = PluginMount.points
        PluginMount.points = []
        sync.all()
        self.assertEqual(points.filter(status=REMOVED).count(), 1)
        self.assertEqual(plugins.filter(status=REMOVED).count(), 0)

        # Sync plugins again, with deleting all removed from database.
        # Using cascaded deletes, all plugins, that belongs to being deleted
        # plugin points will be deleted also.
        sync = SyncPlugins(True, 0)
        sync.all()
        self.assertEqual(points.count(), 0)
        self.assertEqual(plugins.count(), 0)

        PluginMount.points = points_copy
        sync = SyncPlugins(False, 0)
        sync.all()

    def test_plugins(self):
        SyncPlugins(False, 0).all()
        pass
