from django import forms
from models import *

class ContestantEntryWinnerForm(forms.ModelForm):
    class Meta:
        model = ContestantEntryWinner
        exclude = ('chosen_on','chosen_by')

class ContestantEntryImageForm(forms.ModelForm):
    class Meta:
        model = ContestantEntryImage
        fields = ('image',)