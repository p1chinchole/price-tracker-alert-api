from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import (
    AlertLogSerializer,
    PriceHistorySerializer,
    ProductSerializer,
    UserRegistrationSerializer,
    UserTrackedProductSerializer,
)
from pricing.models import AlertLog, PriceHistory, Product, UserTrackedProduct


def home_view(request):
    user_count = get_user_model().objects.count()
    html = f"""
    <!doctype html>
    <html lang=\"en\">
    <head>
        <meta charset=\"utf-8\">
        <title>Price Tracker & Alert API</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            code {{ background: #f4f4f4; padding: 2px 6px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-top: 16px; }}
            .status {{ background: #e8f5e9; color: #2e7d32; padding: 10px 14px; border-radius: 6px; display: inline-block; }}
            button {{ padding: 10px 14px; border: none; background: #1976d2; color: white; border-radius: 6px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>Price Tracker & Alert API</h1>
        <div class=\"status\">Live status: API is running</div>
        <p>This backend lets users register, track products, store price history, and receive alerts when a price drops below a threshold.</p>
        <div class=\"card\">
            <h2>Demo action</h2>
            <p>Registered users currently in the database: <strong>{user_count}</strong></p>
            <p>Use the registration endpoint to create a new user and see the count grow.</p>
            <a href=\"/api/register/\" target=\"_blank\"><button>Open registration endpoint</button></a>
        </div>
        <div class=\"card\">
            <h2>Available endpoints</h2>
            <ul>
                <li><code>/api/register/</code> – create a user</li>
                <li><code>/api/token/</code> – obtain JWT tokens</li>
                <li><code>/api/products/</code> – list products</li>
                <li><code>/api/tracked-products/</code> – manage tracked products</li>
                <li><code>/api/alerts/</code> – view alert history</li>
            </ul>
        </div>
        <div class=\"card\">
            <h2>Tech stack</h2>
            <p>Django, Django REST Framework, JWT, Celery, Redis, and a Scrapy-based scraper pipeline.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        product = self.get_object()
        history = product.pricehistory_set.all().order_by("scraped_at")
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = PriceHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PriceHistorySerializer(history, many=True)
        return Response(serializer.data)


class PriceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceHistory.objects.all().order_by("-scraped_at")
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTrackedProductViewSet(viewsets.ModelViewSet):
    serializer_class = UserTrackedProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTrackedProduct.objects.filter(user=self.request.user).select_related("product").order_by("-created_at")

    @action(detail=False, methods=["get"])
    def my_products(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AlertLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlertLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AlertLog.objects.filter(user=self.request.user).order_by("-sent_at")


class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    pass
