from django.contrib import admin
from .models import MembershipTier, MembershipPurchase


@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ["celebrity", "name", "price", "duration_days", "badge_color", "is_active"]
    list_filter = ["celebrity", "badge_color", "is_active"]
    search_fields = ["name", "celebrity__name"]
    list_editable = ["is_active"]


@admin.register(MembershipPurchase)
class MembershipPurchaseAdmin(admin.ModelAdmin):
    list_display = ["user", "tier", "amount_paid", "purchased_at", "expires_at", "is_active"]
    list_filter = ["is_active", "tier__celebrity"]
    search_fields = ["user__email", "user__name", "transaction_ref"]
    readonly_fields = ["id", "transaction_ref", "purchased_at"]
