from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class FlatPageForm(forms.ModelForm):
    ...
    content = forms.CharField(widget=TinyMCE(attrs={"cols": 40, "rows": 30}))
    ...

    class Meta:
        model = FlatPage
