"""
Convert query results to json files
"""

from rest_framework import serializers
from .models import Routes, Stops


class StopSerializer(serializers.ModelSerializer):
    """
    Convert stop data from gtfs to json
    """
    class Meta:
        """
        Meta data for StopSerializer, model and what to return
        """
        model = Stops
        # Return more specific fields when we know what we want
        fields = "__all__"

class RouteSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        """
        Meta data for RouteSerializer, model and what to return
        """
        model = Routes
        # Return more specific fields when we know what we want
        fields = "__all__"
