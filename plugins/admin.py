from django.contrib import admin

from plugins.models import PluginPoint, Plugin


class PluginPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('status',)
admin.site.register(PluginPoint, PluginPointAdmin)


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'status')
    list_filter = ('point', 'status')
admin.site.register(Plugin, PluginAdmin)
