from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

from bizwallet.core.models import EmailSubscribe, Services, ServicesVariations


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


class EmailSubscribeForm(forms.ModelForm):

    class Meta:
        model = EmailSubscribe
        fields = ['email']
