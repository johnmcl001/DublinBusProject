from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *

# Create your views here.


class StopView(viewsets.ModelViewSet):
    """
    Implement logic for SearchByStop here
    Currently returns list of stops ending in stop number
    Stop number supplied in url/?stopnumber=xxxx
    """
    # Define which serializer to use
    serializer_class = StopSerializer
    queryset = Stops.objects.all()

class RouteView(viewsets.ModelViewSet):
    """
    For SearchByRoute
    """
    serializer_class = RouteSerializer
    queryset = Routes.objects.all()

class DestinationView(viewsets.ModelViewSet):
    """
    For SearchByDestination
    """
    pass
