from django.test import TestCase

from plugins import PluginMount
from plugins.models import Plugin, PluginPoint
from plugins.models import ENABLED, REMOVED
from plugins.management.commands.syncplugins import SyncPlugins


class MyPluginPoint:
    __metaclass__ = PluginMount


class MyPlugin(MyPluginPoint):
    pass


class PluginSyncTestCaseBase(TestCase):
    def delete_plugins_from_db(self):
        Plugin.objects.all().delete()
        PluginPoint.objects.all().delete()

    def prepate_query_sets(self):
        self.points = PluginPoint.objects.filter(
                        name='plugins.tests.MyPluginPoint')
        self.plugins = Plugin.objects.filter(
                        name='plugins.tests.MyPlugin')


class PluginSyncTestCase(PluginSyncTestCaseBase):
    def setUp(self):
        self.delete_plugins_from_db()
        self.prepate_query_sets()

    def test_plugins_not_synced(self):
        """
        At first there should not be any plugins in database
        """
        self.assertEqual(self.points.count(), 0)
        self.assertEqual(self.plugins.count(), 0)

    def test_plugins_are_synced(self):
        """
        Now sync plugins and check if they appear in database
        """
        SyncPlugins(False, 0).all()
        self.assertEqual(self.points.filter(status=ENABLED).count(), 1)
        self.assertEqual(self.plugins.filter(status=ENABLED).count(), 1)


class PluginSyncRemovedTestCase(PluginSyncTestCaseBase):
    def setUp(self):
        self.prepate_query_sets()
        self.copy_of_points = PluginMount.points

    def tearDown(self):
        PluginMount.points = self.copy_of_points

    def test_removed_plugins(self):
        """
        Remove all plugin points and sync again, without deleting.
        All plugin points (but not plugins) should be marked as REMOVED
        """
        PluginMount.points = []
        SyncPlugins(False, 0).all()
        self.assertEqual(self.points.filter(status=REMOVED).count(), 1)
        self.assertEqual(self.plugins.filter(status=REMOVED).count(), 0)

    def test_sync_and_delete(self):
        """
        Sync plugins again, with deleting all removed from database.
        Using cascaded deletes, all plugins, that belongs to being deleted
        plugin points will be deleted also.
        """
        PluginMount.points = []
        SyncPlugins(True, 0).all()
        self.assertEqual(self.points.count(), 0)
        self.assertEqual(self.plugins.count(), 0)


class PluginModels(TestCase):
    def test_plugins_of_point(self):
        plugin = Plugin.objects.get(name='plugins.tests.MyPlugin')
        qs = MyPluginPoint.get_plugins_qs()
        self.assertEqual(qs[0].id, plugin.id)

    def test_plugins_of_plugin(self):
        self.assertRaises(PluginPoint.DoesNotExist, MyPlugin.get_plugins_qs)
