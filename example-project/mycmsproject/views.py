from __future__ import absolute_import
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import get_object_or_404

import mycmsproject


def index(request):
    return render(request, 'index.html')


def content_list(request, plugin):
    return render(request, 'content/list.html', {
        'plugin': mycmsproject.plugins.ContentType.get_plugin(plugin),
        'posts': mycmsproject.models.Content.objects.all(),
    })


def content_create(request, plugin):
    plugin = mycmsproject.plugins.ContentType.get_plugin(plugin)
    if request.method == 'POST':
        form = mycmsproject.forms.ContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.plugin = plugin.get_model()
            content.save()
            return HttpResponseRedirect(content.get_absolute_url())
        else:
            return "[ERROR] from views: {0}".format(form.errors)
    else:
        form = mycmsproject.forms.ContentForm()
    return render(request, 'content/form.html', {
        'form': form,
    })


def content_read(request, pk, plugin):
    plugin = mycmsproject.plugins.ContentType.get_plugin(plugin)
    content = get_object_or_404(mycmsproject.models.Content,
                                pk=pk, plugin=plugin.get_model())
    return render(request, 'content/read.html', {
        'plugin': plugin,
        'content': content,
    })
