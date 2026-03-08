from rest_framework import serializers
from .models import MembershipTier, MembershipPurchase
from celebs.serializers import CelebrityListSerializer


class MembershipTierSerializer(serializers.ModelSerializer):
    celebrity_name = serializers.CharField(source="celebrity.name", read_only=True)
    celebrity_slug = serializers.CharField(source="celebrity.slug", read_only=True)

    class Meta:
        model = MembershipTier
        fields = "__all__"


class MembershipPurchaseSerializer(serializers.ModelSerializer):
    tier = MembershipTierSerializer(read_only=True)
    tier_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipTier.objects.filter(is_active=True), source="tier", write_only=True
    )

    class Meta:
        model = MembershipPurchase
        fields = ["id", "tier", "tier_id", "transaction_ref", "amount_paid", "purchased_at", "expires_at", "is_active"]
        read_only_fields = ["id", "purchased_at", "is_active"]
