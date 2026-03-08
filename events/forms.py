from django import forms
from .models import Event


class EventRegistrationForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=forms.HiddenInput)
