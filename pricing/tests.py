from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from pricing.models import AlertLog, PriceHistory, Product, UserTrackedProduct
from pricing.tasks import check_price_alerts, scrape_product_price
from scraper.price_parser import extract_price_from_html


class PricingFlowTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username="tester", password="secret123")
        self.product = Product.objects.create(name="Example Widget", url="https://example.com/widget", source_site="example")
        self.tracking = UserTrackedProduct.objects.create(
            user=self.user,
            product=self.product,
            threshold_price=Decimal("120.00"),
            is_active=True,
        )

    def test_scrape_product_price_creates_price_history(self) -> None:
        scraped = scrape_product_price(self.product.id)

        self.assertTrue(scraped)
        self.assertEqual(PriceHistory.objects.filter(product=self.product).count(), 1)
        self.assertGreaterEqual(PriceHistory.objects.get(product=self.product).price, Decimal("0.00"))

    def test_check_price_alerts_creates_log_when_threshold_is_breached(self) -> None:
        with patch("pricing.tasks.send_price_drop_alert.delay") as mocked_send:
            scrape_product_price(self.product.id)
            check_price_alerts()

        self.assertEqual(AlertLog.objects.count(), 1)
        mocked_send.assert_called_once()

    def test_extract_price_from_html_parses_currency_value(self) -> None:
        html = '<html><body><span class="price">$129.99</span></body></html>'

        self.assertEqual(extract_price_from_html(html), Decimal("129.99"))
