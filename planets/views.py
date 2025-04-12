from rest_framework import viewsets
from .models import Planet
from .serializers import PlanetSerializer

class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
