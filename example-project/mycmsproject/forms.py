from django import forms

from .models import Content


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
