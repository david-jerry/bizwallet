from bizwallet.core.models import ServicesVariations, Services
from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'row': 40}))


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title', "image", 'description', 'active']



class ServicesVariationForm(forms.ModelForm):
    class Meta:
        model = ServicesVariations
        fields = ['service', 'title', 'min_investment', "percentage", 'duration', 'active']