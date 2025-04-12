from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanetViewSet

router = DefaultRouter()
router.register(r'planets', PlanetViewSet, basename='planet')

urlpatterns = [
    path('', include(router.urls)),
]
