from django.contrib import admin
from .models import Celebrity


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "nationality", "is_featured", "is_active", "created_at"]
    list_filter = ["category", "is_featured", "is_active"]
    search_fields = ["name", "bio", "nationality"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_featured", "is_active"]
