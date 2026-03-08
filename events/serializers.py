from rest_framework import serializers
from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    celebrity_name = serializers.CharField(source="celebrity.name", read_only=True)
    celebrity_slug = serializers.CharField(source="celebrity.slug", read_only=True)
    seats_available = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = "__all__"


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source="event", write_only=True
    )

    class Meta:
        model = EventRegistration
        fields = ["id", "event", "event_id", "transaction_ref", "amount_paid", "registered_at", "attended"]
        read_only_fields = ["id", "registered_at", "attended"]
