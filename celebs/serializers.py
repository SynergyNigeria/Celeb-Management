from rest_framework import serializers
from .models import Celebrity


class CelebrityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = ["id", "name", "slug", "tagline", "category", "photo", "nationality", "is_featured"]


class CelebrityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = "__all__"
