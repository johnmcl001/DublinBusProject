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

    def get_queryset(self):
        """
        Overwrite default get_queryset to produce desired result
        """
        stop_number = self.request.query_params.get("stopnumber")
        queryset = Stops.objects.filter(stop_id__endswith=stop_number)
        return queryset

class RouteView(viewsets.ModelViewSet):
    """
    For SearchByRoute
    """
    pass

class DestinationView(viewsets.ModelViewSet):
    """
    For SearchByDestination
    """
    pass
