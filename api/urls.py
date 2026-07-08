from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AlertLogViewSet, PriceHistoryViewSet, ProductViewSet, UserTrackedProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"price-history", PriceHistoryViewSet, basename="price-history")
router.register(r"tracked-products", UserTrackedProductViewSet, basename="tracked-product")
router.register(r"alerts", AlertLogViewSet, basename="alert")

urlpatterns = [
    path("", include(router.urls)),
]
