from django.dispatch import Signal

django_plugin_disabled = Signal(providing_args=["plugin"])
django_plugin_enabled = Signal(providing_args=["plugin"])
