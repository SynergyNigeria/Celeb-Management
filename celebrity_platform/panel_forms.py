from django import forms
from celebs.models import Celebrity
from memberships.models import MembershipTier
from donations.models import Foundation
from events.models import Event

_W = {"class": "input-field"}


class CelebrityForm(forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = [
            "name", "slug", "tagline", "bio", "category",
            "photo", "cover_image", "nationality",
            "instagram", "twitter", "youtube",
            "is_featured", "is_active",
        ]
        widgets = {
            "name":        forms.TextInput(attrs=_W),
            "slug":        forms.TextInput(attrs=_W),
            "tagline":     forms.TextInput(attrs=_W),
            "bio":         forms.Textarea(attrs={**_W, "rows": 5}),
            "category":    forms.Select(attrs=_W),
            "nationality": forms.TextInput(attrs=_W),
            "instagram":   forms.URLInput(attrs=_W),
            "twitter":     forms.URLInput(attrs=_W),
            "youtube":     forms.URLInput(attrs=_W),
        }


class MembershipTierForm(forms.ModelForm):
    class Meta:
        model = MembershipTier
        fields = ["celebrity", "name", "description", "price", "duration_days", "benefits", "badge_color", "is_active"]
        widgets = {
            "celebrity":    forms.Select(attrs=_W),
            "name":         forms.TextInput(attrs=_W),
            "description":  forms.Textarea(attrs={**_W, "rows": 3}),
            "price":        forms.NumberInput(attrs=_W),
            "duration_days": forms.NumberInput(attrs=_W),
            "benefits":     forms.Textarea(attrs={**_W, "rows": 6, "placeholder": "One benefit per line"}),
            "badge_color":  forms.Select(attrs=_W),
        }


class FoundationForm(forms.ModelForm):
    class Meta:
        model = Foundation
        fields = ["celebrity", "name", "description", "target_amount", "amount_raised", "cause_type", "cover_image", "is_active"]
        widgets = {
            "celebrity":     forms.Select(attrs=_W),
            "name":          forms.TextInput(attrs=_W),
            "description":   forms.Textarea(attrs={**_W, "rows": 4}),
            "target_amount": forms.NumberInput(attrs=_W),
            "amount_raised": forms.NumberInput(attrs=_W),
            "cause_type":    forms.TextInput(attrs={**_W, "placeholder": "e.g. Education, Health"}),
        }


class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={**_W, "type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={**_W, "type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Event
        fields = [
            "celebrity", "title", "slug", "description", "event_type", "status",
            "event_date", "end_date", "location", "venue", "city", "country",
            "image", "ticket_price", "is_free", "seats_total",
        ]
        widgets = {
            "celebrity":    forms.Select(attrs=_W),
            "title":        forms.TextInput(attrs=_W),
            "slug":         forms.TextInput(attrs=_W),
            "description":  forms.Textarea(attrs={**_W, "rows": 4}),
            "event_type":   forms.Select(attrs=_W),
            "status":       forms.Select(attrs=_W),
            "location":     forms.TextInput(attrs=_W),
            "venue":        forms.TextInput(attrs=_W),
            "city":         forms.TextInput(attrs=_W),
            "country":      forms.TextInput(attrs=_W),
            "ticket_price": forms.NumberInput(attrs=_W),
            "seats_total":  forms.NumberInput(attrs=_W),
        }
