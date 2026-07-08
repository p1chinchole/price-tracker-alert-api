from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from pricing.models import AlertLog, PriceHistory, Product, UserTrackedProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "url", "source_site", "created_at"]


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ["id", "product", "price", "scraped_at"]


class UserTrackedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrackedProduct
        fields = ["id", "product", "threshold_price", "is_active", "created_at"]


class AlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLog
        fields = ["id", "user", "product", "threshold_price", "sent_at"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
