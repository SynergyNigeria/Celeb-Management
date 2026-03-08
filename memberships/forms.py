from django import forms
from .models import MembershipTier


class MembershipPurchaseForm(forms.Form):
    tier = forms.ModelChoiceField(
        queryset=MembershipTier.objects.filter(is_active=True),
        widget=forms.HiddenInput,
    )
