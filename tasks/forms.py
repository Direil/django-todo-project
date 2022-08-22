from django import forms

from .models import *


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add new task', 'id': 'add-task'})
    )

    class Meta:
        model = Task
        fields = ['title', 'complete']


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label="From:", widget=forms.TextInput( attrs={'size': '10', 'placeholder': 'mm-dd-yy'}))
    end_date = forms.DateField(label="To:", widget=forms.TextInput(attrs={'size': '10', 'placeholder': 'mm-dd-yy'}))


