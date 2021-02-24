"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from __future__ import absolute_import

from django.conf.urls import url

from djangoplugins.utils import include_plugins
from .plugins import ContentType
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^content/', include_plugins(ContentType)),
    url(r'^content/', include_plugins(
        ContentType, '{plugin}/(?P<pk>\d+)/', 'instance_urls'
    )),
]
