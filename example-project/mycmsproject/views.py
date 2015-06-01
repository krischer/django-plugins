from __future__ import absolute_import

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Content
from .plugins import ContentType
from .forms import ContentForm


def index(request):
    return render(request, 'index.html')


def content_list(request, plugin):
    return render(request, 'content/list.html', dict(
        plugin=ContentType.get_plugin(plugin),
        posts=Content.objects.all(),
    ))


def content_create(request, plugin):
    plugin = ContentType.get_plugin(plugin)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.plugin = plugin.get_model()
            content.save()
            return content.get_absolute_url()
    else:
        form = ContentForm()
    return render(request, 'content/form.html', dict(
        form=form,
    ))


def content_read(request, pk, plugin):
    plugin = ContentType.get_plugin(plugin)
    content = get_object_or_404(Content, pk=pk, plugin=plugin.get_model())
    return render(request, 'content/read.html', dict(
        plugin=plugin,
        content=content,
    ))
