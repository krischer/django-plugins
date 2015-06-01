from __future__ import absolute_import

from django.conf.urls import patterns, url

from djangoplugins.utils import include_plugins

from .plugins import ContentType

urlpatterns = patterns(
    'mycmsproject.views',
    url(r'^$', 'index', name='index'),
    url(r'^content/', include_plugins(ContentType)),
    url(r'^content/', include_plugins(
        ContentType, '{plugin}/(?P<pk>\d+)/', 'instance_urls'
    )),
)
