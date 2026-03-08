from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["celebrity", "title", "event_type", "status", "event_date", "location", "ticket_price", "is_free"]
    list_filter = ["celebrity", "event_type", "status", "is_free"]
    search_fields = ["title", "location", "city", "celebrity__name"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["status"]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "amount_paid", "registered_at", "attended"]
    list_filter = ["attended", "event__celebrity"]
    search_fields = ["user__email", "transaction_ref"]
    readonly_fields = ["id", "transaction_ref", "registered_at"]
