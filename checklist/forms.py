from django import forms

from .models import Check

class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        exclude = []


class TrendsForm(forms.Form):
    date = forms.DateField()
    interval = forms.IntegerField()
