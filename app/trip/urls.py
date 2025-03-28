# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, test

router = DefaultRouter()
router.register(r"trips", TripViewSet, basename="trip")

urlpatterns = [
    path("", TripViewSet.as_view({"post": "create"}), name="trip-view"),
    path("test", test, name="test-endpoint"),
]
