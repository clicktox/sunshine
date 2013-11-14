import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from articles.models import Article,ArticleImage
from taxonomy.models import *
from django_bootstrap_wysiwyg.widgets import WysiwygInput

class ScoopItemForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        #load authors created by this user...
        #if staff, load all authors created by staff...
        super(ScoopItemForm, self).__init__(*args, **kwargs)

   

    def save(self, *args, **kwargs):
        return super(ScoopItemForm, self).save(*args, **kwargs)

    class Meta:
        model = Article
        exclude = ('slug','authors','creator','sites','image','description','markup',
                   'rendered_introduction','content','autotag','followup_for',
                   'keywords','auto_tag','related_articles')
        widgets = {
            'introduction': WysiwygInput()
        }

class ScoopItemSlideshowForm(forms.ModelForm):
    authors = forms.ChoiceField(required=False)
    #followup_for = forms.CharField(max_length=1500,required=False) #TypeAhead
    #related_articles = forms.CharField(max_length=1500,required=False) #TypeAhead

    def __init__(self, *args, **kwargs):
        #load authors created by this user...
        #if staff, load all authors created by staff...
        super(ScoopItemSlideshowForm, self).__init__(*args, **kwargs)

   

    def save(self, *args, **kwargs):
        return super(ScoopItemSlideshowForm, self).save(*args, **kwargs)

    class Meta:
        model = Article
        exclude = ('slug','author','creator','sites','image','description','markup',
                   'rendered_introduction','content','autotag','followup_for',
                   'keywords','auto_tag','related_articles','is_active','display_type')
        widgets = {
            'introduction': WysiwygInput(toolbar_items=['font-sizes', 'alignments','link'])
        }
        
class ScoopItemImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #load authors created by this user...
        #if staff, load all authors created by staff...
        super(ScoopItemImageForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super(ScoopItemImageForm, self).save(*args, **kwargs)

    class Meta:
        model = ArticleImage
        exclude = ('effect',)
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('uuid','slug','priority','tags')

class TopicImageForm(forms.ModelForm):
    class Meta:
        model = TopicImage
        exclude = ('topic',)
