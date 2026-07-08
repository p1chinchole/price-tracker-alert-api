from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    source_site = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pricing_product"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, related_name="pricehistory_set", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pricing_price_history"
        indexes = [models.Index(fields=["product", "scraped_at"])]
        ordering = ["-scraped_at"]

    def __str__(self) -> str:
        return f"{self.product.name} @ {self.price}"


class UserTrackedProduct(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tracked_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tracked_by")
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pricing_user_tracked_product"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.product.name}"


class AlertLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="alert_logs")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="alert_logs")
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pricing_alert_log"
        ordering = ["-sent_at"]

    def __str__(self) -> str:
        return f"Alert for {self.product.name}"
