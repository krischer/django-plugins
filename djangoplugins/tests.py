from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from .point import PluginMount, PluginPoint
from .models import Plugin, PluginPoint as PluginPointModel
from .models import ENABLED, REMOVED
from .management.commands.syncplugins import SyncPlugins


class MyPluginPoint(PluginPoint):
    pass


class MyPlugin(MyPluginPoint):
    pass


class MyPluginFull(MyPluginPoint):
    name = 'my-plugin-full'
    title = _('My Plugin Full')


class PluginSyncTestCaseBase(TestCase):
    def delete_plugins_from_db(self):
        Plugin.objects.all().delete()
        PluginPointModel.objects.all().delete()

    def prepate_query_sets(self):
        self.points = PluginPointModel.objects.filter(
                        name='djangoplugins.tests.MyPluginPoint')
        self.plugins = Plugin.objects.filter(
                        name='djangoplugins.tests.MyPlugin')


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
        qs = MyPluginPoint.get_plugins_qs()
        self.assertEqual(2, qs.count())

    def test_plugin_model(self):
        plugin_name = 'djangoplugins.tests.MyPlugin'
        plugin = Plugin.objects.get(name=plugin_name)
        self.assertEqual(plugin_name, unicode(plugin))
        self.assertEqual((plugin_name,), plugin.natural_key())

    def test_plugin_model_full(self):
        plugin_name = 'djangoplugins.tests.MyPluginFull'
        plugin = Plugin.objects.get(name=plugin_name)
        self.assertEqual(_('My Plugin Full'), unicode(plugin))

    def test_plugin_point_model(self):
        point_name = 'djangoplugins.tests.MyPluginPoint'
        point = PluginPointModel.objects.get(name=point_name)
        self.assertEqual(point_name, unicode(point))

    def test_plugins_of_plugin(self):
        self.assertRaises(PluginPointModel.DoesNotExist, MyPlugin.get_plugins_qs)
