from rest_framework import serializers
from .models import Foundation, Donation


class FoundationSerializer(serializers.ModelSerializer):
    progress_pct = serializers.ReadOnlyField()
    celebrity_name = serializers.CharField(source="celebrity.name", read_only=True)
    celebrity_slug = serializers.CharField(source="celebrity.slug", read_only=True)

    class Meta:
        model = Foundation
        fields = "__all__"


class DonationSerializer(serializers.ModelSerializer):
    foundation_name = serializers.CharField(source="foundation.name", read_only=True)
    donor_name = serializers.SerializerMethodField()
    foundation_id = serializers.PrimaryKeyRelatedField(
        queryset=Foundation.objects.filter(is_active=True), source="foundation", write_only=True
    )

    class Meta:
        model = Donation
        fields = [
            "id", "foundation", "foundation_id", "foundation_name",
            "amount", "message", "transaction_ref", "donated_at",
            "is_anonymous", "donor_name",
        ]
        read_only_fields = ["id", "donated_at", "foundation"]

    def get_donor_name(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.user.name if obj.user else "Deleted User"
