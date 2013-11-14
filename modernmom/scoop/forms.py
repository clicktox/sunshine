from django import forms
from models import *

class ScoopTopicForm(forms.ModelForm):
    class Meta:
        model = ScoopTopic
        exclude = ('image',)

class ScoopTopicTwitterForm(forms.ModelForm):
    class Meta:
        model = ScoopTopicTwitter
        #exclude = ('topic',)