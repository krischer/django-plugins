from django.contrib import admin

from .models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('title', 'index', 'status')
    list_filter = ('point', 'status')
admin.site.register(Plugin, PluginAdmin)
