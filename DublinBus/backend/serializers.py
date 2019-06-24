"""
Convert query results to json files
"""

from rest_framework import serializers
from .models import *


class StopSerializer(serializers.ModelSerializer):
    """
    Convert stop data from gtfs to json
    """
    class Meta:
        # Specify mode
        model = Stops
        # Specify fields, this represents all fields
        fields = "__all__"

class RouteSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        # specify model
        model = Routes
        # Specify fields
        fields = "__all__"
