import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from models import *

class FeaturedItemForm(forms.ModelForm):
    class Meta:
        model = FeaturedItem
        exclude = ('image',)
class FeaturedItemImageForm(forms.ModelForm):
    class Meta:
        model = FeaturedItemImage
        exclude = ('effect','caption')