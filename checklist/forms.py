from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Check, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'interval']
        labels = {
            'name': _('name'),
            'interval': _('interval'),
        }


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        exclude = []


class TrendsForm(forms.Form):
    date = forms.DateField()
    interval = forms.IntegerField()
