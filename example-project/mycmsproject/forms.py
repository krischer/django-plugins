from __future__ import absolute_import

from django import forms

from .models import Content


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ()
