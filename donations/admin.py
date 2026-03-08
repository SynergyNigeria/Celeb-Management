from django.contrib import admin
from .models import Foundation, Donation


@admin.register(Foundation)
class FoundationAdmin(admin.ModelAdmin):
    list_display = ["celebrity", "name", "target_amount", "amount_raised", "is_active"]
    list_filter = ["celebrity", "is_active"]
    search_fields = ["name", "celebrity__name"]
    list_editable = ["is_active"]
    readonly_fields = ["amount_raised"]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ["foundation", "user", "amount", "donated_at", "is_anonymous"]
    list_filter = ["is_anonymous", "foundation__celebrity"]
    search_fields = ["user__email", "transaction_ref"]
    readonly_fields = ["id", "transaction_ref", "donated_at"]
