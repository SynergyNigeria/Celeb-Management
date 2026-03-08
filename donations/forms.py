from django import forms
from .models import Foundation


class DonationForm(forms.Form):
    foundation = forms.ModelChoiceField(queryset=Foundation.objects.filter(is_active=True), widget=forms.HiddenInput)
    amount = forms.DecimalField(
        min_value=1, max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Amount (USD)", "min": "1", "step": "0.01"}),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Leave a message of support (optional)"}),
    )
    is_anonymous = forms.BooleanField(required=False, label="Donate anonymously")
