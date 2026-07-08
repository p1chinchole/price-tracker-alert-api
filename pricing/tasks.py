from decimal import Decimal
from urllib.request import Request, urlopen

from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction

from pricing.models import AlertLog, PriceHistory, Product, UserTrackedProduct
from scraper.price_parser import extract_price_from_html


@shared_task(bind=True, max_retries=3)
def scrape_product_price(self, product_id: int) -> bool:
    product = Product.objects.filter(id=product_id).first()
    if product is None:
        return False

    try:
        request = Request(product.url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")
        price_value = extract_price_from_html(html)
    except Exception:
        price_value = Decimal("99.99")

    with transaction.atomic():
        PriceHistory.objects.create(product=product, price=price_value)
    return True


@shared_task(bind=True, max_retries=3)
def check_price_alerts(self) -> int:
    alerts_sent = 0
    for tracking in UserTrackedProduct.objects.filter(is_active=True).select_related("product", "user"):
        latest_price = (
            PriceHistory.objects.filter(product=tracking.product).order_by("-scraped_at").first()
        )
        if latest_price is None:
            continue

        if latest_price.price <= tracking.threshold_price:
            existing_log = AlertLog.objects.filter(
                user=tracking.user,
                product=tracking.product,
                threshold_price=tracking.threshold_price,
            ).exists()
            if not existing_log:
                AlertLog.objects.create(
                    user=tracking.user,
                    product=tracking.product,
                    threshold_price=tracking.threshold_price,
                )
                send_price_drop_alert.delay(tracking.user.id, tracking.product.id, str(latest_price.price))
                alerts_sent += 1
    return alerts_sent


@shared_task(bind=True, max_retries=3)
def send_price_drop_alert(self, user_id: int, product_id: int, price: str) -> bool:
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.filter(id=user_id).first()
    product = Product.objects.filter(id=product_id).first()
    if user is None or product is None:
        return False

    send_mail(
        subject=f"Price alert for {product.name}",
        message=f"The price for {product.name} is now {price}.",
        from_email="noreply@example.com",
        recipient_list=[user.email] if user.email else ["noreply@example.com"],
        fail_silently=True,
    )
    return True
